"""Purpose: download ERA5 data from the Copernicus Data Store
Dependencies: $HOME/.cdsapirc (for more info: https://cds.climate.copernicus.eu/api-how-to#install-the-cds-api-key)

Creation date: 5 May 2022
Author: backeb <bjorn.backeberg@deltares.nl> Bjorn Backeberg
"""
import cdsapi
import click
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

@click.command()
@click.option("--longitude_min", default=22.5, help="Set minimum longitude for region of interest")
@click.option("--longitude_max", default=24.5, help="Set maximum longitude for region of interest")
@click.option("--latitude_min", default=36.5, help="Set minimum latitude for region of interest")
@click.option("--latitude_max", default=38.5, help="Set maximum latitude for region of interest")
@click.option("--date_min", default=(datetime.now()-timedelta(days=5)).strftime('%Y-%m-%d'), help="Set start date for data download. Format: YYYY-MM-DD. Default is today minus 5 days.")
@click.option("--date_max", default=(datetime.now()).strftime('%Y-%m-%d'), help="Set end date for data download. Format: YYYY-MM-DD. Default is today.")

def download_era5(longitude_min, longitude_max, latitude_min, latitude_max, date_min, date_max):
    c = cdsapi.Client()
    
    fname = f'/data/era5.nc'
   
    # here we make the strings to use in the api 
    areastr = [str(longitude_min)+'/'+str(latitude_min)+'/'+str(longitude_max)+'/'+str(latitude_max)]

    yearstr = []
    pdyears = pd.period_range(start=date_min, end=date_max, freq='Y')
    [yearstr.append(f'{year:0>4}') for year in pdyears.year]
    
    monthstr = []
    pdmonths = pd.period_range(start=date_min, end=date_max, freq='M')
    [monthstr.append(f'{month:0>2}') for month in np.unique(pdmonths.month)]
    
    daystr = []
    pddays = pd.period_range(start=date_min, end=date_max, freq='D')
    [daystr.append(f'{day:0>2}') for day in np.unique(pddays.day)]
    
    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type':'reanalysis',

            'variable': [
                '10m_u_component_of_wind',
                '10m_v_component_of_wind',
                'mean_sea_level_pressure',
                '2m_dewpoint_temperature',
                'relative_humidity',
                'surface_net_solar_radiation',
                '2m_temperature',
                'total_cloud_cover'
            ],
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

        fname)

if __name__ == '__main__':
    download_era5()
