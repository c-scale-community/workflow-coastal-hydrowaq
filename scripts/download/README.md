# Download data
This folder contains the following files needed to build and run the docker
containers to download the necessary input data for the workflow:

**Download scripts**
1. `download_cmems_physics.py`
2. `download_cmems_biogeochemistry.py`
3. `download_era5.py`

Type e.g. `python download_cmems_physics.py --help` for usage options.

**Files for docker**
1. `Dockerfile`
2. `environment.yml`

## `docker build`
To build the docker container image run the following command
  
    docker build --tag download-cmems-era5 .

## Usage `docker run` for `download_cmems_physics.py`
To run the `download-cmems-era5` docker container image for `download_cmems_physics.py` do

    docker run -v /path/to/where/you/want/to/keep/the/data:/data/cmems download-cmems-era5 ./download_cmems_physics.py --username TEXT --password TEXT --longitude_min FLOAT --longitude_max FLOAT --latitude_min FLOAT --latitude_max FLOAT --date_min TEXT --date_max TEXT

Example:

    docker run -v /path/to/where/you/want/to/keep/the/data:/data/cmems download-cmems-era5 ./download_cmems_physics.py --username TEXT --password TEXT --longitude_min 22.5 --longitude_max 24.5 --latitude_min 36.5 --latitude_max 38.5 --date_min '2022-04-01' --date_max '2022-04-05'

Note, the default values for --date_min and --date_max download the last 5 days of data.
  
## Usage `docker run` for `download_cmems_biogeochemistry.py`
To run the `download-cmems-era5` docker container image for `download_cmems_biogeochemistry.py` do

    docker run -v /path/to/where/you/want/to/keep/the/data:/data/cmems download-cmems-era5 ./download_cmems_biogeochemistry.py --username TEXT --password TEXT --longitude_min FLOAT --longitude_max FLOAT --latitude_min FLOAT --latitude_max FLOAT --date_min TEXT --date_max TEXT

Example:

    docker run -v /path/to/where/you/want/to/keep/the/data:/data/cmems download-cmems-era5 ./download_cmems_biogeochemistry.py --username TEXT --password TEXT --longitude_min 22.5 --longitude_max 24.5 --latitude_min 36.5 --latitude_max 38.5 --date_min '2022-04-01' --date_max '2022-04-05'
  
Note, the default --date_min and --date_max download the latest 5 days of data.

To get a `username` and `password` please register at https://resources.marine.copernicus.eu/registration-form

## Usage `docker run` for `download_era5.py`
TODO add details
TODO update below about CDS API key

### CDS API key
Use the .cdsapirc file in this repository (only for C-SCALE) or alterantively create your own account via the steps below:

https://cds.climate.copernicus.eu/api-how-to#install-the-cds-api-key
- If you don't have an account, please self register at the CDS registration page (https://cds.climate.copernicus.eu/user/register?destination=%2F%23!%2Fhome) and go to the steps below.
- If you are not logged, please login and go to the step below.
- Copy the code displayed beside (url and key), in the file $HOME/.cdsapirc (in your Unix/Linux environment).


> Usage: download_era5.py [OPTIONS]
> 
> Download Era5 data.
>
> Options:
>   --year TEXT    Year of Era5 data  [required]
>   --output TEXT  Output path for nc file  [required]
>   --help         Show this message and exit.



# General information

## CMEMS MOTUCLIENT
TODO

## CDS API
TODO

General information
https://cds.climate.copernicus.eu/api-how-to 

