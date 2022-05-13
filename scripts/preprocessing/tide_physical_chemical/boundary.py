from coastserv.models.boundary import Boundary
from datetime import datetime
from pathlib import Path
import click
import os

@click.command()
@click.option('--interp', required=False, type=bool, default=False, help='True/False then regular grid interpolation is conducted on 48 local cells, otherwise nearest neighbour (default: False)')
@click.option('--simultaneous', required=False, type=bool, default=False, help='True/False-- if true then all data is interpolated at the same time across entire domain(default: False)')
@click.option('--steric', required=True, default=True, type=str, help='True/False -- if true then steric boundary will be created')
#@click.option('--tref', required=True, type=str, help='YYYY,MM,DD,hh,mm,ss (Reference time in DFlowFM model)')
@click.option('--input', required=True, type=str, help='Folder downloaded data')
@click.option('--model', required=True, type=str, help='Folder with FM model')
@click.option('--output', required=True, type=str, help='Folder with output')     
def boundary(interp, simultaneous, steric, input, output, model):
    "Read tide data from CMEMS and ERA download and convert to FM boundary conditions"

    model_path = Path(model)
    #Find all ext file from the model
    fm_ext = list(model_path.glob('*.ext'))
    sub = ['Opal', 'PON1', 'POP1', 'POC1', 'OXY', 'NO3', 'PO4', 'salinity', 'temperature', 'uxuy', 'steric', 'Green', 'Diat', 'Si']

    #Get tref from model .mdu file
    mdu_files=[]
    for root, dirs, files in os.walk(model_path):
        for file in files:
            if file.endswith(".mdu"):
                 mdu_files.append(os.path.join(root, file))
    
    #Specify text to be found in the .mdu file
    text='Reference date'
    
    try:
        with open(mdu_files[0],'r') as mdufile:
            lines = mdufile.readlines()
            new_list = []
            idx = 0
          
            # looping through each line in the file
            for line in lines:
                  
                # if line have the input string, get the index 
                # of that line and put the
                # line into newly created list 
                if text in line:
                    new_list.insert(idx, line)
                    idx += 1
          
            # closing file after reading
            mdufile.close()
            
            # if length of new list is 0 that means 
            # the input string isn't
            # found in the text file
            if len(new_list)==0:
                print("\n\"" +text+ "\" is not found in \"" +mdufile+ "\"!")
            else:
                tref_str=new_list[0].split()[2]
                tref=datetime.strptime(tref_str, '%Y%m%d')
                print(" ")
                print("Model reference date is: {}".format(tref))
                print(" ")
                
    # entering except block
    # if input file doesn't exist 
    except :
      print("\nThe .mdu file doesn't exist!")
    

    for ext in fm_ext:
        test = Boundary(ext, input, sub, tref, output)
        print('running with options interp = %s, simultaneous = %s, steric = %s' %(interp, simultaneous, steric))
        test.build_boundary(interp=interp, simultaneous=simultaneous, steric=steric)
        print('running with options interp = %s, simultaneous = %s, steric = %s' %(interp, simultaneous, steric))


if __name__ == '__main__':
    boundary()


# docker run -it -v ~/git/use-case-hisea/scripts/processing/download2FM/:/app -v ~/data/hisea/download/:/data/input -v ~/git/use-case-hisea/fm_model/:/data/model -v ~/data/hisea/boundaries:/data/output --entrypoint /bin/bash hisea-processing
# python boundary.py --interp true --simultaneous true --steric true --input /data/input --output /data/output --model /data/model
