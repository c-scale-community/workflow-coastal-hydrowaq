# fm_model

This folder contains all the necessary files to run the example Delft3D FM model schematisation. Below we list the important files to take note of when running the model.

## pull and run the Delft3D FM docker contaienr

This example model can be run using the [Delft3D FM docker container](https://hub.docker.com/repository/docker/deltares/delft3dfm). Please contact software.support@deltares.nl to arrange a support package to access the pre-compiled software container.

    docker login --username ... --password ...
	
    docker image pull deltares/delft3dfm:latest
        
    docker run -v /home/$USER/use-case-hisea/fm_model:/data --shm-size=4gb --ulimit stack=-1 -t deltares/delft3dfm:latest

## important files and folders
* `dimr_config.xml` \
    This is the `.xml`-file referenced when calling `docker run -v /path/to/fm_model:/data --ulimit stack=-1 -t deltares/delft3dfm:latest`. \
    Contact software.support@deltares.nl for help to edit this file.
* `run_docker.sh` \
    This script is called during `docker run -v /path/to/fm_model:/data --ulimit stack=-1 -t deltares/delft3dfm:latest`. \
    Contact software.support@deltares.nl for help to edit this file.
* `tttz_waq.mdu` \
    In the `.mdu`-file, users can specify a range of parameters for their simulations, including simulation start and stop time (`TStart` and `TStop`),  locations of the `.ext` forcing files and much more.
* `boundary1_waq.ext` \
    In this file the boundary condition quantities, boundary location file (`.pli`) locations and forcing ('.bc') locations are specified.
* `wind_heat_waq.ext` \
    In this file the forcing field quantitites and file locations (e.g. `input/era5_FM.nc`) as well as intitial condition quantities and file locations are specified.
* `input/` \
    [The input folder](https://github.com/c-scale-community/use-case-hisea/tree/main/fm_model/input) contains all the boundary condition, initial condition and forcing files needed for the simulation. Most of these files are created in the [preprocessing](https://github.com/c-scale-community/use-case-hisea/tree/main/scripts/preprocessing) step.

## other file details

* `Marine_Algae_20200603.sub` = Substance File called in `tttz_waq.mdu`, needed by Water Quality Module
* `addhisout.eho` = Additional History Output File called in `tttz_waq.mdu`, needed by Water Quality Module
* `bloom.spe` = bloom species setting key called in `dimr_config.xml`, needed by Water Quality Module
* `initial_conditions` = folder containing depthavg initial conditions from CMEMS, called in `wind_heat_waq.ext`
* `myortho3_net.nc` = Delft3D FM unstructured grid file, called in `tttz_waq.mdu`
* `proc_def.dat` = Process Database File called in `tttz_waq.mdu` and `dimr_config.xml`, needed by Water Quality Module
* `proc_def.def` = ????. Not called anywhere, but seems to be related to `proc_def.dat`.
    - [ ] delete❓
* `trial1.ldb` = Land boundary file used for visualisation, called in `tttz_waq.mdu`
* `trial5_obs.xyn` = Obs file (points file with observation stations), called in `tttz_waq.mdu`
* `east2.pli` = location file containing the lon/lat coordinates of a boundary, called in `tttz_waq.mdu`
* `south2.pli` = location file containing the lon/lat coordinates of a boundary, called in `tttz_waq.mdu`
