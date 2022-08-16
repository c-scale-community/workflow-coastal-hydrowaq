# -*- coding: utf-8 -*-
"""
Read, write and process ERA-interim maps

Author: M.Verlaan Modified by Wilms (fine.wilms@deltares.nl)
"""

import numpy as np
from netCDF4 import Dataset
import os
import os.path
from datetime import datetime, timedelta


class EraMaps:
    'Utility for reading and processing era-interim map output.'
    
    def __init__(self,filename,formatuser,readOrWrite='r'):#format='NETCDF3_CLASSIC'):
        '''create a new object matching one era-interim map file, ie one netcdf'''
        self._filename=filename

        self._ds=Dataset(filename,readOrWrite,format=formatuser) #_ds should not be accessed directly


    def getRelativeTimes(self):
        'provide map times as numpy array in seconds since reftime'
        if self._ds.variables.__contains__('time'):
            temp=self._ds.variables['time']
        else:
            raise NameError('No variable named time found in '+self._filename)
        print('in get RelativeTimes')
        return temp[:]

    
    def getReferenceTime(self):
        'provide map times as numpy array in seconds since reftime'
        if self._ds.variables.__contains__('time'):
            temp=self._ds.variables['time']
        else:
            raise NameError('No variable named time found in '+self._filename)
        tstr=temp.getncattr('units')
        refdate=tstr[tstr.find('since')+len('since')+1:]
        reftime=datetime.strptime(refdate,'%Y-%m-%d %H:%M:%S')
        print('in getReferenceTime')
        return reftime
    

    def setRelativeTimes(self,times,istart=0):
        'set map times as numpy array in seconds since reftime'
        if self._ds.variables.__contains__('time'):
            temp=self._ds.variables['time']
        else:
            raise NameError('No variable named time found in '+self._filename)
        temp[istart:istart+len(times)]=times
        
    def setNewRelativeTimes(self,newref,times,oldref,istart):
        'fill in map times with given reference date, from istart.change attribute reference time if needed'
        if self._ds.variables.__contains__('time'):
            temp=self._ds.variables['time']            
        else:
            raise NameError('No variable named time found in '+self._filename)
        
        #newref in datenum format
#        tstr=temp.getncattr('units')
#        tunits=tstr[0:tstr.find('since')-1]
        
        
#        if tunits=='seconds':
#            tabs=[oldref + timedelta(seconds=i) for i in times]
#            trel=[(ti-newref).total_seconds() for ti in tabs]

#        elif tunits=='hours':
        tabs=[oldref + timedelta(hours=i) for i in times]
        trel=[(ti-newref).total_seconds()/3600 for ti in tabs]
        
        #see if we need to change reftime
        tstr=temp.getncattr('units')
        refdate=tstr[tstr.find('since')+len('since')+1:]
        reftime=datetime.strptime(refdate,'%Y-%m-%d %H:%M:%S')
        
        if not reftime==newref:
            newstr= "hours since %s" %(datetime.strftime(newref,'%Y-%m-%d %H:%M:%S'))
            temp.setncattr('units',newstr)     
        
        temp[istart:istart+len(times)]=trel

    def getVar(self, timeIndex, var_name):
        if self._ds.variables.__contains__(var_name):
            temp = self._ds.variables[var_name]
        else:
            raise NameError('No variable named %s found in ' % var_name + self._filename)

        if timeIndex == -1:
            return temp[:, :, :]
        else:
            return temp[timeIndex, :, :]

    def setVar(self,timeIndex,values,new_name):
        if self._ds.variables.__contains__(new_name):
            temp=self._ds.variables[new_name]
        else:
            raise NameError('No variable named %s found in %s'%(new_name,self._filename))
        if timeIndex==-1:
            temp[:,:,:]=values[:,:,:]
        else:
            temp[timeIndex,:,:]=values[:,:]

    def getX(self):
        'get x-coordinates, ie longitudes  as numpy array for one time'
        if self._ds.variables.__contains__('longitude'):
            temp=self._ds.variables['longitude']
        else:
            raise NameError('No variable named longitude found in '+self._filename)
        return temp[:]

    def getY(self):
        'get y-coordinates, ie latitudes as numpy array for one time'
        if self._ds.variables.__contains__('latitude'):
            temp=self._ds.variables['latitude']
        else:
            raise NameError('No variable named latitude found in '+self._filename)
        return temp[:]
  
    def getDim(self,dim_name):
        'Read a netcdf dimension by name'
        if self._ds.dimensions.__contains__(dim_name):
            temp=self._ds.dimensions[dim_name]
        else:
            raise NameError('No dimension named %s found in '%dim_name +self._filename)
        return temp
        
    def createDim(self,dim_name,value):
        'Create a new dimension in the netcdf file. Use None for unlimited dims'
        dim=self._ds.createDimension(dim_name,value)
        return dim
        
    def getVariableType(self,variable_name):
        'Get variable type'
        if self._ds.variables.__contains__(variable_name):
            temp=self._ds.variables[variable_name]
        else:
            raise NameError('No variable named %s found in '%variable_name +self._filename)
        return temp.dtype.str

    def copyVariableFrom(self,src,var_name,new_name='',copy_data_flag=1):
        'copy one variable from another netcdf'
        if len(new_name)==0:
            new_name=var_name
        if not repr(src).startswith('EraMaps'):
            raise TypeError('The src argument must be a EraMaps instance')
        src_var=src._ds.variables[var_name]
        src_dims=src_var.dimensions
        src_type=src_var.dtype.str
