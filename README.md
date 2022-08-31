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
- [ ] to do.

## TODO's

- [ ] confirm example DFlowFM model runs with preprocessed files
	- [ ] clean up fm_model folder (many unnecessary files)
- [ ] confirm postprocessing works
	- [ ] improve input arguments
	- [ ] dockerise
- [ ] make visualisations


