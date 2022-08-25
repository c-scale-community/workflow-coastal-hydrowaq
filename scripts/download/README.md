# download

This folder contains the files needed to build and run the docker container to download the necessary input data for the workflow.

## Download scripts

1. `download_cmems_physics.py`
2. `download_cmems_biogeochemistry.py`
3. `download_era5.py`

## Dependencies

* the `download_cmems_physics.py` and `download_cmems_biogeochemistry.py` require a `username` and `password` which can be obtained by registering at <https://resources.marine.copernicus.eu/registration-form>.
* the `download_era5.py` script requires a CDS API key. follow instructions at <https://cds.climate.copernicus.eu/api-how-to#install-the-cds-api-key> to generate the key.

## `docker build`

To build the docker container image run the following command
  
    docker build --tag download-input .

## Usage: `docker run`

For help

    docker run download-input 

## Examples

`download_cmems_physics.py`:

    docker run -v /path/to/where/you/want/to/download/to:/data download-input python download_cmems_physics.py --username TEXT --password TEXT --longitude_min 22.5 --longitude_max 24.5 --latitude_min 36.5 --latitude_max 38.5 --date_min '2022-04-01' --date_max '2022-04-05'

`download_cmems_biogeochemistry.py`:

    docker run -v /path/to/where/you/want/to/download/to:/data download-input python download_cmems_biogeochemistry.py --username TEXT --password TEXT --longitude_min 22.5 --longitude_max 24.5 --latitude_min 36.5 --latitude_max 38.5 --date_min '2022-04-01' --date_max '2022-04-05'

`download_era5.py`:

    docker run -v /path/to/.cdsapirc:/root/.cdsapirc -v /path/to/where/you/want/to/download/to:/data download-input python download_era5.py --longitude_min 22.5 --longitude_max 24.5 --latitude_min 36.5 --latitude_max 38.5 --date_min '2022-04-01' --date_max '2022-04-05'

## Additional information

### CMEMS MOTUCLIENT

For more information about the CMEMS MOTUCLIENT see: <https://help.marine.copernicus.eu/en/articles/4796533-what-are-the-motu-client-motuclient-and-python-requirements>

### CDS API

For more information about the CDS API see: <https://cds.climate.copernicus.eu/api-how-to>

#### Creating a CDS API key

Follow instruction at: <https://cds.climate.copernicus.eu/api-how-to#install-the-cds-api-key>

1. If you don't have an account, register at <https://cds.climate.copernicus.eu/user/register?destination=%2F%23!%2Fhome>
2. Login at <https://cds.climate.copernicus.eu/user/login?destination=%2F%23!%2Fhome>
3. Navigate to <https://cds.climate.copernicus.eu/api-how-to>
4. Copy the code displayed (url and key) into the file `.cdsapirc`
5. Move the `.cdsapirc` file to `$HOME`
6. Accept the Licence to use Copernicus Products at <https://cds.climate.copernicus.eu/cdsapp/#!/terms/licence-to-use-copernicus-products> while logged in

Note: Be shure to 

## Windows users

To run these docker containers locally on Windows we suggest using the Windows Subsystem for Linux (WSL) with Ubuntu 20.04 and Docker Desktop.

To install WSL and Ubuntu 20.04 follow instructions here: <https://docs.microsoft.com/en-us/windows/wsl/install>

To install Docker Desktop follow instructions here: <https://www.docker.com/products/docker-desktop/>

In Docker Desktop under Settings > General, make sure the "Use the WSL 2 based engine" checkbox is checked.
