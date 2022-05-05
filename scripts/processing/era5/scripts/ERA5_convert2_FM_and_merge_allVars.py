#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 18:18:03 2017

@author: irazoqui and modified by fine.wilms@deltares.nl

merge & convert to FM on the fly

wind = 0 offset + 0.01*wind_as_int
patm=100000 + 1*pressure_int
"""

import numpy as np
import os
import os.path
from era_maps_allVars import EraMaps
import click

"""dict[variable name as shown in era5 netcdf] = [standard name, offset, float]. 
If you need to add more parameter types, expand this dictionary."""
dict_stdNames = {}
dict_stdNames['d2m'] = ['2 metre dewpoint temperature', np.float(270.0), np.float(0.0002)]
dict_stdNames['t2m'] = ['2 metre temperature',np.float(275) , np.float(0.0003)]
dict_stdNames['tcc'] = ['Total cloud cover', np.float(0.5), np.float(0.000015)]
dict_stdNames['u10'] = ['eastward_wind', np.float(0), np.float(0.01)]
dict_stdNames['v10'] = ['northward_wind', np.float(0), np.float(0.01)]
dict_stdNames['msl'] = ['air_pressure', np.float(100000.0), np.float(1.0)]

@click.command()
@click.option('--input', required=True, type=str, help='Folder downloaded era5 data')
@click.option('--output', required=True, type=str, help='Folder with output')
def era5_fm(input, output):
    """
    Convert ERA5 data to FM input netcdf
    """
    path_in = input
    path_out = output


    filename_list = os.listdir(path_in)

    if not os.path.exists(path_out):
        os.makedirs(path_out)
    newfilename = os.path.abspath(os.path.join(path_out, 'era5_FM.nc'))

    #loop over files. we assume they are in the right order in time

    first=True
    tcount=0


    if os.path.isfile(newfilename):
        #raise RuntimeError('Output file already exists. Please remove and try again. File name is '+newfilename)
        os.remove(newfilename)
            
    for filename in filename_list:
        fp = os.path.abspath(os.path.join(path_in,filename))
        maps=EraMaps(fp,'r')
        times=maps.getRelativeTimes()
        print("Postprocessing " + filename)
        """create meta data once: this includes variable names, offsets, and scalings"""
        if first:
            dest=EraMaps(newfilename,'NETCDF4','w')
        
            dest.copyGlobalDataFrom(maps,skipDims=['longitude','time'])
            dest.copyVariableFrom(maps,'latitude')
            
            #create Dimesions and variables
            
            #longitude
            x=maps.getX()
            overlapright=(x>179) #overlap
            overlapleft=(x<-179) #overlap

            x_new=np.hstack((x[overlapright]-360,x,x[overlapleft]+360))
            nx=len(x_new)
            longitude_dim=dest.createDim('longitude',nx)
            longitude_type=maps.getVariableType('longitude')
            new_longitude=dest.createVariable('longitude',longitude_type,('longitude'))
            dest.copyVariableAttributesFrom(maps,'longitude')
            new_longitude[:]=x_new

            #time
            time_dim = dest.createDim('time',None)
            time_type=maps.getVariableType('time')
            new_time=dest.createVariable('time',time_type,('time'))
            dest.copyVariableAttributesFrom(maps,'time')
            dest.createVariableAttribute('time','standard_name','time')

            for var in dict_stdNames.keys():
                print(var)
                var_type=maps.getVariableType(var)
                dest.createVariable(var,var_type,('time','latitude','longitude'))
                dest.copyVariableAttributesFrom(maps,var)
                dest.createVariableAttribute(var,'standard_name',dict_stdNames[var][0])
                dest.createVariableAttribute(var,'coordinates','latitude longitude')
                dest.createVariableAttribute(var,'scale_factor',dict_stdNames[var][2])
                dest.createVariableAttribute(var,'add_offset',dict_stdNames[var][1])

            first=False

        """read data from netcdf once the scalings, offsets, types, and names have been assigned for each parameter"""
        ntimes=len(times)
        dest.setRelativeTimes(times,tcount)    
    
        for itime in np.arange(ntimes):
            for key in dict_stdNames.keys():
                var = maps.getVar(itime, key)
                new_var = np.hstack((var[:, overlapright], var[:, :], var[:, overlapleft]))
                dest.setVar(tcount, new_var, key)
            tcount+=1
                

        maps.close()
    dest.close()

if __name__ == '__main__':
    era5_fm()


# docker run -it -v ~/data/hisea/download/:/data/input -v ~/data/hisea/era5:/data/output --entrypoint /bin/bash era5_fm
# python ERA5_convert2_FM_and_merge_allVars.py --input /data/input --output /data/output
