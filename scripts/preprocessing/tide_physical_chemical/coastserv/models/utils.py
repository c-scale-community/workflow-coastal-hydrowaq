'''
@schueder July 2019

functions for facilitation boundary condition file creation
'''

import os
#import glob
#import datetime
import numpy as np 
#import shutil as sh
#import netCDF4 as nc 
#from coastserv.models.units.units import usefor, constituent_boundary_type
import secrets
import pandas as pd

def save_pli_file(root, pli_file):
    '''
    saves uploaded pli to static folder and returns new path
    '''
    if False: # for future if we want to store unique file names
        random_hex = secrets.token_hex(8)
        _ , f_ext = os.path.splitext(pli_file.filename)
        pli_fn = random_hex + f_ext
    
    pli_fn = pli_file.filename
    pli_path = os.path.join(root, pli_fn)
    pli_file.save(pli_path)

    return pli_path

def find_last(var,ss):
    ind = 0
    lstInd = ind
    it = 0
    while ind >= 0:
        ind = var.find(ss,ind + it,len(var))
        it = 1
        if ind < 0:
            return lstInd + 1
        lstInd = ind


def change_os(var):
    osys = []
    for ch in var:
        if ':' in ch:
            osys = 'windows'
        if ch == '\\':
            osys = 'windows'
    if len(osys) == 0:
        osys = 'linux'
    if '/p/' in var and osys == 'linux':
        return var.replace('/p/','p:\\').replace('/','\\')
    elif osys == 'linux':
        return var.replace('/','\\')
    elif ':\\' in var and osys == 'windows':
        return var.replace(':\\','/').replace('\\','/')


def make_len(var, size):
    '''
    returns the passed string as a longer string of len(size) characters, with any additional characters being a prefix of zeros
    '''
    if len(str(var)) != size:
        go_to = size - len(str(var))
        add = ''
        for ii in range(0, go_to):
            add += '0'
        return add + str(var)
    else:
        return str(var)


def datetime_to_timestring(dt):
    return str(dt.year) + '-' + make_len(dt.month, 2) + '-' + make_len(dt.day, 2) + ' ' + make_len(dt.hour, 2) + ':00:00'


def row2array(line):
    '''
    takes a string of space seperated floats and returns an array
    '''
    line = line.split(' ')
    arr = []
    for ch in line:
        try:
            val = float(ch)
            arr.append(val)
        except:
            pass
    return np.array(arr)
    

def read_pli(var):
    '''
    reads a pli boundary into an array
    '''
    with open(var) as plifile:
        lines = plifile.readlines()
        X = []
        Y = []
        for ind, row in enumerate(lines):
            if '.' in row:
                line = row2array(row)
                X.append(float(line[0]))
                Y.append(float(line[1]))
    return np.array([X, Y]).T


def read_sub_file(file):
    '''
    outputs the substances in a sub file
    '''
    with open(file,'r') as subs:
        sub = []
        lines = subs.readlines()
        for line in lines:
            if line[0:9] == 'substance':
                tmp = line.split(' ')
                sub.append(tmp[1].replace("'",''))
    return sub


def boundary_from_ext(var):
    '''
    extracts the boundary name and type from a boundary definition .ext file

    Jul 10 note to self for update 
    this is intentionally different from the more generic version available in dflowutil
    this is because dflowutil will return a salinity and temperature and water level boundary
    that already exist, whereas this tool will make those based solely on a single pli, assuming
    there are not already other consituents specified at the same pli. If there is, and wl is not
    the last constituent specified for a given non-unique pli, the tool will not work.

    This is a valid assumption because this tool is designed to work on models for which only waterlevel
    boundaries have been defined.
    '''

    boundaries = {}
    with open(var,'r') as nmf: # nmf = new_model_file
        page = nmf.readlines()
        ext_type = 'old' # first assume ext type is old, then check
        for line,text in enumerate(page):
            if '[boundary]' in text:
                ext_type = 'new'
        # parse
        if ext_type == 'new':
            for line,text in enumerate(page):
                if '*' not in text:
                    if '[boundary]' in text:
                        name = page[line+2].replace('locationfile=','').replace('.pli','').replace('\n','')
                        if '/' in name:    
                            name = name[find_last(name,'/'):]
                        boundaries[name] = {}
                        boundaries[name]['type'] = page[line+1].replace('quantity=','').replace('\n','')
                        boundaries[name]['pli_loc'] = change_os(page[line+2].replace('locationfile=','').replace('\n',''))
                        boundaries[name]['data_loc'] = page[line+3].replace('forcingfile=','').replace('\n','')
        else:
            for line,text in enumerate(page):
                if '*' not in text:
                    if 'QUANTITY=' in text:
                        name = page[line+1].replace('FILENAME=','').replace('.pli','').replace('\n','')
                        boundaries[name] = {}
                        boundaries[name]['type'] = text.replace('QUANTITY=','')
                        boundaries[name]['location'] = name + '.pli'
                        boundaries[name]['data'] = name + '.tim'

    return boundaries