#        print var_name+'='+'('+str(src_dims)+')'
        self._ds.createVariable(new_name,src_type,src_dims)
        dest_var=self._ds.variables[new_name]
        #copy global attributes
        for attr_name in src_var.ncattrs():
            print(attr_name,'=',src_var.getncattr(attr_name))
            if attr_name!='_FillValue':
                dest_var.setncattr(attr_name,src_var.getncattr(attr_name))
        #copy data
        if copy_data_flag==1:
            if len(src_dims)==1:
                dest_var[:]=src_var[:]
            elif len(src_dims)==2:
                dest_var[:,:]=src_var[:,:]
            elif len(src_dims)==3:
                dest_var[:,:,:]=src_var[:,:,:]
            elif len(src_dims)==4:
                dest_var[:,:,:,:]=src_var[:,:,:,:]
            else:
                raise TypeError('Only ranks less than 5 are suppported.'+
                ' The following variable is causing trouble '+var_name)

    def copyVariableAttributesFrom(self,src,var_name,new_name=''):
        'copy atrributes of one variable from another netcdf'
        if len(new_name)==0:
            new_name=var_name
        if not repr(src).startswith('EraMaps'):
            raise TypeError('The src argument must be a EraMaps instance')
        src_var=src._ds.variables[var_name]


        dest_var=self._ds.variables[new_name]
        #copy variable attributes
        for attr_name in src_var.ncattrs():
            if attr_name!='_FillValue':
                print(attr_name,'=',src_var.getncattr(attr_name))
                dest_var.setncattr(attr_name,src_var.getncattr(attr_name))

    def createVariable(self,variable_name,variable_type,variable_dims=()):
        'Create a new variable'
        self._ds.createVariable(variable_name,variable_type,variable_dims)
        dest_var=self._ds.variables[variable_name]  
        return dest_var
        
    def createVariableAttribute(self,variable_name,attribute_name,value):
        'Create a new attribute for a variable'
        if not self._ds.variables.__contains__(variable_name):
            raise RuntimeError('Variable not found :'+variable_name)
        variable=self._ds.variables[variable_name]
        variable.setncattr(attribute_name,value)

        
    def close(self):
        'close the netcdf file'
        self._ds.close()
        self._ds=None #file is no longer accessible
        
    def __repr__(self):
        return 'EraMaps(\''+self._filename+'\')'
        


    def copyGlobalDataFrom(self,src,skipDims=[]):
        'Copy global attributes of era-interim map meta data from source dataset'
        if not repr(src).startswith('EraMaps'):
            raise TypeError('The src argument must be a EraMaps instance')
        #copy global attributes
        for attr_name in src._ds.ncattrs():
            print(attr_name,'=',src._ds.getncattr(attr_name))
            self._ds.setncattr(attr_name,src._ds.getncattr(attr_name))
        #copy dimensions
        for dim_name in src._ds.dimensions:
            print(dim_name,'=',src._ds.dimensions[dim_name])
            if not(dim_name in skipDims):
                temp=src._ds.dimensions[dim_name]
                if temp.isunlimited():
                    dim=self._ds.createDimension(dim_name,None)
                else:
                    dim=self._ds.createDimension(dim_name,len(temp))

        
if __name__ == "__main__": #run tests for this module
    maps=EraMaps('era_interim_201311.nc', 'r')
    t=maps.getRelativeTimes()
    if t.shape[0]!=249:
        print('Was expecting 249 times, but found',t.shape[0])
    print('times t[0:3]= ',t[0:3])
    p=maps.getPressure(3) #4th field counting from 0
    if p.shape[0]!=241:
        print('Was expecting 241 cells for pressure in y direction, but found',p.shape[0])
    if p.shape[1]!=480:
        print('Was expecting 480 cells for pressure in x direction, but found',p.shape[1])
    print('p[time=3,0:2,0:2] = ',p[0:2,0:2])
    x=maps.getX() 
    if x.shape[0]!=480:
        print('Was expecting 480 x coordinates, but found',x.shape[0])
    print('x[time=3,0:3] = ',x[0:3])
    y=maps.getY() 
    if y.shape[0]!=241:
        print('Was expecting 241 y-coordinates, but found',y.shape[0])
    print('y[time=3,0:3] = ',y[0:3])
    
    #start copying some data
    if os.path.isfile('test_era1.nc'):
        os.remove('test_era1.nc')

    dest=EraMaps('test_era1.nc','NETCDF4', 'w')

    dest.copyBasicsFrom(maps)
    dest
    
    #clean up
    dest.close()
    maps.close()
    

