# preprocessing / CMEMS and FES2012
This folder contains the files needed to build and run the docker container to preprocess CMEMS and FES2012 data for use as boundary conditions for DFlowFM.

The scripts use the CMEMS physics and biogeochemistry NetCDF files downloaded using `download_cmems_physics.py` and `download_cmems_biogeochemistry.py` to create the necessary `.bc` files to drive a DFlowFM model. 
The `download_cmems_physics.py` and `download_cmems_biogeochemistry.py` scripts and instructions on how to build and run the download docker container can be found [here](https://github.com/c-scale-community/use-case-hisea/tree/main/scripts/download).

## `docker build`

To build the docker container image run the following command from this directoy

	docker build --tag preprocessing .

## Usage `docker run`

After you've built the docker container you can run it. There are slightly different ways to run the `preprocessing` container for CMEMS and for FES2012

For CMEMS type:

	docker run -v /path/to/downloaded/cmems/data:/data/input -v /path/to/fm_model/files:/data/model -v /path/to/where/you/want/to/save/the/output:/data/output preprocessing boundary.py --interp true --simultaneous true --steric true --input /data/input --model /data/model --output /data/output

For FES2012 type:

	docker run -v /path/to/fes2012/data:/data/input -v /path/to/fm_model/files:/data/model -v /path/to/where/you/want/to/save/the/output:/data/output preprocessing tide.py --fespath /data/input --coords "lon_min, lon_max, lat_min, lat_max" --pli plifile.pli --output /data/output --model /data/model

Note that multiple pli files can be specified in the above by doing `--pli plifile1.pli --pli plifile2.pli --pli plifile3.pli` and so on.

Depending on how many ocean boundaries the DFlowFM model has (and hence the number of `plifiles.pli`), the above two scripts will create the necessary `.bc` files to drive a DFlowFM model. Below is an example list of files created by running the above two commands for one `plifile.pli`:

```
Diat_plifile.bc
Green_plifile.bc
NO3_plifile.bc
Opal_plifile.bc
OXY_plifile.bc
PO4_plifile.bc
POC1_plifile.bc
PON1_plifile.bc
POP1_plifile.bc
salinity_plifile.bc
Si_plifile.bc
steric_plifile.bc
temperature_plifile.bc
tide_plifile.bc
uxuy_plifile.bc
```

