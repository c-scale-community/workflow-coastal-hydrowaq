#!/bin/sh
# Purpose: Update helpfile explaining how to use download_*.py scripts
#
# Creation date: 5 May 2022
# Author: backeb <bjorn.backeberg@deltares.nl> Bjorn Backeberg

echo 'This container has the following scripts to download data:' > helpfile
echo ' ' >> helpfile

echo '1. download_cmems_physics.py' >> helpfile
echo '     download hydrodynamic input data for Delft3D FM from the Copernicus Marine Service' >> helpfile
echo '     this script requires a username and password which you can get by registering at: https://resources.marine.copernicus.eu/registration-form' >> helpfile
echo ' ' >> helpfile

echo '2. download_cmems_biogeochemistry.py' >> helpfile
echo '     download biogeochemistry input data for Delft3D FM from the Copernicus Marine Service' >> helpfile
echo '     this script requires a username and password which you can get by registering at: https://resources.marine.copernicus.eu/registration-form' >> helpfile
echo ' ' >> helpfile

echo '3. download_era5.py' >> helpfile
echo '     download ERA5 input data for Delft3D FM from the Copernicus Data Store' >> helpfile
echo '     this script requires a CDS API key. ' >> helpfile
echo '     follow instructions at https://cds.climate.copernicus.eu/api-how-to#install-the-cds-api-key to generate the key' >> helpfile
echo ' ' >> helpfile

echo ' ' >> helpfile
echo '########### USAGE ###########' >> helpfile
echo ' ' >> helpfile

echo 'To run the scripts in docker type' >> helpfile
echo '      $ docker run download-input python download_???.py [OPTIONS]' >> helpfile
echo ' ' >> helpfile

echo 'Below are the usage options for the scripts:' >> helpfile
echo ' ' >> helpfile

python download_cmems_physics.py --help >> helpfile
echo ' ' >> helpfile

python download_cmems_biogeochemistry.py --help >> helpfile
echo ' ' >> helpfile

python download_era5.py --help >> helpfile
echo ' ' >> helpfile
echo 'Dependencies:' >> helpfile
echo '  download_era5.py requires a CDS API key placed in $HOME/.cdsapirc' >> helpfile
echo '  follow instructions at https://cds.climate.copernicus.eu/api-how-to#install-the-cds-api-key to generate the key' >> helpfile

