# Instructions for DFlowFM_Preprocessing_Era5

DFlowFM_Preprocessing_Era5 is a Python library for dealing with the conversion of ERA5 data for usage with a DFlowFM model.
It converts NetCDF Era5 data to a single NetCDF input file (called era5_FM.nc) that can then be used to drive a DFlowFM model. Parameters that are currently included in the conversion, include:

- 2 metre dewpoint temperature
- 2 metre temperature
- Total cloud cover
- eastward_wind
- northward_wind
- air pressure

More parameters can be added by modifying the ERA5_convert2_FM_and_merge_allVars.py script. However, if you do add more parameters, the docker container
needs to be created again too.

The directory structure of the folder should look like:

```bash
+-- scripts
    +-- Dockerfile
    +-- ERA5_convert2_FM_and_merge_allVars.py
    +-- Retrieve_ERA5.py
    +-- environment.yml
    +-- era_maps_allVars.py
    +-- readme.md
```

## How to create the docker container

- Open a terminal, navigate to the folder containing the python scripts, the yaml environment, this readme, and the Dockerfile.
- Run the following command:
```bash
docker build --tag getera:1.0 .
```
- To check that the image has created, run:
```bash
docker images
```
This should output two images:
```bash
REPOSITORY               TAG                 IMAGE ID            CREATED             SIZE
getera                   1.0                 041fb0e18df0        3 minutes ago       1.29GB
continuumio/miniconda3   latest              52daacd3dd5d        2 months ago        437MB
```
- To save the created docker image as a .tar file, run:
```bash
docker image save --output getera.tar getera:1.0
```
## Usage
- If the image is not created yet, create it from the tar file with:
```bash
docker load --input .\getera.tar
```
- To use the created docker container to convert your NetCDF ERA5 input into a format that DFlowFM can use, 
place the NetCDF files you would like to convert in a folder called 'in'. In a terminal, navigate to the folder that contains this 'in' folder and run:
```bash
docker run -v Path_to_in_folder:/app/data -t getera:1.0
```
A test_case folder has been added to this repo. It contains three ERA5 netcdf files in an 'in' folder. Run the test case with:
```bash
 docker run -v  D:\PROJECTS\2020\COASTSERV_ALL\openearth_era5\test_case\test_era5\:/app/data -t getera:1.0
```

- This will create an 'out' folder within the same directory as the 'in' folder.  era5_FM.nc file. To use this file with your DFlowFM simulation, copy the era5_FM.nc file into your DFlowFM model directory. Ensure that 
DFlowFM can find it by setting the FILENAME variable in the .ext file to era5_FM.nc. **Note: This takes about 20 minutes to run. The era5_FM.nc file should have a size of 
60889 KB in the end.

