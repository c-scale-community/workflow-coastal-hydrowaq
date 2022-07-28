#!/bin/bash

## prerequisites
#
# 1. build the docker containers to download the data following instructions on 
#	<https://github.com/c-scale-community/use-case-hisea/tree/main/scripts/download>
#
# 2. build the docker containere to run preprocessing following instructions on
#	<...>
#
## usage to also log how long it takes to run the workflow
# $ (time run_workflow.sh) > logfiles/logfile_$(date +%F)_$(date +%T) 2>&1

# setup some input variables
CDSAPIRC_LOC=/home/centos/.cdsapirc
CMEMS_UNAME=bbackeberg
CMEMS_PWD=iaTmwJ7D
DATA_DOWNLOAD_LOC=/home/centos/backeb/data/download
PREPROC_OUTPUT_LOC=/home/centos/backeb/data/preprocout
FM_MODEL_LOC=/home/centos/backeb/use-case-hisea/fm_model
LON_MIN=22.5
LON_MAX=24.5
LAT_MIN=36.5
LAT_MAX=38.5
DATE_MIN='2022-04-01'
DATE_MAX='2022-04-05'

# download era5 data
docker run -v $CDSAPIRC_LOC:/root/.cdsapirc -v $DATA_DOWNLOAD_LOC:/data download-input python download_era5.py --longitude_min $LON_MIN --longitude_max $LON_MAX --latitude_min $LAT_MIN --latitude_max $LAT_MAX --date_min $DATE_MIN --date_max $DATE_MAX

# download cmems physics
docker run -v $DATA_DOWNLOAD_LOC:/data download-input python download_cmems_physics.py --username $CMEMS_UNAME --password $CMEMS_PWD --longitude_min $LON_MIN --longitude_max $LON_MAX --latitude_min $LAT_MIN --latitude_max $LAT_MAX --date_min $DATE_MIN --date_max $DATE_MAX

# download cmems biogeochemistry
docker run -v $DATA_DOWNLOAD_LOC:/data download-input python download_cmems_biogeochemistry.py --username $CMEMS_UNAME --password $CMEMS_PWD --longitude_min $LON_MIN --longitude_max $LON_MAX --latitude_min $LAT_MIN --latitude_max $LAT_MAX --date_min $DATE_MIN --date_max $DATE_MAX

echo $(du -shc $DATA_DOWNLOAD_LOC/*)
