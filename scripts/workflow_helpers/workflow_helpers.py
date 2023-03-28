import re
from datetime import datetime, timedelta
import os

def set_date_range(run_mode, forecast_window_mid_pt=None, forecast_window=None, tstart=None, tstop=None, outfile=None):
    """
    To use the `set_date_range()` function, simply call it with the desired mode of operation and any required parameters. 
    The function takes two arguments: `run_mode` and `params`, where `run_mode` is either "forecast" or "hindcast" 
    and `params` is a dictionary of parameters required for the chosen mode of operation.
    
    If `run_mode` is "forecast", the following parameters must be included in `params`:
      - `forecast_window_mid_pt`: A string representing the mid-point of the forecast window in the format "today - X days".
      - `forecast_window`: A string representing the duration of the forecast window in the format "X days".
    
    If `run_mode` is "hindcast", the following parameters must be included in `params`:
      - `tstart`: A string representing the start date of the hindcast period in the format "YYYY-MM-DD".
      - `tstop`: A string representing the end date of the hindcast period in the format "YYYY-MM-DD".
    
    The function returns a tuple containing the minimum and maximum dates for the chosen mode of operation.
    It also updates the config.yml file with the new date_min and date_max of the run.
    
    Example usage:
       `date_min, date_max = get_date_range(run_mode='forecast', forecast_window_mid_pt='today - 15 days', forecast_window='10 days', outfile='config.yml')`
       `!cat config.yml`
    """

    if run_mode == 'forecast':
        if forecast_window_mid_pt is None:
            raise ValueError('forecast_window_mid_pt must be defined in forecast mode')
        if not re.match(r'today - \d+ days', forecast_window_mid_pt):
            raise ValueError("forecast_window_mid_pt must have the format 'today - X days'")

        if forecast_window is None:
            raise ValueError('forecast_window must be defined in forecast mode')
        if not re.match(r'\d+ days', forecast_window):
            raise ValueError("forecast_window must have the format 'X days'")

        # Split the input string `forecast_window_mid_pt`
        parts = forecast_window_mid_pt.split(' - ')
        if len(parts) == 2 or parts[1][-4:] == 'days':
            # Parse the number of days to subtract
            days2subtract = int(parts[1][:-5])
        elif len(parts) == 1:
            days2subtract = 0

        # Extract the number from the string `forecast_window` using regular expressions
        days2forecast = int(re.findall(r'\d+', forecast_window)[0])

        # Calculate the date
        today = datetime.today().date()
        date_min = (today - timedelta(days=days2subtract)).strftime("%Y-%m-%d")
        date_max = (today - timedelta(days=days2subtract) + timedelta(days=days2forecast)).strftime("%Y-%m-%d")

    elif run_mode == 'hindcast':
        if tstart is None:
            raise ValueError('tstart must be defined in hindcast mode')
        if tstop is None:
            raise ValueError('tstop must be defined in hindcast mode')

        date_min = tstart
        date_max = tstop
    else:
        raise ValueError("run_mode must be either 'forecast' or 'hindcast'")

    # Open the file in read mode and read its contents
    with open(outfile, 'r') as f:
        file_contents = f.readlines()

    # Update the values of date_min and date_max in the file contents
    for i, line in enumerate(file_contents):
        if line.startswith('date_min:'):
            file_contents[i] = f'date_min: {date_min}\n'
        elif line.startswith('date_max:'):
            file_contents[i] = f'date_max: {date_max}\n'

    # Write the updated contents back to the file
    with open(outfile, 'w') as f:
        f.writelines(file_contents)

    return date_min, date_max

def check_fes2012_files_exist(directory):
    """
    Checks if all required FES2012 files exist in the specified directory.
    
    Inputs:
        - directory: The path to the directory containing the FES2012 files (wildcards are allowed).
        
    Returns:
        - True if all required files exist, False otherwise.
    """
    # List of files to check for
    file_list = [
        "2N2_FES2012_SLEV.nc",
        "E2_FES2012_SLEV.nc",
        "J1_FES2012_SLEV.nc",
        "K1_FES2012_SLEV.nc",
        "K2_FES2012_SLEV.nc",
        "L2_FES2012_SLEV.nc",
        "LA2_FES2012_SLEV.nc",
        "M2_FES2012_SLEV.nc",
        "M3_FES2012_SLEV.nc",
        "M4_FES2012_SLEV.nc",
        "M6_FES2012_SLEV.nc",
        "M8_FES2012_SLEV.nc",
        "MF_FES2012_SLEV.nc",
        "MKS2_FES2012_SLEV.nc",
        "MM_FES2012_SLEV.nc",
        "MN4_FES2012_SLEV.nc",
        "MS4_FES2012_SLEV.nc",
        "MSF_FES2012_SLEV.nc",
        "MTM_FES2012_SLEV.nc",
        "MU2_FES2012_SLEV.nc",
        "N2_FES2012_SLEV.nc",
        "N4_FES2012_SLEV.nc",
        "NU2_FES2012_SLEV.nc",
        "O1_FES2012_SLEV.nc",
        "P1_FES2012_SLEV.nc",
        "Q1_FES2012_SLEV.nc",
        "R2_FES2012_SLEV.nc",
        "S1_FES2012_SLEV.nc",
        "S2_FES2012_SLEV.nc",
        "S4_FES2012_SLEV.nc",
        "SSA_FES2012_SLEV.nc",
        "T2_FES2012_SLEV.nc",
        "Z0_FES2012_SLEV.nc"
    ]

    # Expand the directory path to handle environment variables
    directory = os.path.expandvars(directory)

    # Check if all files in the list exist in the directory
    all_files_exist = all([os.path.isfile(os.path.join(directory, f)) for f in file_list])

    # Touch the 'check4fes2012_files.done' file if all files exist
    if all_files_exist:
        with open('workflow/logs/check4fes2012_files.done', 'w') as f:
            pass

    return all_files_exist

