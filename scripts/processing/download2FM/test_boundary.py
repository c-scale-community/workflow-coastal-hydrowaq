from coastserv.models.boundary import Boundary
import datetime
import os

path_out = os.path.join('/app','data', 'out')
path_in = os.path.join('/app','data', 'in')
ext_fn = [f for f in os.listdir(path_out) if f.endswith('.ext')][0]
ext = os.path.join(path_out, ext_fn)
data_list = os.path.join(path_in, 'data','*.nc')
# sub = ['salinity', 'temperature', 'uxuy', 'steric']
sub = ['Opal', 'PON1', 'POP1', 'POC1', 'OXY', 'NO3', 'PO4', 'salinity', 'temperature', 'uxuy', 'steric', 'Green', 'Diat', 'Si']
#'Opal', 'PO4', 'PON1', 'POP1', 'POC1', 'NO3',
#, 'Si', 'PON1', 'POP1', 'POC1', 'Green', 'Diat', 'salinity', 'temperature', 'uxuy', 'steric']


opt_path = os.path.join(path_in, 'options_physbio.txt')
with open(opt_path) as f:
    lines = f.readlines()
    for line in lines:
        li = line.strip()
        if not li.startswith("#"):
            if li.startswith('interp'):
                interpval = li.strip().split('=')[-1].strip()
            if li.startswith('simultaneous'):
                simval = li.strip().split('=')[-1].strip()
            if li.startswith('steric'):
                stericval = li.strip().split('=')[-1].strip()
            if li.startswith('tref'):
                trefval = li.strip().split('=')[-1].strip()
                tref_list = [int(c) for c in trefval.strip().split(',')]
tref = datetime.datetime(tref_list[0], tref_list[1], tref_list[2], tref_list[3], tref_list[4], tref_list[5])

test = Boundary(ext, data_list, sub, tref, path_out)
print('running with options interp = %s, simultaneous = %s, steric = %s' %(interpval, simval, stericval))
test.build_boundary(interp=interpval, simultaneous=simval, steric=stericval)
print('running with options interp = %s, simultaneous = %s, steric = %s' %(interpval, simval, stericval))
