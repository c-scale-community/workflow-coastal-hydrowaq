import re
from datetime import datetime, timedelta

def set_date_range(run_mode, forecast_window_mid_pt=None, forecast_window=None, tstart=None, tstop=None, outfile=None):
    # To use the `set_date_range()` function, simply call it with the desired mode of operation and any required parameters. 
    # The function takes two arguments: `run_mode` and `params`, where `run_mode` is either "forecast" or "hindcast" 
    # and `params` is a dictionary of parameters required for the chosen mode of operation.
    # 
    # If `run_mode` is "forecast", the following parameters must be included in `params`:
    #   - `forecast_window_mid_pt`: A string representing the mid-point of the forecast window in the format "today - X days".
    #   - `forecast_window`: A string representing the duration of the forecast window in the format "X days".
    # 
    # If `run_mode` is "hindcast", the following parameters must be included in `params`:
    #   - `tstart`: A string representing the start date of the hindcast period in the format "YYYY-MM-DD".
    #   - `tstop`: A string representing the end date of the hindcast period in the format "YYYY-MM-DD".
    # 
    # The function returns a tuple containing the minimum and maximum dates for the chosen mode of operation.
    # It also updates the config.yml file with the new date_min and date_max of the run.
    #
    # Example usage:
    #   `date_min, date_max = get_date_range(run_mode='forecast', forecast_window_mid_pt='today - 15 days', forecast_window='10 days', outfile='config.yml')`
    #   `!cat config.yml`
    
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

