'''
Tide

A class that can create an ext file and bc file for water level boundaries, including astronomic boundary conditions from FES
'''

import coastserv.models.utils as utils
import netCDF4 as nc
import glob
import scipy.interpolate
import numpy as np
import shutil as sh
import os

class Tide(object):

    def __init__(self, path, coords, pli, out):
        """
        Tide class
        
        Arguments:
            path {str} -- path to folder containin fes data
            coords {list} -- [xmin, xmax, ymin, ymax]
            pli {str} -- path to *.pli file
            out {path} -- path for output
        """
        
        self.path = path
        self.coords = coords
        self.out = out    

        self.const = ['2N2',   
            'MF'   , 
            'P1'   , 
            'M2'   , 'MKS2' , 'MU2'  , 'Q1'   , 'T2'  , 'J1'  , 'M3'  , 'MM'  ,  'N2'  ,  
            'R2'  ,  'K1'  ,  'M4'  ,  'MN4' ,  'S1'  ,  'K2'  ,  'M6'  , 'MS4' ,  'NU2' ,  
            'S2'  ,  'L2'  ,  'M8'  ,  'MSF' ,  'O1'  ,  'S4' ] 

        XY = utils.read_pli(pli)

        self.pli = pli
        self.X = XY[:,0]
        self.Y = XY[:,1]   

        self.check_coords()
       
        self.name = os.path.split(self.pli)[1][:utils.find_last(os.path.split(self.pli)[1],'.')-1]

        self.ext = os.path.join(self.out,'%s.ext' % self.name)

        try:
            self.representative = glob.glob(os.path.join(self.path, '*SLEV.nc'))[0]
        except(IndexError):
            print('ERROR: NO DATA FOUND IN FES PATH, NOT VALID TIDE OBJECT')
            self.representative = None
            raise
              

    def build_tide(self):
        if self.representative is not None:
            self.write_tide()
        else:
            print('ERROR: NO DATA FOUND IN FES PATH, NOT VALID TIDE OBJECT')


    def write_ext(self):
        with open(self.ext,'w') as ext:
            ext.write('[boundary]\n')
            ext.write('quantity=waterlevelbnd\n')
            ext.write('locationfile=%s\n' % os.path.split(self.pli)[1])
            ext.write('forcingfile=tide_%s.bc\n' % self.name)
            try:
                sh.copyfile(self.pli, os.path.join(self.out, os.path.split(self.pli)[1]))
            except():
                print('It appears the *.pli file already exists next to the *.ext file, skipping copy...')



    def write_tide(self):
        # check if file exists before remaking
        #if not os.path.exists(os.path.join(self.out,'tide_%s.bc' % self.name)):
            self.write_ext()
            self.interp_tide()

            with open( os.path.join(self.out,'tide_%s.bc' % self.name), 'w') as bnd:
                for ss in range(0,len(self.X)):
                    zz = utils.make_len(ss+1, 4)
                    bnd.write('[forcing]\n')
                    bnd.write('Name = %s_%s\n' % (self.name,zz))
                    bnd.write('Function = astronomic\n')
                    bnd.write('Quantity = astronomic component\n')
                    bnd.write('Unit = -\n')
                    bnd.write('Quantity = waterlevelbnd amplitude\n')
                    bnd.write('Unit = m\n')
                    bnd.write('Quantity = waterlevelbnd phase\n')
                    bnd.write('Unit = deg\n')
                    bnd.write('A0   0.0   0.0\n')
                    for co in range(0,len(self.const)):
                        bnd.write('%s   %f   %f\n' % (self.const[co], self.amp[ss,co] / 100, self.pha[ss,co]))
                    bnd.write('\n')


    def interp_tide(self, downsize = True):

        '''
        returns AMP, PHASE as attribute
        '''
        print('begin tide building')

        dat           = nc.Dataset(self.representative)
        
        LON          = dat['lon'][:]
        LON[LON>180] = LON[LON>180]-360 #wrapTo180
        LAT          = dat['lat'][:]
        
        # downsize dataset based on bounding box
        if downsize:
            x_min = np.argmin(abs(LON - self.coords[0]))
            x_max = np.argmin(abs(LON - self.coords[1]))
            y_min = np.argmin(abs(LAT - self.coords[2]))
            y_max = np.argmin(abs(LAT - self.coords[3]))
            
            if x_min > x_max:
                # goes through prime meridian
                LON = np.concatenate((LON[x_min:], LON[:x_max + 1]))
            else:
                # does not go through prime meridian
                LON = LON[x_min:x_max + 1]

            LAT = LAT[y_min:y_max + 1]
       
        AMPout = np.zeros((len(self.X), len(self.const)))
        PHAout = np.zeros((len(self.X), len(self.const)))

        ind = 0
        pos = np.zeros((len(LON) * len(LAT), 2))
        # order of this being passed is the same order as you would say the dimensions
        # this is because C reshapes will reshape backwards through the dimensions, which
        # reflects what is happening below.
        # nest from first down to last dimension 
        for jj in LAT:
            for ii in LON:
                pos[ind,:] = [ii, jj]
                ind += 1

        print('initiate constituent loop')

        for ii, c in enumerate(self.const):
            print('tidal constituent %s' % c)
            dat = nc.Dataset(os.path.join(self.path, '%s_FES2012_SLEV.nc' % c))
            if downsize:
                if x_min > x_max:
                    # goes through prime meridian
                    FES_amp = np.concatenate((dat.variables['Ha'][y_min:y_max+1,x_min:], dat.variables['Ha'][y_min:y_max+1, :x_max + 1]), axis = 1)
                    FES_pha = np.concatenate((dat.variables['Hg'][y_min:y_max+1,x_min:], dat.variables['Hg'][y_min:y_max+1, :x_max + 1]), axis = 1)                 
                else:
                    FES_amp = dat.variables['Ha'][y_min:y_max+1,x_min:x_max+1]
                    FES_pha = dat.variables['Hg'][y_min:y_max+1,x_min:x_max+1]
            else:    
                FES_amp = dat.variables['Ha'][:,:]
                FES_pha = dat.variables['Hg'][:,:]
            
            if len(FES_amp) == 0:
                print('ERROR: No data. Is xmin < xmax and ymin < ymax?')
                raise ValueError

            AMP_keep = FES_amp
            PHA_keep = FES_pha

            # produce masked versions of data to fill in gaps later using nearest neighbour
            # need to do this before changing mask to np.nan, a step that is necessary to indicate missing after interpolation
            valid_pos = pos[AMP_keep.reshape(-1).mask == False]
            valid_amp = AMP_keep.reshape(-1)[AMP_keep.reshape(-1).mask == False]
            valid_pha = PHA_keep.reshape(-1)[PHA_keep.reshape(-1).mask == False] 
            valid_pha = valid_pha*2*np.pi/360
            realC = 1*np.cos(valid_pha) 
            imagC = 1*np.sin(valid_pha)            
            valid_pha = np.array(realC + 1j * imagC)                 
            #

            FES_amp[FES_amp.mask == True] = np.nan
            FES_pha[FES_pha.mask == True] = np.nan

            # translate to radians
            FES_pha = FES_pha*2*np.pi/360
            FES_pha_real = FES_pha
            realC = 1*np.cos(FES_pha) 
            imagC = 1*np.sin(FES_pha)

            # combine these to a single imaginary number
            
            FES_pha = np.array(realC + 1j * imagC)

            # Interp amplitudes and phases to locations 
            print('first interpolation')

            amp = scipy.interpolate.griddata(pos, np.reshape(FES_amp, newshape = (-1,1)), np.transpose(np.array([self.X, self.Y])), fill_value = np.nan)
            pha = scipy.interpolate.griddata(pos, np.reshape(FES_pha, newshape = (-1,1)), np.transpose(np.array([self.X, self.Y])), fill_value = np.nan)
            pha_real = scipy.interpolate.griddata(pos, np.reshape(FES_pha_real, newshape = (-1,1)), np.transpose(np.array([self.X, self.Y])), fill_value = np.nan)
            
            # will not return nan in imaginary interpolation, so find index where it would go wrong
            
            pha[np.isnan(pha_real)] = np.nan

            # method of checking plausibility of interpolation
            # plt.scatter(pos[:,0], pos[:,1], c = np.angle(FES_pha.reshape(-1)), vmin = -10, vmax = 10)
            # plt.scatter(X, Y, c = pha.reshape(-1), vmin = -10, vmax = 10)
            # plt.colorbar()

            # for reference, this method is very slow
            # inter = scipy.interpolate.interp2d(pos[:,0], pos[:,1], np.reshape(FES_amp, newshape = (-1,1)))   
            # amp = inter(X, Y)

            # As no extrapolation was performed, a natural neighbor
            # interpolation is needed to fill some gaps in FES_amp/FES_pha.
            # fill missing values

            if sum(np.isnan(amp)) > 0:
                print('second interpolation needed to fill the gaps')

                #print(np.transpose(np.array([self.X.reshape(-1,1)[np.isnan(amp)], self.Y.reshape(-1,1)[np.isnan(amp)]])))
                try:
                    xi = np.transpose(np.array([self.X.reshape(-1,1)[np.isnan(amp)], self.Y.reshape(-1,1)[np.isnan(amp)]]))
                    amp[np.isnan(amp)] = scipy.interpolate.griddata(valid_pos, valid_amp, xi, fill_value = np.nan, method = 'nearest')
                    pha[np.isnan(pha)] = scipy.interpolate.griddata(valid_pos, valid_pha, xi, fill_value = np.nan, method = 'nearest')
                except ValueError:
                    print('ERROR: Mismatch between area in coords array and locations in pli')
                    raise
                    
            pha = np.angle(pha) * 360 / (2 * np.pi)

            AMPout[:,ii] = amp.ravel()
            PHAout[:,ii] = pha.ravel()
        
        self.amp = AMPout
        self.pha = PHAout


    def check_coords(self):
        '''
        verify consistency of pli and coords
        '''

        try:
            assert(isinstance(self.X[0], float))
            assert(isinstance(self.Y[0], float))
        except:
            print('ERROR: pli file is not formatted correctly')
            raise(ValueError)   

        try:
            assert(np.min(self.X) > self.coords[0])
            assert(np.max(self.X) < self.coords[1])
            assert(np.min(self.Y) > self.coords[2])
            assert(np.max(self.Y) < self.coords[3])
        except:
            print('ERROR: pli does not reside within the bounding box')
            raise(ValueError)  
