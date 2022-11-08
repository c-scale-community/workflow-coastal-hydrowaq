# coding: utf-8
"""Purpose: download ERA5 data from the Copernicus Data Store
Dependencies: $HOME/.cdsapirc (for more info: https://cds.climate.copernicus.eu/api-how-to#install-the-cds-api-key)

Creation date: 5 May 2022
Author: backeb <bjorn.backeberg@deltares.nl> Bjorn Backeberg
"""
import cdsapi
import click
from datetime import datetime, timedelta
from pathlib import Path
import xarray as xr

@click.command()
@click.option(	'--longitude_min',
		type=(float),
		help='Minimum longitude for region of interest',
		default=-180,
		show_default=True)
@click.option(	'--longitude_max',
		type=(float), 
		help='Maximum longitude for region of interest',
		default=180,
		show_default=True)
@click.option(	'--latitude_min',
		type=(float),
		help='Minimum latitude for region of interest',
		default=-90,
		show_default=True)
@click.option(	'--latitude_max',
		type=(float),
		help='Maximum latitude for region of interest',
		default=90,
		show_default=True)
@click.option(	'--date_min',
		type=(str),
		help='Start date for data download. Format: YYYY-MM-DD',
		default=(datetime.now()).strftime('%Y-%m-%d'),
		show_default=True)
@click.option(	'--date_max',
		type=(str),
		help='End date for data download. Format: YYYY-MM-DD',
		default=(datetime.now()).strftime('%Y-%m-%d'),
		show_default=True)
@click.option(	'--vars',
		multiple=True,
		help='List of available vars: https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation',
		default=(	'10m_u_component_of_wind',
				'10m_v_component_of_wind',
				'mean_sea_level_pressure',
				'2m_dewpoint_temperature',
				'relative_humidity',
				'surface_net_solar_radiation',
				'2m_temperature',
				'total_cloud_cover'),
		show_default=True)

def download_era5(longitude_min, longitude_max, latitude_min, latitude_max, date_min, date_max, vars):
	c = cdsapi.Client()
	# here we make the strings to use in the api 
	areastr = [str(latitude_min)+'/'+str(longitude_min)+'/'+str(latitude_max)+'/'+str(longitude_max)]
	vars = list(vars) # convert tuple to list for cdsapi
	#make the /data/era5 directory if it does not exist
	Path('data/era5').mkdir(parents=True, exist_ok=True)
	delta = datetime.strptime(date_max, '%Y-%m-%d') - datetime.strptime(date_min, '%Y-%m-%d')
	for i in range(delta.days+1):
		day = datetime.strptime(date_min, '%Y-%m-%d').date() + timedelta(days=i)
		check_file = Path('data/era5/era5_'+str(day)+'.nc')
		while not check_file.is_file():
			yearstr = [f'{day.year:0>4}']
			monthstr = [f'{day.month:0>2}']
			daystr = [f'{day.day:0>2}']
			c.retrieve(
				'reanalysis-era5-single-levels', 
				{
				'product_type':'reanalysis',
				'variable': vars,
				'year':yearstr,
				'area':areastr,
				'month':monthstr,
				'day':daystr,
				'time':[
					'00:00','01:00','02:00',
					'03:00','04:00','05:00',
					'06:00','07:00','08:00',
					'09:00','10:00','11:00',
					'12:00','13:00','14:00',
					'15:00','16:00','17:00',
					'18:00','19:00','20:00',
					'21:00','22:00','23:00'
					],
				'format':'netcdf'
				},
				check_file)

	Path('data/era5/download_era5.done').touch()


if __name__ == '__main__':
	download_era5()
