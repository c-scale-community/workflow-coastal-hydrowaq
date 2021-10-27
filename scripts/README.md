# Data Download

3 script are available to download data:
- CMEMS physics data
- CMEMS biogeochemistry data
- ERA5

## CMEMS

CMEMS in download with the motu client. This client can be installed via python pip or conda:
	
	python -m pip install motuclient==1.8.4 --no-cache-dir

or

	conda install -c conda-forge motuclient

Example bash scripts using this client are provided in this folder. Note that Username, Password should be set in these scripts

## ERA5

For ERA5 download an example python script is available. For this script CDS API client is used. This client can be installed via python pip or conda:

	pip install cdsapi

or

	conda install -c conda-forge cdsapi

The example script is a command line tool:

> Usage: download_era5.py [OPTIONS]
> 
> Download Era5 data.
>
> Options:
>   --year TEXT    Year of Era5 data  [required]
>   --output TEXT  Output path for nc file  [required]
>   --help         Show this message and exit.
