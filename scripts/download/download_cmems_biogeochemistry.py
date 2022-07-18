# coding: utf-8
"""Purpose: download near real time hydrodynamics data from Copernicus Marine Service

Creation Date: 2 May 2022
Author: backeb <bjorn.backeberg@deltares.nl> Bjorn Backeberg
"""
import click
import subprocess
from datetime import datetime, timedelta

@click.command()
@click.option("--username", default="", help="To get a username and password register at: https://resources.marine.copernicus.eu/registration-form")
@click.option("--password", default="", help="To get a username and password register at: https://resources.marine.copernicus.eu/registration-form")
@click.option("--longitude_min", default=22.5, help="Set minimum longitude for region of interest")
@click.option("--longitude_max", default=24.5, help="Set maximum longitude for region of interest")
@click.option("--latitude_min", default=36.5, help="Set minimum latitude for region of interest")
@click.option("--latitude_max", default=38.5, help="Set maximum latitude for region of interest")
@click.option("--date_min", default=(datetime.now()-timedelta(days=5)).strftime('%Y-%m-%d'), help="Set start date for data download. Format: YYYY-MM-DD. Default is today minus 5 days.")
@click.option("--date_max", default=(datetime.now()).strftime('%Y-%m-%d'), help="Set end date for data download. Format: YYYY-MM-DD. Default is today.")

def runcommand(username, password, longitude_min, longitude_max, latitude_min, latitude_max, date_min, date_max):
    subprocess.run(["python", "-m", "motuclient", 
    "--motu", "https://nrt.cmems-du.eu/motu-web/Motu",
    "--service-id", "GLOBAL_ANALYSIS_FORECAST_BIO_001_028-TDS",
    "--product-id", "global-analysis-forecast-bio-001-028-daily",
    "--longitude-min",str(longitude_min),
    "--longitude-max", str(longitude_max),
    "--latitude-min", str(latitude_min),
    "--latitude-max", str(latitude_max),
    "--date-min", date_min+" 12:00:00",
    "--date-max", date_max+" 12:00:00",
    "--depth-min", "0.493",
    "--depth-max", "5727.918000000001",
    "--variable", "no3",
    "--variable", "o2",
    "--variable", "phyc",
    "--variable", "po4",
    "--variable", "si",
    "--out-dir", "/data",
    "--out-name", "cmems_no3_o2_phyc_po4_si.nc",
    "--user", username,
    "--pwd", password])

if __name__ == '__main__':
    runcommand()
