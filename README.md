# C-SCALE HiSea Use Case
## Workflow solution for coastal hydrodynamic and water quality modelling using Delft3D FM

With this workflow solution a user can easily produce hydrodynamic and water quality hindcasts or forecasts for the coastal ocean for a Delft3D FM model schematisation.

The workflow solution has the following functionality

1. Download the necessary input data for the user's [Delft3D Flexible Mesh](https://www.deltares.nl/en/software/delft3d-flexible-mesh-suite/) model setup. Input data include Copernicus' [Global Ocean Physics Reanalysis](https://resources.marine.copernicus.eu/product-download/GLOBAL_REANALYSIS_PHY_001_030) and [Global ocean biogeochemistry hindcast](https://resources.marine.copernicus.eu/product-download/GLOBAL_REANALYSIS_BIO_001_029), [ERA5](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=form) and [FES2012](https://www.aviso.altimetry.fr/es/data/products/auxiliary-products/global-tide-fes/description-fes2012.html).
2. Prepare the data for ingestion into the user's Delft 3D Flexible Mesh [hydrodynamic](https://www.deltares.nl/en/software/module/d-flow-flexible-mesh/) and [water quality model](https://www.deltares.nl/en/software/module/d-water-quality/). This entails the preparation of forcings, initial conditions, and boundary condiditons.
3. Produce hydrodynamic and water quality hindcasts or forcasts based on the user's Delft3D Flexible Mesh hydrodynamic and water quality model setups.
4. Post-process the model outputs by interpolating the unstructured grid output from Delft3D Flexible Mesh to a regular grid for user specified spatial resolution, timesteps, model vertical layers and variables.
5. Visualise the simulation outputs in an interactive Jupyter Notebook.

The workflow solution can be deployed on any provider part of the [C-SCALE data and compute federation](https://c-scale.eu/) offering cloud container compute.

The ambition is to expand the workflow solution to include options to deploy a hybrid workflow leveraging both cloud and HPC compute resources offered by the C-SCALE federation as illustrated in the figure below.

![workflow](./img/cloud_hpc_workflow.png)

## Folders

* [fm_model](https://github.com/c-scale-community/use-case-hisea/tree/main/fm_model) - example Delft3D Flexible Mesh model files
* [img](https://github.com/c-scale-community/use-case-hisea/tree/main/img) - folder containing images used in this README.md
* [notebooks](https://github.com/c-scale-community/use-case-hisea/tree/main/notebooks) - Jupyter Notebooks used for development and troubleshooting purposes
* [scripts](https://github.com/c-scale-community/use-case-hisea/tree/main/scripts) - scripts and instructions to build and run the docker containers used to run the workflow

# Getting started

### Prerequisites
1. Github account
2. DockerHub account and access to https://hub.docker.com/repository/docker/deltares/delft3dfm (contact software.support@deltares.nl to arrange access)

### Set up your computing environment

It is recommended to run the workflow in a Linux environment with [docker](https://www.docker.com/). This could be a virtual machine in the cloud, or your local computer. To run the workflow locally on a Linux or Apple Mac computer requires [docker desktop](https://www.docker.com/products/docker-desktop/). 

For Windows users, it is recommended to [install the Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install), upgrade to [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install#upgrade-version-from-wsl-1-to-wsl-2) and [install the docker desktop WSL2 backend](https://docs.docker.com/desktop/windows/wsl/).

### Setting up the folder structure and cloning the repo

1. Open a terminal on your local computer or log on to your virtual machine in the cloud.
2. Navigate to the folder where you want to work, here we use the `$HOME` directory, which typically has the path `home/$USER`, where `$USER` is your username.
3. In `$HOME` create the folders to where you want the data from the workflow to be stored, e.g.: \
	`mkdir -p data/download/` - the directory to which you download data from CMEMS and CDS, and where you place the FES data \
	`mkdir -p data/preprocout/` - the directory where the output from the [preprocessing](https://github.com/c-scale-community/use-case-hisea/tree/main/scripts/preprocessing) will be written to \
4. In `$HOME` (or some other preferred directory) clone this repository by doing: \
	`git clone https://github.com/c-scale-community/use-case-hisea.git` \
	This will create the folder `$HOME/use-case-hisea` containing all the files you need for the workflow.
	
### Build and pull the docker containers for the workflow

1. Navigate to `$HOME/use-case-hisea/scripts/download` and do: \
	`docker build --tag download-input .`
2. Navigate to `$HOME/use-case-hisea/scripts/preprocessing/era5` and do: \
	`docker build --tag getera .`
3. Navigate to `$HOME/use-case-hisea/scripts/preprocessing/tide_physical_chemical` and do: \
	`docker build --tag preprocessing .`
4. Pull docker image for Delft3D Flexible Mesh by doing: \
	`docker login --username ... --password ...`
	`docker image pull deltares/delft3dfm:latest`
- [ ] todo: build post-processing docker container

### Run the work flow

An example `bash` script to run each step of the workflow can be found at \
`$HOME/use-case-hisea/scripts/run_workflow.sh`

Navigate to `$HOME/use-case-hisea/scripts`, open `run_workflow.sh` in your preferred text editor and edit the below lines

```
CDSAPIRC_LOC=/path/to/your/.cdsapirc
CMEMS_UNAME= 
CMEMS_PWD=
DATA_DOWNLOAD_LOC=/path/to/where/you/want/to/download/the/data/to # e.g. $HOME/data/download
PREPROC_OUTPUT_LOC=/path/to/where/you/want/to/save/the/preprocessing/output # e.g. $HOME/data/preprocout
FM_MODEL_LOC=/path/to/your/Delft3DFM/model/files 
PLIFILE1=filename1.pli # e.g. south2.pli
PLIFILE2=filename2.pli # e.g. east2.pli
LON_MIN=22.5
LON_MAX=24.5
LAT_MIN=36.5
LAT_MAX=38.5
DATE_MIN='2022-04-01'
DATE_MAX='2022-04-05'
```

Run the workflow from `$HOME/use-case-hisea/scripts` by typing `./run_workflow.sh`


## TODO's

- [ ] confirm example DFlowFM model runs with preprocessed files
	- [ ] clean up fm_model folder (many unnecessary files)
- [ ] confirm postprocessing works
	- [ ] improve input arguments
	- [ ] dockerise
- [ ] make visualisations


