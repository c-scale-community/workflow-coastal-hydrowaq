# C-SCALE HiSea

## Workflow

- Download data
- Preprocessing
    - tidal boundaries -> script/processing/tide_physical_chemical/boundary.py
    - pyshical chemical -> script/processing/tide_physical_chemical/tide.py
    - convert era -> script/processing/era5/ERA5_convert2_FM_and_merge_allVars.py
- FM Model
- Postprocessing

## TODO

- fix convert era 5 python script. Did the ERA5 downloaded data change?
- Update the model with the output from the preprocessing steps. These will output model files which need to be copied to the fm model directory
- Try model run with output from the preprocessing container
- Check postprocessing


