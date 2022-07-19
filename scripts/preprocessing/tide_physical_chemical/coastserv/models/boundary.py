'''
Boundary
A class that can create boundary conditions from CMEMS
'''

import os
import gc
import glob
import datetime
import numpy as np 
import shutil as sh
import netCDF4 as nc 
from scipy.interpolate import griddata, LinearNDInterpolator, RegularGridInterpolator
import scipy.ndimage as nd
from coastserv.models.units.units import usefor, constituent_boundary_type, ini
import coastserv.models.utils as utils

class Boundary(object):

    def __init__(self, ext, data_list, sub, tref, model_dir):
        """
        Model class
        
        Arguments:
            ext {str} -- ext file produced from Tide.initiate_tide()
            data_list {str} -- path to location of downloaded CMEMS *.nc files
            sub {list} -- list of constituents corresponding to DFM names
            tref {datetime.datetime} -- datetime.datetime(yyyy,mm,dd,hh,MM,SS)
            model_dir {str} -- path to output
        """
        
        self.ext       = ext
        print('data files expected to be found in ' + data_list)
        self.data_list = data_list   
        self.sub_in    = sub
        self.tref      = tref
        self.dir       = model_dir
        self.fill      = {}

    def build_boundary(self, interp = False, simultaneous = False, search = 3, steric = True):
        """creates boundary conditions
        
        Keyword Arguments:
            interp {bool} -- if true then regular grid interpolation is conducted on 48 local cells, otherwise nearest neighbour (default: {False})
            simultaneous {bool} -- if true then all data is interpolated at the same time across entire domain(default: {False})
            search {int} -- subsection of data to use in interpolation (1/2 width of search square)
            steric {bool} -- if true then steric boundary will be created
        """

        self.interp = interp
        self.simultaneous = simultaneous
        self.search = search
        self.steric = steric

        self.make_boundary()

    def make_boundary(self, grid = None):
        """creates bc files, pli files, and possibly initial conditions for FM constituents
        
        Keyword Arguments:
            grid {[str]} -- [path to _net.nc file, necessary for initial conditions] (default: {None})
        """
        
        if isinstance(self.sub_in, str):
            print('ERROR: substances must be a list')
            
        else:
            self.subs = self.sub_in

        # parse ext file to get boundaries dictionary
        self.boundaries = utils.boundary_from_ext(self.ext)

        # return a file that can be representative of all files to get meta data
        match = self.check_files()
        ds = nc.Dataset(match)

        # add meta data
        self.get_boundary_index(ds)
        # extracts data from files as necessary, and writes to .bc file
        self.process_bc()

        # makes new pli files for the new boundaries
        self.write_pli()

        # makes a copy of the passed ext file and appends the new boundaries
        self.write_new_ext_file()

        self.write_ini(grid)

    def check_files(self):
        """
        from the list of requested subs and the location of the files, find out
        how complete the data list is, and find one file that can be representative
        w.r.t. attributes and such
        """
        count = list()
        sub_data_list = list()
        
        self.data_list = glob.glob(self.data_list)
            
        for sub in self.subs:
            if sub in usefor.keys():
                csub = usefor[sub] # csub is name of sub in CMEMS nomenclature
                query = [file for file in self.data_list if csub['substance'][0] in file]
                print('files for %s: %i' % (csub['substance'][0], len(query)))
                sub_data_list.append(query)
                count.append(len(query))
            else:
                count.append(0)
        
        count = np.array(count)
        if sum(count) == 0:
            print('ERROR: cannot continue with boundary creation, no data files found for ANY variable')
            print('usefor.keys() = ') 
            print(list(usefor.keys()))
            print('self.subs = ' )
            print(self.subs)
            print('checked %s' % self.data_list)
            raise FileNotFoundError
        elif sum(count >0) > 0 and sum(count > 0) != len(self.subs):
            print('WARNING: no data files available for some variables, will try to continue')
            print('suspected missing subs:')
            for sind, ss in enumerate(self.subs):
                if count[sind] == 0:
                    print(ss)
        else:
            print('Data files found for all variables')
        print('subs:')
        print(self.subs)
        print('# of files available:')
        print(count)
        if len(set(count)) > 1:
            print('WARNING: SOME VARIABLES COVER DIFFERENT TIME SPANS THAN OTHERS, RESULTING BOUNDARIES WILL NOT BE VALID. SEE INCONGRUENCY BETWEEN NUMBER OF FILES FOUND IN ARRAY ABOVE')
        
        # find the first substance that has a data file so the geometry can be extracted a single time
        ind = count > 0
        for i, bol in enumerate(ind):
            if bol:
                match =  i
                break

        return sub_data_list[match][0]


    def get_boundary_index(self, ds):
        """
        returns the passed boundaries dictionary with the corresponding xy and CMEMS index per point added
        (nearest neighbour)
        
        Arguments:
            ds {nectCDF4 dataset} -- [description]
        """
        boundaries = self.boundaries

        XCM = ds.variables['longitude'][:]
        YCM = ds.variables['latitude'][:]
        
        # Iterating over the boundaries
        for bnd in boundaries.keys():
            if boundaries[bnd]['type'] == 'waterlevelbnd':
                boundaries, pli = self.update_pli_loc(boundaries, bnd)
                boundaries[bnd]['CMEMS_index'] = np.zeros((len(pli),2))
                boundaries[bnd]['coords']      = np.zeros((len(pli),2))
                # obtain indicies on CMEMS grid for all support points for all BND
                for ind, _ in enumerate(pli):
                    # we  assume perefctly rectangular, which is what the CMEMS grid is
                    # this means for every X value there is some corresponding constant Y
                    # and vice versa
                    Xind = np.argmin(np.abs(pli[ind,0] - XCM))
                    Yind = np.argmin(np.abs(pli[ind,1] - YCM))
                    Xdist = np.min(np.abs(pli[ind,0] - XCM))
                    Ydist = np.min(np.abs(pli[ind,1] - YCM))
                    if Xdist > 1.0 or Ydist > 1.0:
                        print('WARNING: closest CMEMS grid point more than 1 degree away from pli point %i on pli %s' %(ind, bnd))
                        print('ensure coordinates are lat/long')
                    boundaries[bnd]['CMEMS_index'][ind,:] = np.array([Xind, Yind])
                    boundaries[bnd]['coords'][ind,:] = np.array([pli[ind,0], pli[ind,1]])
                
        self.boundaries = boundaries

    def update_pli_loc(self, boundaries, bnd):
        """
        make sure location of pli is readable and return an array of that pli
        and the updated boundaries, assigned to the boundaries attribute
        Arguments:
            boundaries {[type]} -- [description]
            bnd {[type]} -- [description]
        """

        pli_loc_key = 'pli_loc'
        # assume absolute path to begin with
        try:
            pli = utils.read_pli(boundaries[bnd][pli_loc_key])
        except(FileNotFoundError):
            # could be local, so look in same folder as ext
            pli_dir = os.path.split(self.ext)[0]
            try:
                boundaries[bnd][pli_loc_key] = os.path.join(pli_dir, boundaries[bnd][pli_loc_key])
                pli = utils.read_pli(boundaries[bnd][pli_loc_key])
            except(FileNotFoundError):
                print('No absolute path to pli provided and pli not located in local folder. Please copy the pli to the local folder')
                raise

        return boundaries, pli

 
    def process_bc(self):
        """
        wrapper for writing a bc file
        """
        boundaries = self.boundaries

        for bnd in boundaries.keys():
            if boundaries[bnd]['type'] == 'waterlevelbnd':
                # waterlevel because an ocean boundary should be waterlevel
                for sub in self.subs:
                    if sub in usefor.keys():
                        self.write_bc_file(sub, bnd)
                    else:
                        print('WARNING: requested sub %s not in CMEMS dict, no boundary made!' % sub)


    def write_bc_file(self, sub, bnd):
        '''
        write the bc file for a single sub, calling preamble function and writing values at all depths for all times
        '''
        csub = usefor[sub] # csub is name of sub in CMEMS nomenclature
        full_data_list = self.data_list
        data_list = list()
        for part_sub in csub['substance']:
            data_list.append([file for file in full_data_list if part_sub in file])

        if len(data_list) == 0:
            print('ERROR: cannot continue with boundary creation, no data files found for this variable')
            print('variable = %s (called %s in CMEMS) skipped' % (sub, csub['substance']))

        else:
            with open(os.path.join(self.dir, '%s_%s.bc' % (sub, bnd)),'w') as bcfile:

                print('substance: %s' % sub)
                print('reading data...')

                # get depths from first file rather than from every file
                # this is necessary to write preamble
                times, depths, data, fill = self.read_nc_data(data_list, bnd, csub)

                print('finished reading data')
                print('writing file...')

                # for every position, go through all the data files and read data
                val_save = np.empty([len(self.boundaries[bnd]['CMEMS_index']),len(times)])
                for position in range(0, len(self.boundaries[bnd]['CMEMS_index'])):

                    self.write_bc_preamble(bcfile, bnd, position, sub, depths)

                    for tind, tt in enumerate(times):
                        tdiff = tt - self.tref
                        # to minutes
                        bcfile.write(str((tdiff.seconds / 60) + (tdiff.days * 1440)))
                        bcfile.write('  ')
                        # find valid fill value in selected water column, dependent on parameter and depth
                        valid = {}
                        for part_sub in csub['substance']:
                            valid[part_sub] = self.find_valid_value(data, part_sub, csub, tind, position)

                        # FLIP THE ARRAY?
                        #for dind, _ in enumerate(depths):
                        for dind, _ in reversed(list(enumerate(depths))):
                            for part_sub in csub['substance']:
                                try:
                                    val = data[part_sub][tind, dind, position]
                                except(IndexError):
                                    # steric
                                    val = data[part_sub][tind, position]

                                if val == float(self.fill[part_sub]) or np.isnan(val):
                                    val = valid[part_sub]
                                else:
                                    valid[part_sub] = val

                                bcfile.write('%.4e' % (val * csub['conversion']))
                                bcfile.write('  ')
                                
                        if sub == 'steric':
                            val_save[position, tind] = val * csub['conversion']
                                
                        bcfile.write('\n')
                print('finished writing %s boundary for position %i/%i in boundary %s' % (sub, position+1, len(self.boundaries[bnd]['CMEMS_index']), bnd))
                gc.collect()
        if sub == 'steric':
            with open(os.path.join(self.dir, '%s_timeAveraged_%s.bc' % (sub, bnd)),'w') as bcfile:

                print('substance: %s_timeAveraged' % sub)
                print('time-averaging steric data...')
                
                for position in range(0, len(self.boundaries[bnd]['CMEMS_index'])):
                
                    val = np.mean(val_save[position,:])

                    self.write_bc_preamble(bcfile, bnd, position, sub, depths)
                    
                    bcfile.write(str(0))
                    bcfile.write('  ')
                    bcfile.write('%.4e' % (val))
                    bcfile.write('  ')
                    bcfile.write('\n')
                    bcfile.write(str(10000000))
                    bcfile.write('  ')
                    bcfile.write('%.4e' % (val))
                    bcfile.write('  ')
                    bcfile.write('\n')
                print('finished writing time-averaged %s boundary for position %i/%i in boundary %s' % (sub, position+1, len(self.boundaries[bnd]['CMEMS_index']), bnd))
                gc.collect()

    def read_nc_data(self, data_list, bnd, csub):
        '''
        reads each file belonging to a substance one by one, storing the data per position in a tensor
        this will be returned so it can be writen to a file
        The strategy tries to reduce the number of total times nc file handles are switched
        the alternative strategy was to do the writing point by point, meaning each nc file would be 
        read as many times as there are support points. Now they are only read once each, with the
        data being stored for later use.
        '''

        all_times, depths, fill = self.get_sub_shared_data(data_list, csub)
        meta = {'depths' : depths, 'times': all_times}
        data = {}

        # allocate array
        for part_sub in csub['substance']:
            if len(meta['depths']) > 1:
                # if 3D
                data[part_sub] = np.zeros((len(meta['times']), len(meta['depths']), len(self.boundaries[bnd]['CMEMS_index'])))
            else:
                # if 2D
                data[part_sub] = np.zeros((len(meta['times']), len(self.boundaries[bnd]['CMEMS_index'])))

        # for each constituent/part sub making up this substance
        for part_sub_i, part_sub in enumerate(csub['substance']):
            for file_index, data_file in enumerate(data_list[part_sub_i]):
                print('reading data file ' + os.path.split(data_file)[1])
                ds = nc.Dataset(data_file, 'r')
                # these are times local to only this file
                # these are needed to determine the location in the all array for the data to be inserted
                #times = np.array([datetime.datetime(1950,1,1,0,0,0) + datetime.timedelta(hours = int(tt)) for tt in ds.variables['time'][:]])
                time_var = ds.variables['time']
                times = nc.num2date(time_var[:],units=time_var.units,only_use_cftime_datetimes=False)

                if self.simultaneous and self.interp:
                    # interpolate all points accross all data
                    st = datetime.datetime.now()

                    # find index in times array that this subsection of time best matches and insert data in that slice later
                    t_index = np.argmin(abs(meta['times'] - times[0]))
                    # TIME, DEPTH, LAT, LONG
                    # interpolate all locations at the same time
                    # we feed in depths and times to reducing read frequency
                    arr = self.get_interp_array_multiple(ds, part_sub, bnd, times, depths)
                    arr = arr.squeeze()

                    if len(meta['depths']) > 1:
                        data[part_sub][t_index:t_index+len(times), :, :] = arr
                    else:
                        # steric
                        data[part_sub][t_index:t_index+len(times), :] = arr

                    et = datetime.datetime.now()
                    print(part_sub + ' multiple interpolation took ' + str((et - st).seconds) + ' seconds on time chunk ' + str(file_index + 1) + '/' + str(len(data_list[part_sub_i])))
                
                elif self.simultaneous and not self.interp:
                    print('ERROR: Cannot be simultaneous interpolation without interpolation option turned on')
                    raise

                else:
                    # interpolate point by point using subset of neighbours
                    for position in range(0, len(self.boundaries[bnd]['CMEMS_index'])):
                        st = datetime.datetime.now()
                        # find index in times array that this subsection of time best matches and insert data in that slice later
                        t_index = np.argmin(abs(meta['times'] - times[0]))
                        # TIME, DEPTH, LAT, LONG
                        if self.interp:
                            arr = self.get_interp_array(ds, part_sub, bnd, position, times, depths)
                        else:
                            arr = self.get_nearest_array(ds, part_sub, bnd, position, depths)
                        arr = arr.squeeze()

                        if len(meta['depths']) > 1:
                            data[part_sub][t_index:t_index+len(times), :, position] = arr
                        else:
                            # steric
                            data[part_sub][t_index:t_index+len(times), position] = arr                          
                        
                        et = datetime.datetime.now()
                        print(part_sub + ' position ' + str(position) + ' read took ' + str((et - st).seconds) + ' seconds on time chunk ' + str(file_index + 1) + '/' + str(len(data_list[part_sub_i])))

        return meta['times'], depths, data, fill

    def get_sub_shared_data(self, data_list, csub):
        '''
        look through all of a substance's files and make a time and depth array
        '''
        times = np.array([])
        
        # first get all times and the depth, where the associated data will be filled incrementally
        for file_index, data_file in enumerate(data_list[0]):
            ds = nc.Dataset(data_file, 'r')
            if file_index == 0:
                try:
                    depths = ds.variables['depth'][:]
                except:
                    # 2D file
                    depths = [0]
            time_var = ds.variables['time']
            #file_time = ds.variables['time'][:]
            file_time = nc.num2date(time_var[:],units=time_var.units,only_use_cftime_datetimes=False)
            times = np.concatenate((times, file_time))
        try:
            fill = ds.variables[csub['substance'][0]]._FillValue 
            # assign same fill value
            for part_sub in range(0, len(csub['substance'])):
                self.fill[csub['substance'][part_sub]] = float(fill)

        except(UnboundLocalError):
            print('ERROR: critical lack of files!')
            raise
        times = np.array(times)
        # not sure what order the times will be in, so we sort them
        times.sort()
        # 1950 01 01 is the reference time for CMEMS
        # this is times across all files, used to pre_allocate array
        #times = np.array([datetime.datetime(1950,1,1,0,0,0) + datetime.timedelta(hours = int(tt)) for tt in times])

        return times, depths, fill


    def get_nearest_array(self, ds, part_sub, bnd, position, depths):
        '''
        nearest neighbour interpolation using pre-calculated indices
        indices could lead you onto land
        '''
        
        #top_map = ds.variables[part_sub][0, 0, :, :]
        #top_map.mask = False
        if len(depths) > 1:
            arr = ds.variables[part_sub][:, :, int(self.boundaries[bnd]['CMEMS_index'][position,1]), int(self.boundaries[bnd]['CMEMS_index'][position,0])]
            arr = self.clean_array(arr, part_sub)
           
        else:
            arr = ds.variables[part_sub][:, int(self.boundaries[bnd]['CMEMS_index'][position,1]), int(self.boundaries[bnd]['CMEMS_index'][position,0])]
            arr = self.clean_array(arr, part_sub)

        return arr

        
    def get_interp_array(self, ds, sub, bnd, position, times, depths):
        """        
        returns array interpolated from local selection of data
        
        Arguments:
            ds {netCDF4.Dataset} -- Dataset of data file to be interpolated
            sub {str} -- CMEMS style sub name
            bnd {str} -- boundary name
            position {int} -- position in pli
            times {np.array(pd.Timestamp)} -- pandas timestamp array
            depths {np.array()} -- array of CMEMS depths            
        """

        xind = int(self.boundaries[bnd]['CMEMS_index'][position, 0])
        xi = self.boundaries[bnd]['coords'][position, 0]
        yind = int(self.boundaries[bnd]['CMEMS_index'][position, 1])
        yi = self.boundaries[bnd]['coords'][position, 1]

        search = self.search
        # vectorize query points
        # TIME, DEPTH, LAT, LON
        # order C flattening
        ind = 0
        # make integers of times
        times = [ii for ii, jj in enumerate(times)]
        if len(depths) > 1:
            xii = np.zeros((len(depths) * len(times), 4))
            for tt in times:
                for dd in depths:
                    xii[ind,:] = [tt, dd, yi, xi]
                    ind += 1
        else:
            xii = np.zeros((len(times), 3))
            for tt in times:
                xii[ind,:] = [tt, yi, xi]
                ind += 1

        x = ds.variables['longitude'][xind-search:xind+search+1]
        y = ds.variables['latitude'][yind-search:yind+search+1]

        '''
        # TIME, DEPTH, LAT, LON
        take small section for the interpolation
        order of this being passed is the same order as you would say the dimensions
        this is because C reshapes will reshape backwards through the dimensions, which
        reflects what is happening below.
        nest from first down to last dimension   
        reshape (vectorize) the subsection of data for interpolation routine 
        '''
        if len(depths) > 1:
            # 3D
            try:
                arr_t = ds.variables[sub][:, :, yind-search:yind+search+1,  xind-search:xind+search+1]  
            except(IndexError):
                print('not enough buffer space between pli and data domain. Please increase size of data domain')
                print('resorting to nearest neigbour')
                arr_t = self.get_nearest_array(ds, sub, bnd, position, depths)
                return arr_t

            # to get caught later
            arr_t = self.clean_array(arr_t, sub)
            inter = RegularGridInterpolator((times, depths, y, x), arr_t)

        else:
            # steric
            try:
                arr_t = ds.variables[sub][:, yind-search:yind+search+1,  xind-search:xind+search+1]
            except(IndexError):
                print('not enough buffer space between pli and data domain. Please increase size of data domain')
                print('resorting to nearest neigbour')
                arr_t = self.get_nearest_array(ds, sub, bnd, position, depths)
                return arr_t

            arr_t = self.clean_array(arr_t, sub)
            inter = RegularGridInterpolator((times, y, x), arr_t)

        '''
        interpolate to single point in space from spatial subsection, old method
        V[V == 0] = np.nan
        arr = griddata(arrs, V, xi = xii.T )
        inter = LinearNDInterpolator(arrs, V, fill_value=np.nan, rescale=False)
        '''
        arr = inter(xii)
        '''
        reravel, it went times -> depths, so go back
        data must be returned in times, depth, position, where position is dim 1 for single position interpolation
        '''
        if len(depths) > 1:
            arr_t = arr.reshape(len(times), len(depths), -1)
        else:
            arr_t = arr.reshape(len(times), -1)

        if np.isnan(np.nanmean(arr)):
            '''
            if all data were nan, too close to the coast, so use nearest neighbour
            the returned shape will be as expected, so it is done after the reshape
            issue arises if not nan but fill
            '''
            arr_t = self.get_nearest_array(ds, sub, bnd, position, depths)

        return arr_t 
        

    def get_interp_array_multiple(self, ds, sub, bnd, times, depths, plot_chk = False):
        """
        returns array interpolated from all data to MULTIPLE points
        pros - only one interpolation step, no loop
        cons - done with much more memory
        
        Arguments:
            ds {netCDF4.Dataset} -- Dataset of data file to be interpolated
            sub {str} -- CMEMS style sub name
            bnd {str} -- boundary name
            position {int} -- position in pli
            times {np.array(pd.Timestamp)} -- pandas timestamp array
            depths {np.array()} -- array of CMEMS depths            
        """

        arr = []
        # make intergers of times
        times = [ii for ii, jj in enumerate(times)]

        xi = self.boundaries[bnd]['coords'][:, 0]
        yi = self.boundaries[bnd]['coords'][:, 1]

        # form query point xii
        ind = 0
        if len(depths) > 1:
            xii = np.zeros((len(depths) * len(times) * len(yi), 4))
            for tt in times:
                for dd in depths:
                    for pos, jj in enumerate(yi):
                        xii[ind,:] = [tt, dd, yi[pos], xi[pos]]
                        ind += 1
        else:
            xii = np.zeros((len(depths) * len(times) * len(yi), 3))
            for tt in times:
                for pos, jj in enumerate(yi):
                    xii[ind,:] = [tt, yi[pos], xi[pos]]
                    ind += 1
        
        x = ds.variables['longitude'][:]
        y = ds.variables['latitude'][:]
        
        #if len(depths) > 1:
        if len(np.shape(sub)) == 4:
            # 3D
            arr_t = ds.variables[sub][:, :, :, :]  
            arr_t = self.clean_array(arr_t, sub)
            
            # SCL 20200821: option to fill NaNs per layer with surrounding values (horizontal search)
            if False:
                for depth in range(0,arr_t.shape[1]):
                    if not np.isnan(np.nanmean(arr_t[0,depth,:,:])):
                        invalid = np.isnan(arr_t[0,depth,:,:])
                        ind = nd.distance_transform_edt(invalid, return_distances=False, return_indices=True)
                        for time in range(0,arr_t.shape[0]):
                            data = arr_t[time,depth,:,:]
                            data = data[tuple(ind)]
                            arr_t[time,depth,:,:] = data
            
            inter = RegularGridInterpolator((times, depths, y, x), arr_t, fill_value=np.nan)
            arr = inter(xii)
            '''
            reravel, 
            the query point was created times -> depths -> y -> x, 
            so a C reshape specifying the first 2 dimensions should
            cause each entry to vary in space (x, y)
            '''
            arr_t = arr.reshape(len(times), len(depths), -1)
            # check for nan and do nearest instead
            for position in range(0, arr_t.shape[-1]):
                if np.isnan(np.nanmean(arr_t[:, :, position])):
                    print('getting nearest array instead for position %i' % position)
                    arr_t[:, :, position] = self.get_nearest_array(ds, sub, bnd, position, depths)
        else:
            # steric
            arr_t = ds.variables[sub][:, :, :]
            arr_t = self.clean_array(arr_t, sub)


            inter = RegularGridInterpolator((times, y, x), arr_t, fill_value = np.nan)
            arr = inter(xii)
            # reravel, it went times -> depths, so go back
            arr_t = arr.reshape(len(times), -1)
            # check for nan and do nearest instead
            for position in range(0, arr_t.shape[-1]):
                # will not be nan but could be fill!!!!!
                if np.isnan(np.nanmean(arr_t[:, position])):
                    print('getting nearest array instead for position %i' % position)
                    arr_t[:, position] = self.get_nearest_array(ds, sub, bnd, position, depths)        

        return arr_t 


    def write_bc_preamble(self, handle, pli_name, support, sub, depth):
        '''
        write the header information for a bc file
        '''
        handle.write('[forcing]\n')
        handle.write('Name                            = %s_%s\n' % (pli_name.replace('.pli',''), utils.make_len(support+1, 4)))

        if sub != 'steric':
            handle.write('Function                        = t3D\n')
            handle.write('Time-interpolation              = linear\n')
            handle.write('Vertical position type          = zdatum\n')
            handle.write('Vertical position specification = ')
            for dep in np.flip(depth):
                # FLIP THE ARRAY?
                handle.write('-%.2f  ' % dep)
            handle.write('\n')
        else:
            handle.write('Function                        = timeseries\n')
            handle.write('Time-interpolation              = linear\n')       

        handle.write('Quantity                        = time\n')
        handle.write('Unit                            = MINUTES since %s\n' % utils.datetime_to_timestring(self.tref))

        if sub == 'uxuy':
            handle.write('Vector = uxuyadvectionvelocitybnd:ux,uy\n')

        if sub != 'steric':
            for dep in range(0, len(depth)):
                if sub in constituent_boundary_type.keys():

                    for part_sub_i, _ in enumerate(constituent_boundary_type[sub]['type']):
                        handle.write('Quantity                        = %s\n' % constituent_boundary_type[sub]['type'][part_sub_i])
                        handle.write('Unit                            = %s\n' % constituent_boundary_type[sub]['unit'])
                        handle.write('Vertical position               = %s\n' % str(dep + 1))
                else:
                    handle.write('Quantity                        = tracerbnd%s\n'%(sub))
                    handle.write('Unit                            = g/m3\n')
                    handle.write('Vertical position               = %s\n' % str(dep + 1))
        else:
            for part_sub_i, _ in enumerate(constituent_boundary_type[sub]['type']):
                handle.write('Quantity                        = %s\n' % constituent_boundary_type[sub]['type'][part_sub_i])
                handle.write('Unit                            = %s\n' % constituent_boundary_type[sub]['unit'])       
            

    def write_pli(self):
        """
        ADMINISTRATE ADDITIONAL PLI FILES AND ASSOCIATED NEW EXT
        """

        pli_loc_key = 'pli_loc'
        boundaries = self.boundaries

        for _, bnd in enumerate(boundaries.keys()):
            if 'waterlevelbnd' in boundaries[bnd]['type']:
                '''
                # do not write a unique pli, simply copy
                for sub in self.subs:
                    if sub in usefor.keys():
                        # create a pli for every substance based on this existing pli
                        with open(os.path.join(self.dir,'%s%s.pli' % (bnd,sub)) ,'w') as pli:
                            # copy the existing pli but put the substance in the name
                            with open(boundaries[bnd][pli_loc_key],'r') as bndFile:
                                lines = bndFile.readlines()
                                for line in lines:
                                    pli.write(line.replace(bnd, bnd + sub))  
    
                # copy the original boundary pli as well for the hydrodynamic model
                # file_name = boundaries[bnd][pli_loc_key][find_last(boundaries[bnd][pli_loc_key],'\\'):]
                '''
                file_name = os.path.split(boundaries[bnd][pli_loc_key])[1]
                try:
                    sh.copyfile(boundaries[bnd][pli_loc_key], os.path.join(self.dir, file_name))
                except(sh.SameFileError):
                    print('file ' + os.path.join(self.dir, file_name) + ' already exists, ignoring...')


    def write_new_ext_file(self):
        """
        WRITE NEW EXT FILE CONTAINING THE CONSTITUENT BOUNDARIES
        
        """
        boundaries = self.boundaries

        with open(self.ext,'r') as new_template:
            for _, bnd in enumerate(boundaries.keys()):
                with open(os.path.join(self.dir,'DFMWAQ_' + bnd + '_tmp.ext'),'w') as new_ext:
                    # copy old boundaries, should only be waterlevel
                    for line in new_template.readlines():
                        new_ext.write(line)
                    if 'waterlevelbnd' in boundaries[bnd]['type']:
                        new_ext.write('\n')
                        # if it is waterlevel then it was involved in the previous steps
                        for sub in self.subs:
                            if sub in usefor.keys():
                                if sub == 'steric' and not self.steric:
                                    pass
                                else:
                                    new_ext.write('[boundary]\n')
                                    if sub in constituent_boundary_type.keys():
                                        if sub != 'uxuy':
                                            new_ext.write('quantity=%s\n' % ','.join(constituent_boundary_type[sub]['type']).replace(',',''))
                                        else:
                                            # advection, inconsistent naming
                                            new_ext.write('quantity=uxuyadvectionvelocitybnd\n')
                                    else:
                                        new_ext.write('quantity=tracerbnd%s\n'%(sub))
                                                                    
                                    new_ext.write('locationfile=%s.pli\n' % (bnd))
                                    new_ext.write('forcingfile=%s_%s.bc\n' % (sub, bnd))
                                    new_ext.write('\n')


    def write_ini(self, grid):
        '''
        write initial conditions file
        Keyword Arguments:
            grid {[type]} -- [description] (default: {None})
        '''

        if isinstance(self.subs, str):
            if grid is not None:
                # initials go in old style file
                grd = nc.Dataset(grid)
                try:
                    x_min = np.min(grd.variables['mesh2d_node_x'][:])
                    x_max = np.max(grd.variables['mesh2d_node_x'][:])
                    y_min = np.min(grd.variables['mesh2d_node_y'][:])
                    y_max = np.max(grd.variables['mesh2d_node_y'][:])

                    with open(self.dir + 'domain.pol','w') as pol:
                        pol.write('domain\n')
                        pol.write('4   2\n')
                        pol.write('%.4e    %.4e\n' % (x_min, y_min))
                        pol.write('%.4e    %.4e\n' % (x_min, y_max))
                        pol.write('%.4e    %.4e\n' % (x_max, y_max))
                        pol.write('%.4e    %.4e\n' % (x_max, y_min))

                    with open(self.dir + 'DFMWAQ_initials.ext','w') as old_ext:
                        for sub in self.subs:
                            old_ext.write('QUANTITY=initialtracer%s\n' % sub)
                            old_ext.write('FILENAME=domain.pol\n')
                            old_ext.write('FILETYPE=10\n')
                            old_ext.write('METHOD=4\n')
                            old_ext.write('OPERAND=O\n')
                            if sub in ini.keys():
                                old_ext.write('VALUE=%.4e\n' % ini[sub])
                            else:
                                old_ext.write('VALUE=0.0\n')
                            old_ext.write('\n')
                except:
                    print('only map4 style grids accepted')
                    print('domain polygon not written')
            else:
                print('Cannot make WAQ initials, no grid file passed')


    def merge_ext(self):
        '''
        write final ext file by merging temporary ones
        '''
        with open(os.path.join(self.dir,'DFMWAQ.ext'),'w') as new_ext:
            for tmp_ext in glob.glob(os.path.join(self.dir, '*_tmp.ext')):
                with open(tmp_ext, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        new_ext.write(line)
                new_ext.write('\n')
            os.remove(tmp_ext)
        for tmp_ext in glob.glob(os.path.join(self.dir, '*.ext')):
            if tmp_ext != os.path.join(self.dir, 'DFMWAQ.ext'):
                # remove tide only bnd
                os.remove(tmp_ext)


    def clean_array(self, arr, part_sub):
        arr.mask = False
        arr[arr == self.fill[part_sub]] = np.nan

        return arr


    def find_valid_value(self, data, part_sub, csub, tind, position):
        try:
            val = data[part_sub][tind, :, position]
            good_ind = np.sum(~np.isnan(val)) - 1
            
            if good_ind >= 0:
                valid = val[good_ind]
            else:
                valid = 0.0
        except(IndexError):
            # steric, no flip
            valid = 0.0

        return valid