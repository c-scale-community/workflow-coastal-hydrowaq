# fm_model

This folder contains all the necessary files to run the example Delft3D FM model schematisation. Below we list the important files to take note of when running the model.

## important files and folders
* `dimr_config.xml` \
    This is the `.xml`-file referenced when calling `docker run -v /path/to/fm_model:/data --ulimit stack=-1 -t deltares/delft3dfm:latest`.
    Contact mailto:software.support@deltares.nl for help to edit this file.
* `run_docker.sh` \
    This script is called during `docker run -v /path/to/fm_model:/data --ulimit stack=-1 -t deltares/delft3dfm:latest`. \
    Contact mailto:software.support@deltares.nl for help to edit this file.
* `tttz_waq.mdu` \
    In the `.mdu`-file, users can specify a range of parameters for their simulations, including simulation start and stop time (`TStart` and `TStop`),  locations of the `.ext` forcing files and much more.
* `boundary1_waq.ext`
* `wind_heat_waq.ext`
* `input/`

## other files files

* `Marine_Algae_20200603.sub` = Substance File called in `tttz_waq.mdu`, needed by Water Quality Module
* `addhisout.eho` = Additional History Output File called in `tttz_waq.mdu`, needed by Water Quality Module
* `bloom.spe` = bloom species setting key called in `dimr_config.xml`, needed by Water Quality Module
* `domain.pol` = ❓ called in `wind_heat_waq.ext`, needed for initial conditions
    - [ ] what does this file do?
* `initial_conditions` = folder containing depthavg initial conditions from CMEMS, called in `wind_heat_waq.ext`
* `myortho3_net.nc` = Delft3D FM unstructured grid file, called in `tttz_waq.mdu`
* `proc_def.dat` = Process Database File called in `tttz_waq.mdu` and `dimr_config.xml`, needed by Water Quality Module
* `proc_def.def` = ????. Not called anywhere, but seems related to `proc_def.dat`.
    - [ ] delete❓
* `trial1.ldb` = Land boundary file used for visualisation, called in `tttz_waq.mdu`
* `trial5_obs.xyn` = Obs file (points file with observation stations), called in `tttz_waq.mdu`
* `myortho3_❓❓❓❓_net.nc` = Delft3D FM unstructured grid file, called in `tttz_waq_❓❓❓❓.mdu`
    - [ ] delete❓
* `tttz_waq_❓❓❓❓.mdu` = mdu files created when running on particitions?
* `boundary1_waq.ext` = new format external forcings file, called in `tttz_waq.mdu`
    - [ ] move `.bc` files to `input/` and edit this file
* `wind_heat_waq.ext` = old format external forcing file, called in `tttz_waq.mdu`. Needed for ERA5 and initial conditions.
    - [ ] move files called in here to `input/` and edit this file to point to new locaitons
* `east2.pli` = location file containing the lon/lat coordinates of a boundary, called in `tttz_waq.mdu`
* `south2.pli` = location file containing the lon/lat coordinates of a boundary, called in `tttz_waq.mdu` 
* `east2.ext` and `south2.ext` = contain only information about the water level boundary and reference to a `tide_????.bc file`
    - [ ] delete❓

# TODOs

- [ ] `make_continuity_bc.py` (`input/Continuity.bc`)
- [ ] `make_im1_bc.py` (`input/IM1.bc`)
- [ ] `make_nh4_bc` (`input/NH4.bc`)
- [ ] `make_radsurf_daily_tim.py` (`input/RadSurf_daily.tim`)
- [ ] `make_depthavg_xyz_ini.py` (`input/❓❓❓❓❓_❓❓❓❓❓_fromCMEMS_depthavg.xyz`)
