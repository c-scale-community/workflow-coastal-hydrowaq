from coastserv.models.tide import Tide
from pathlib import Path
import click

@click.command()
@click.option('--fespath', required=True, type=str, help='name of FES tidal constituents')
@click.option('--coords', required=True, type=str, help='boundingbox coordinates: lonmin, lonmax, latmin, latmax',)
@click.option('--pli', required=True, multiple=True, type=str, help='Name of polygon file that contains the coordinates at which boundaries are needed. Name only, no spaces.')
@click.option('--output', required=True, type=str, help='name of output folder')
@click.option('--model', required=True, type=str, help='Folder with FM model')

def convert_tide(fespath, coords, pli, output, model):
    "Read tide data from FES and convert to FM boundary conditions"
    coordsval = [float(c) for c in coords.strip().split(',')]

    path = Path(fespath)
    model_path = Path(model)

    for f in pli:
        pli = model_path / f
        tide = Tide(fespath, coordsval, str(pli), output)
        tide.build_tide()

if __name__ == '__main__':
    convert_tide()


# python test_tide.py --fespath /data/FES2012/data --coords "23.069583000000000, 25.354302000000000, 35.835178000000000, 38.622824000000000" --pli south2.pli --pli east2.pli --output /data/output --model /data/model