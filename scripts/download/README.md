# Download data

This folder contains the following files needed to build and run the docker
containers to download the necessary input data for the workflow:

**Download scripts**
1. `download_cmems_physics.sh`
2. `download_cmems_biogeochemistry.sh`
3. `download_era5.py`

**Files for docker**
1. `Dockerfile`
2. `environment.yml`

## docker
To build the docker container image run the following command
  
    docker build --tag download-cmems-era5 .

To run the `download-cmems-era5` docker container image for `download_cmems_physics.sh` do

    docker run download-cmems-era5 -v /path/to/where/you/want/to/keep/the/data:/data/cmems username password longitude_min longitude_max latitude_min latitude_max date_min date_max

Example to get the latest 5 days of input data:

    docker run download-cmems-era5 -v /path/to/where/you/want/to/keep/the/data:/data/cmems username password 22.5 24.5 36.5 38.5 $(date --date="5 days ago" +"%Y-%m-%d") $(date +"%Y-%m-%d")
  
Note, to get a `username` and `password` please register at https://resources.marine.copernicus.eu/registration-form

TODO @backeb - add info about biogeochemistry docker

# Deprecated
The below needs updating

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



