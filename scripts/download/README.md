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

## `docker build`
To build the docker container image run the following command
  
    docker build --tag download-cmems-era5 .

## Usage `docker run` for `download_cmems_physics.sh`
To run the `download-cmems-era5` docker container image for `download_cmems_physics.sh` do

    docker run -v /path/to/where/you/want/to/keep/the/data:/data/cmems download-cmems-era5 ./download_cmems_physics.sh username password longitude_min longitude_max latitude_min latitude_max date_min date_max

Example to get the latest 5 days of input data for a geographic region of interest:

    docker run -v /path/to/where/you/want/to/keep/the/data:/data/cmems download-cmems-era5 ./download_cmems_physics.sh username password 22.5 24.5 36.5 38.5 $(date --date="5 days ago" +"%Y-%m-%d") $(date +"%Y-%m-%d")
  
## Usage `docker run` for `download_cmems_biogeochemistry.sh`
To run the `download-cmems-era5` docker container image for `download_cmems_biogeochemistry.sh` do

    docker run -v /path/to/where/you/want/to/keep/the/data:/data/cmems download-cmems-era5 ./download_cmems_biogeochemistry.sh username password longitude_min longitude_max latitude_min latitude_max date_min date_max

Example to get the latest 5 days of input data for a geographic region of interest:

    docker run -v /path/to/where/you/want/to/keep/the/data:/data/cmems download-cmems-era5 ./download_cmems_biogeochemistry.sh username password 22.5 24.5 36.5 38.5 $(date --date="5 days ago" +"%Y-%m-%d") $(date +"%Y-%m-%d")
  
Note, to get a `username` and `password` please register at https://resources.marine.copernicus.eu/registration-form

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

