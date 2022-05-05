from coastserv.models.boundary import Boundary
import datetime
from pathlib import Path
import click

@click.command()
@click.option('--interp', required=False, type=bool, default=False, help='True/False then regular grid interpolation is conducted on 48 local cells, otherwise nearest neighbour (default: False)')
@click.option('--simultaneous', required=False, type=bool, default=False, help='True/False-- if true then all data is interpolated at the same time across entire domain(default: False)')
@click.option('--steric', required=True, default=True, type=str, help='True/False -- if true then steric boundary will be created')
@click.option('--tref', required=True, type=str, help='YYYY,MM,DD,hh,mm,ss (Reference time in DFlowFM model)')
@click.option('--input', required=True, type=str, help='Folder downloaded data')
@click.option('--model', required=True, type=str, help='Folder with FM model')
@click.option('--output', required=True, type=str, help='Folder with output')
def boundary(interp, simultaneous, steric, tref, input, output, model):
    "Read tide data from CMEMS and ERA download and convert to FM boundary conditions"

    model_path = Path(model)
    #Find all ext file from the model
    fm_ext = list(model_path.glob('*.ext'))
    sub = ['Opal', 'PON1', 'POP1', 'POC1', 'OXY', 'NO3', 'PO4', 'salinity', 'temperature', 'uxuy', 'steric', 'Green', 'Diat', 'Si']

    tref_list = [int(c) for c in tref.strip().split(',')]
    tref = datetime.datetime(tref_list[0], tref_list[1], tref_list[2], tref_list[3], tref_list[4], tref_list[5])

    for ext in fm_ext:
        test = Boundary(ext, input, sub, tref, output)
        print('running with options interp = %s, simultaneous = %s, steric = %s' %(interp, simultaneous, steric))
        test.build_boundary(interp=interp, simultaneous=simultaneous, steric=steric)
        print('running with options interp = %s, simultaneous = %s, steric = %s' %(interp, simultaneous, steric))


if __name__ == '__main__':
    boundary()


# docker run -it -v ~/git/use-case-hisea/scripts/processing/download2FM/:/app -v ~/data/hisea/download/:/data/input -v ~/git/use-case-hisea/fm_model/:/data/model -v ~/data/hisea/boundaries:/data/output --entrypoint /bin/bash hisea-processing
# python boundary.py --interp true --simultaneous true --steric true --tref '2015,01,01,00,00,00' --input /data/input --output /data/output --model /data/model
