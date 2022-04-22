from dfm_tools.get_nc import get_netdata, get_ncmodeldata
from dfm_tools.get_nc_helpers import get_ncvardimlist
from dfm_tools.regulargrid import scatter_to_regulargrid

import argparse
import os
import numpy as np
from netCDF4 import Dataset
import time as tm


"""original model located at
    p:\11202428-hisea\03-Model\Greece_model\waq_model\
"""

def regularGrid_to_netcdf(fp_in, nx, ny, treg, lreg):
    #dir_output = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','output'))
    #dir_output = os.getcwd() + '\data\output'
    dir_output = '/data/output'
    if not os.path.exists(dir_output):
        os.makedirs(dir_output)
    print(dir_output)
    file_nc = fp_in
    input_nc = Dataset(file_nc, 'r', format='NetCDF4')
    time_old = input_nc.variables['time'][:]
    if treg != 'all':
        time_old = np.take(time_old, treg)

    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)


    df = vars_pd

    key_values = ['mesh2d_tem1','time', 'mesh2d_s1', 'mesh2d_ucx', 'mesh2d_ucy', 'mesh2d_tem1', 'mesh2d_sa1', 'mesh2d_water_quality_output_17', 'mesh2d_OXY', 'mesh2d_face_x', 'mesh2d_face_y', 'mesh2d_layer_z']

    df = df.loc[df['nc_varkeys'].isin(key_values)]

    """
    ####################################################################################################################
    #   Regularise all files with 3 dimensions (time, nFaces, layers). 
    #   This will be equal to four dimensions in the regular grid format since nFaces is the x- and y- dimension.
    ####################################################################################################################
    """
    df2 = df.loc[df['ndims'] == 3]

    data_frommap_x = get_ncmodeldata(file_nc=file_nc, varname='mesh2d_face_x')
    data_frommap_y = get_ncmodeldata(file_nc=file_nc, varname='mesh2d_face_y')
    data_frommap_z = get_ncmodeldata(file_nc=file_nc, varname='mesh2d_layer_z', layer='all')
    time = get_ncmodeldata(file_nc=file_nc, varname='time', timestep=treg)
    outname = '%s_regular.nc' % os.path.split(fileNC)[1][0:-3]
    file_nc_reg = os.path.join(dir_output, outname)
    root_grp = Dataset(file_nc_reg, 'w', format='NETCDF4')
    root_grp.description = 'Example simulation data'
    first_read = True
    i = 0
    for index, row in df2.iterrows():
        print(row['nc_varkeys'])
        if row['dimensions'][1] == 'mesh2d_nEdges':
            continue
        data_frommap_var = get_ncmodeldata(file_nc=file_nc, varname=row['nc_varkeys'], timestep=treg, layer=lreg)
        data_frommap_var = data_frommap_var.filled(np.nan)
        field_array = np.empty((data_frommap_var.shape[0], ny, nx, data_frommap_var.shape[-1]))
        tms = data_frommap_var.shape[0]
        lrs = data_frommap_var.shape[-1]
        trange = range(0, tms)
        lrange = range(0, lrs)
        
        cell_size_x = (data_frommap_x.max() - data_frommap_x.min()) / nx
        cell_size_y = (data_frommap_x.max() - data_frommap_x.min()) / nx
        print('Cell size x: ' + str(cell_size_x))
        print('Cell size y: ' + str(cell_size_y))
        
        A = np.empty((tms, lrs))
        A = np.array([scatter_to_regulargrid(xcoords=data_frommap_x, ycoords=data_frommap_y, ncellx=nx, ncelly=ny,
                                              values=data_frommap_var[t, :, l].flatten(), method= 'nearest', maskland_dist=0.01) for t in
                      trange for l in lrange])
  
        x_grid = A[0][0]
        y_grid = A[0][1]
        A = A[:, 2, :, :]
        A = np.moveaxis(A, [0], [2])
        subs = np.split(A, tms, axis=2)

        field_array[:, :, :, 0:lrs] = [subs[tn] for tn in trange]
        field_array = np.ma.masked_invalid(field_array)
        field_array = field_array.filled(-999.)

        print('done with variable %s' % row['nc_varkeys'])

        if first_read:
            unout = 'seconds since 2015-01-01 00:00:00'
            lon = x_grid[0, :]
            lat = y_grid[:, 0]
            # create dimensions
            root_grp.createDimension('time', None)
            root_grp.createDimension('lon', lon.shape[0])
            root_grp.createDimension('lat', lat.shape[0])
            root_grp.createDimension('layer', lrs)
            lonvar = root_grp.createVariable('lon', 'float32', 'lon')
            lonvar.setncattr('axis', 'X')
            lonvar.setncattr('reference', 'geographical coordinates, WGS84 projection')
            lonvar.setncattr('units', 'degrees_east')
            lonvar.setncattr('_CoordinateAxisType', 'Lon')
            lonvar.setncattr('long_name', 'longitude')
            lonvar.setncattr('valid_max', '180')
            lonvar.setncattr('valid_min', '-180')
            lonvar[:] = lon

            latvar = root_grp.createVariable('lat', 'float32', 'lat')
            latvar.setncattr('axis', 'Y')
            latvar.setncattr('reference', 'geographical coordinates, WGS84 projection')
            latvar.setncattr('units', 'degrees_north')
            latvar.setncattr('_CoordinateAxisType', 'Lat')
            latvar.setncattr('long_name', 'latitude')
            latvar.setncattr('valid_max', '90')
            latvar.setncattr('valid_min', '-90')
            latvar[:] = lat

            layervar = root_grp.createVariable('layer', 'float32', 'layer')
            layervar.setncattr('axis', 'Z')
            layervar.setncattr('reference', 'geographical coordinates, WGS84 projection')
            layervar.setncattr('units', 'm')
            layervar.setncattr('_CoordinateZisPositive', 'down')
            layervar.setncattr('_CoordinateAxisType', 'Height')
            layervar.setncattr('long_name', 'Depth')

            layervar[:] = data_frommap_z[lreg]

            timevar = root_grp.createVariable('time', 'float64', 'time')
            timevar.setncattr('units', unout)
            timevar.setncattr('calendar', 'standard')
            timevar.setncattr('long_name', 'time')
            timevar.setncattr('_CoordinateAxisType', 'Time')


            timevar[:] = time_old

        fieldName = row['nc_varkeys']
        fieldvar = root_grp.createVariable(fieldName, 'float64', ('time', 'lat', 'lon', 'layer'), fill_value=-999.)
        key = fieldName
        for ncattr in input_nc.variables[key].ncattrs():
            if ncattr != "_FillValue":
                root_grp.variables[fieldName].setncattr(ncattr, input_nc.variables[key].getncattr(ncattr))


        fieldvar[:] = field_array
        first_read = False
        i += 1


    """
    ####################################################################################################################
    #   Regularise all files with 2 dimensions (time, nFaces, layers).
    #   This will be equal to 3 dimensions in the regular grid format since nFaces is the x- and y- dimension.
    ####################################################################################################################
    """
    print('STARTING 2D')
    df2 = df.loc[df['ndims'] == 2]

    excludeList = ['edge', 'face', 'x', 'y']
    for index, row in df2.iterrows():
        test = any(n in str(row['nc_varkeys']) for n in excludeList)
        if not test:
            if row['dimensions'][1] == 'mesh2d_nEdges':
                continue
            ntimes = row['shape'][0]
            data_frommap_var = get_ncmodeldata(file_nc=file_nc, varname=row['nc_varkeys'], timestep=treg)
            data_frommap_var = data_frommap_var.filled(np.nan)
            field_array = np.empty((data_frommap_var.shape[0], ny, nx))
            trange = range(0, data_frommap_var.shape[0])
            tms = data_frommap_var.shape[0]
            A = np.array([scatter_to_regulargrid(xcoords=data_frommap_x, ycoords=data_frommap_y, ncellx=nx, ncelly=ny,
                                                 values=data_frommap_var[t, :].flatten(), method='nearest', maskland_dist=0.01) for t in
                          trange])

            A = A[:, 2, :, :]
            field_array[:, :, :] = A
            field_array = np.ma.masked_invalid(field_array)
            field_array = field_array.filled(-999.)
            """write data to new netcdf"""
            fieldName = row['nc_varkeys']
            fieldvar = root_grp.createVariable(fieldName, 'float32', ('time', 'lat', 'lon'), fill_value=-999)
            key = fieldName
            for ncattr in input_nc.variables[key].ncattrs():
                if ncattr != "_FillValue":
                    root_grp.variables[fieldName].setncattr(ncattr, input_nc.variables[key].getncattr(ncattr))
            fieldvar[:] = field_array
    root_grp.close()


