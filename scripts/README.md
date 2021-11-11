# Data Download

3 script are available to download data:
- CMEMS physics data
- CMEMS biogeochemistry data
- ERA5

## CMEMS

General information
https://help.marine.copernicus.eu/en/articles/4796533-what-are-the-motu-client-motuclient-and-python-requirements

CMEMS in download with the motu client. This client can be installed via python pip or conda:
	
	python -m pip install motuclient==1.8.4 --no-cache-dir

or

	conda install -c conda-forge motuclient

Example bash scripts using this client are provided in this folder. Note that Username, Password should be set in these scripts

## ERA5

General information
https://cds.climate.copernicus.eu/api-how-to 

### CDS API key

Use the .cdsapirc file in this repository (only for C-SCALE) or alterantively create your own account via the steps below:

https://cds.climate.copernicus.eu/api-how-to#install-the-cds-api-key
- If you don't have an account, please self register at the CDS registration page (https://cds.climate.copernicus.eu/user/register?destination=%2F%23!%2Fhome) and go to the steps below.
- If you are not logged, please login and go to the step below.
- Copy the code displayed beside (url and key), in the file $HOME/.cdsapirc (in your Unix/Linux environment).

### Install the CDS API client

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
