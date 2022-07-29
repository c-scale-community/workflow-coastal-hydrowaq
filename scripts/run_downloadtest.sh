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
# $ ./run_downloadtest.sh

# setup some input variables
DOWNLOAD_TEST=01
CDSAPIRC_LOC=/home/centos/.cdsapirc
CMEMS_UNAME=bbackeberg
CMEMS_PWD=iaTmwJ7D
LON_MIN=22.5
LON_MAX=24.5
LAT_MIN=36.5
LAT_MAX=38.5
DATE_MIN='2022-04-01'
DATE_MAX='2022-04-05'

#
#
# TECHNICALLY USERS SHOULDN'T NEED TO TOUCH THE BELOW...
#
#

mkdir -p /home/centos/data/download/test${DOWNLOAD_TEST}/logfiles
DATA_DOWNLOAD_LOC=/home/centos/data/download/test${DOWNLOAD_TEST}
LOGFILES_LOC=/home/centos/data/download/test${DOWNLOAD_TEST}/logfiles

echo 'logfile = '${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out
touch ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out
echo 'input parameters:' >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out
echo '		LON_MIN  = '$LON_MIN >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out
echo '		LON_MAX  = '$LON_MAX >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out
echo '		LAT_MIN  = '$LAT_MIN >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out
echo '		LAT_MAX  = '$LAT_MAX >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out
echo '		DATE_MIN = '$DATE_MIN >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out
echo '		DATE_MAX = '$DATE_MAX >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out

echo 'downloading era5 data'
echo ' ' >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out
echo '###################################################' >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out
echo '#### ERA5' >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out

start=`date +%s`
docker run \
	-v $CDSAPIRC_LOC:/root/.cdsapirc \
	-v $DATA_DOWNLOAD_LOC:/data \
	download-input python download_era5.py \
		--longitude_min $LON_MIN \
		--longitude_max $LON_MAX \
		--latitude_min $LAT_MIN \
		--latitude_max $LAT_MAX \
		--date_min $DATE_MIN \
		--date_max $DATE_MAX
end=`date +%s`
echo 'download time' >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out
echo '	seconds: '$((end-start)) >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out

du -sh $DATA_DOWNLOAD_LOC/era5.nc >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out

echo 'downloading cmems physics data'
echo ' ' >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out
echo '###################################################' >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out
echo '#### CMEMS PHYSICS' >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out

start=`date +%s`
docker run -v $DATA_DOWNLOAD_LOC:/data \
	download-input python download_cmems_physics.py \
		--username $CMEMS_UNAME \
		--password $CMEMS_PWD \
		--longitude_min $LON_MIN \
		--longitude_max $LON_MAX \
		--latitude_min $LAT_MIN \
		--latitude_max $LAT_MAX \
		--date_min $DATE_MIN \
		--date_max $DATE_MAX
end=`date +%s`
echo 'download time' >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out
echo '	seconds: '$((end-start)) >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out

du -shc \
	$DATA_DOWNLOAD_LOC/cmems_bottomT.nc \
	$DATA_DOWNLOAD_LOC/cmems_so.nc \
	$DATA_DOWNLOAD_LOC/cmems_uo.nc \
	$DATA_DOWNLOAD_LOC/cmems_zos.nc \
	$DATA_DOWNLOAD_LOC/cmems_thetao.nc \
	$DATA_DOWNLOAD_LOC/cmems_vo.nc \
	>> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out

echo 'downloading cmems biogeochemistry data'
echo ' ' >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out
echo '###################################################' >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out
echo '#### CMEMS BIOGEOCHEMISTRY' >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out

start=`date +%s`
docker run \
	-v $DATA_DOWNLOAD_LOC:/data \
	download-input python download_cmems_biogeochemistry.py \
		--username $CMEMS_UNAME \
		--password $CMEMS_PWD \
		--longitude_min $LON_MIN \
		--longitude_max $LON_MAX \
		--latitude_min $LAT_MIN \
		--latitude_max $LAT_MAX \
		--date_min $DATE_MIN \
		--date_max $DATE_MAX
end=`date +%s`
echo 'download time' >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out
echo '	seconds: '$((end-start)) >> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out

du -shc \
	$DATA_DOWNLOAD_LOC/cmems_no3.nc \
	$DATA_DOWNLOAD_LOC/cmems_o2.nc \
	$DATA_DOWNLOAD_LOC/cmems_phyc.nc \
	$DATA_DOWNLOAD_LOC/cmems_po4.nc \
	$DATA_DOWNLOAD_LOC/cmems_si.nc \
	>> ${LOGFILES_LOC}/download.test${DOWNLOAD_TEST}.out