if __name__ == '__main__':

    # Setup CMD
    parser = argparse.ArgumentParser(
        description='Write FM output to regulargrid.')
    parser.add_argument('mapfile', type=str, nargs=1, help='0th partition of your NetCDF map output')
    parser.add_argument('xpoints', type=int, nargs=1, help='number of points you wish to include into your regular grid')
    parser.add_argument('ypoints', type=int, nargs=1, help='number of points you wish to include into your regular grid')

    args = parser.parse_args()

    time_start = tm.time()
    """change line below to where your DFlowFM output directory is located"""
    # dir_input = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'input', 'DFM_OUTPUT_tttz_waq'))
    dir_input = '/data/input'
    #mapfile='tttz_waq_0000_map.nc'
    """change line below to the name of the 0th partition of your NetCDF map output"""
    

    fileNC = os.path.join(dir_input, args.mapfile[0])
    #fileNC = os.path.join(dir_input, mapfile)
   
    """change xpts and ypts to the number of points you wish to include into your regular grid. Also specify the times you wish to 
    include and the layers """
    xpts = args.xpoints[0]
    ypts = args.ypoints[0]
    """times and layers can also be specified by
    tms = np.arange(40,44,2)
    lrs = [0,10,20,30,46]
    """
    tms = 'all'
    #lrs = 'all'
    #tms = np.arange(40,44,2)
    lrs = [46]
    """
    fileNC : string, is the path to the 0'th partition of the DFlowFM map file output
    xpts : integer, is the number of points in the x-direction (longitude) you wish to interpolate to. The points are evenly spaced.
    ypts : integer, is the number of points in the y-direction (latitude) you wish to interpolate to. The points are evenly spaced.
    tms : numpy array or 'all', an array of times you want to do the interpolation for
    lrs : numpy array, 'all', or integer. The number of layers you wish to include. The script detect if there are layers or not. 
    """

    regularGrid_to_netcdf(fileNC, xpts, ypts, tms, lrs)
    time_elapsed = tm.time() - time_start
    print('Duration: %f s' %time_elapsed) #check how much time the script needs to run.

"""if all else fails: pip install joke-generator"""