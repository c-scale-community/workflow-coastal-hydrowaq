This directory contains all the scripts necessary to run the workflow for "On demand coastal hydrodynamic and water quality modelling" on [C-SCALE](https://c-scale.eu/). There a 3 components / subfolders to the workflow:
1. `download`
2. `preprocessing`
3. `postprocessing`

Information on how to build the docker containers and how to run each of the scripts is in the `README.md` files under each folder.

Here you will find two *example* bash scripts:
1. `run_downloadtest.sh`
2. `run_workflow.sh` (in development)

`run_downloadtest.sh` is a script with which you can test the scalability and performance of downloading data from the [Copernicus Marine Service](https://marine.copernicus.eu/) and the [Climate Data Store](https://cds.climate.copernicus.eu/). It only uses scripts from the `download` folder.

`run_workflow.sh` is a script that runs the complete workflow, first downloading data, then preprocessing it, (`TODO: run model`) and finally (`TODO: postprocessing and visualising the model output`).

To adapt and run the bash scripts, open eith `run_downloadtest.sh` or `run_workflow.sh` in your preferred editor and change the below input variables:
```
CDSAPIRC_LOC=/home/centos/.cdsapirc
CMEMS_UNAME=
CMEMS_PWD=
DATA_DOWNLOAD_LOC=/home/centos/data/download
PREPROC_OUTPUT_LOC=/home/centos/data/preprocout
FM_MODEL_LOC=/home/centos/repos/use-case-hisea/fm_model
LON_MIN=22.5
LON_MAX=24.5
LAT_MIN=36.5
LAT_MAX=38.5
DATE_MIN='2022-04-01'
DATE_MAX='2022-04-05'
```

Note that the docker containers need to have been built for the bash scrips to work. Also note the instruction [here](https://github.com/c-scale-community/use-case-hisea/tree/main/scripts/download) on how to use the CMEMS MOTUCLIENT and how to get a CDS API key.
