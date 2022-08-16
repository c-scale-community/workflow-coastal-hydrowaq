# preprocessing / era5
This folder contains the files needed to build and run the docker container to preprocess ERA5 data for use as forcing fields for DFlowFM.

It converts the daily ERA5 NetCDF files downloaded using `download_era5.py` to a single NetCDF input file (called era5_FM.nc) that can then be used to drive a DFlowFM model. 
The `download_era5.py` script and instructions on how to build the download docker container can be found [here](https://github.com/c-scale-community/use-case-hisea/tree/main/scripts/download).

The directory structure of this folder should look like:

```bash
+-- scripts
    +-- Dockerfile
    +-- ERA5_convert2_FM_and_merge_allVars.py
    +-- Retrieve_ERA5.py
    +-- environment.yml
    +-- era_maps_allVars.py
    +-- README.md
```

## `docker build`

To build the docker container image run the following command from this directoy

	docker build --tag getera .

## Usage `docker run`

After you've built the docker container you can run it by typing

	docker run -v /path/to/downloaded/era5/data:/data/input -v /path/to/where/you/want/to/save/the/output:/data/output getera ERA5_convert2_FM_and_merge_allVars.py --input /data/input --output /data/output

An `era5_FM.nc` file will be created in `/path/to/where/you/want/to/save/the/output`. To use this file with your DFlowFM simulation, copy the `era5_FM.nc` file into your DFlowFM model directory. Ensure that DFlowFM can find it by setting the FILENAME variable in the `.ext` file to `era5_FM.nc`