def read_bc(pli_file, bc_file):
    '''
    reads a bc file into a format useful for plotting a cross sections
    usage restrictions:
    * does not work for uxuyadvectionboundaries
    * file must contain only one variable
    * distance does not check for projection, so will be wrong if spherical

    plotting is expected to look as follows:

    data = read_bc(pli_file, bc_file)

    meshX, meshY = np.meshgrid(data['distance'], data['zprofile'])
    C = np.squeeze(data['salinitybnd'][:,:,time])
    plt.pcolormesh(meshX, meshY, C)
   
    '''    
    non_data = ['ame', 'orcing', 'unction', 'ertical', 'ime', 'uantity', 'nit','ince']
    pli = read_pli(pli_file)
    data = {}
    # create an array of distances
    dist = np.zeros((len(pli)))
    for position in range(1, len(pli)):
        dist[position] = dist[position - 1] + np.abs(pdistf(pli[position, 0], pli[position, 1], pli[position - 1, 0], pli[position - 1, 1]))
    
    with open(bc_file, 'r') as bc:
        ind = []
        page = bc.readlines()
        for row, line in enumerate(page):
            # first pass, obtain metadata
            if '[forcing]' in line:
                ind.append(row)
            if 'Vertical position type          = zdatum' in line:
                data['vertical position type'] = 'zdatum'
            if 'Vertical position specification' in line:
                line = line.replace('Vertical position specification =','')
                arr = row2array(line)
                data['zprofile'] = arr  
            if 'uantity' in line and 'time' not in line:
                data['quantity'] = line.replace('Quantity','').replace('quantity','').replace('=','').strip()      
            if 'nit' in line:
                data['unit'] = line.replace('Unit','').replace('unit','').replace('=','').strip()  
            if 'ince' in line or 'INCE' in line:
                if 'inutes' in line or 'INUTES' in line:
                    data['timeunit'] = 'minutes'
                elif 'econds' in line or 'ECONDS' in line:
                    data['timeunit'] = 'seconds'

                line = line.split(' ')
                time = line[-2]  + ' ' + line[-1].replace('\n','')
                data['reftime'] = pd.Timestamp(time)

        
    assert(len(ind) == len(pli))
    if 'vertical position type' not in data.keys():
        print('ERROR: vertical specification is not zdatum, bc file zprofile is not self describing and not implemented')    
        return None
    else:
        with open(bc_file, 'r') as bc:
            # second pass, load data into memory
            page = bc.readlines()
            # estimate number of times based on first position
            # purpose is for allocation of array
            times = []
            for row in np.arange(ind[0], ind[1]):
                line = page[row]
                chk = sum([word in line for word in non_data])
                if chk == 0 and '.' in line:               
                    arr = row2array(line)
                    time_val = arr[0]
                    if data['timeunit'] == 'minutes':
                        times.append(data['reftime'] + pd.Timedelta(days = time_val / 1440.0))
                    elif data['timeunit'] == 'seconds':
                        times.append(data['reftime'] + pd.Timedelta(days = time_val / 86400.0))

            data['distance'] = dist
            data['coordinates'] = pli
            #data['times'] = np.array(times)
            data['times'] = times

            data[data['quantity']] = np.zeros(( len(data['zprofile']), len(ind), len(times) ))

            for position in range(0,len(ind)):
                tt = 0
                if position + 1 == len(ind):
                    curr_data = page[ind[position]:] 
                else:
                    curr_data = page[ind[position]: ind[position+1]]
                for line in curr_data:
                    chk = sum([word in line for word in non_data])
                    if chk == 0 and '.' in line:
                        arr = row2array(line)
                        data[data['quantity']][:,position,tt] = arr[1:]
                        tt += 1

        return data

def pdistf(X1, Y1, X2, Y2):
    '''
    returns array of euclidean distances between a point and an array
    '''
    return np.sqrt((X2 - X1)**2 + (Y2 - Y1)**2)