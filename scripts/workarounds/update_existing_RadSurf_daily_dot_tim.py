# Author: [backeb](https://github.com/backeb)
# This code reads in a RadSurf_daily.tim file and extends the timeseries to a date specified by the user. 
# The new data is then written to an output file specified by the user.
#
# To use the script, the user needs to provide the following options as command-line arguments:
#
# --tref: Reference time as YYYY-MM-DD
# --filename_in: Path/filename of input file
# --filename_out: Path/filename of output file
# --date_max: Date_max as YYYY-MM-DD
#
# Once the user provides the required options, they can run the script and it will
#
# 1. Read the data from the input file specified in --filename_in option.
# 2. Add a datetime column based on the first column and reference time specified in --tref option.
# 3. Determine the number of days between the last datetime in the last row and date_max specified in --date_max option.
# 4. Append empty rows to the data to cover the missing days.
# 5. Fill in the missing values in column 0 using previous value and unique differences.
# 6. Fill in the missing datetime values using column 0 and reference time.
# 7. Compute the average of values in column 1 for rows with the same day and month as the last row.
# 8. Write the transformed data to a new file specified in --filename_out option with columns [0,1], separated by tabs and with floating point numbers in column 1 rounded to 8 decimal places.
# The user can also add the --help option to see the help message and the list of available options.
# , 
# Below is an example of the scripts usage:
#   `python update_existing_RadSurf_daily_dot_tim.py --tref '2015-01-01' --filename_in ../../fm_model/input/RadSurf_daily.tim --filename_out output.txt --date_max '2023-03-11'`


import pandas as pd
import click
import warnings

# Ignore FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)

@click.command()
@click.option('--tref', type=str, help='Reference time as YYYY-MM-DD')
@click.option('--filename_in', help='path/filename of input file')
@click.option('--filename_out', help='path/filename of output file')
@click.option('--date_max', help='date_max as YYYY-MM-DD')
def main(tref, filename_in, filename_out, date_max):

    # Define the reference time
    tref = pd.to_datetime(tref)
    #print(tref, '\n')

    # Read the data from file
    data = pd.read_csv(filename_in, delim_whitespace=True, header=None)

    # Add a datetime column based on the first column
    data['datetime'] = tref + pd.to_timedelta(data.iloc[:, 0], unit='m')

    # get the number of days between the last datetime in the last row and date_max
    date_max = pd.to_datetime(date_max)
    last_datetime = data.iloc[-1]['datetime']
    days_diff = int((date_max - last_datetime) / pd.Timedelta(days=1))
    #print(days_diff, '\n')

    for i in range(days_diff+1):

        # Append an empty row
        data = data.append({}, ignore_index=True)

        # Get the previous value in column 0
        prev_value = data.iloc[-2, 0]
        #print(prev_value, '\n')

        # Get the unique difference between all the values in column 0
        unique_diff = data[0].diff().dropna().unique()
        #print(unique_diff, '\n')

        # Fill the value in column 0, last row with the previous value plus the unique differenc
        data.iloc[-1, 0] = prev_value + unique_diff

        # Set datetime of last row to the corresponding value from column 0
        data.iloc[-1, 2] = tref + pd.to_timedelta(data.iloc[-1, 0], unit='m')

        # Get the day and month of the datetime in the last row
        last_date = data.iloc[-1]['datetime']
        last_day_month = last_date.strftime('%m-%d')
        #print(last_date)
        #print(last_day_month)

        # Create a mask to filter the rows with the same day and month
        mask = data['datetime'].dt.strftime('%m-%d') == last_day_month

        # Compute the average of values in column 1 for these rows
        # Set the value in the last row of column 1 as the average
        data.iloc[-1, 1] = data.loc[mask, 1].mean()

    # convert column 0 to integers
    data[0] = data[0].astype(int)

    # write to file
    data.to_csv(filename_out, columns=[0,1], header=False, index=False, sep='\t', float_format='%.8f')
    
if __name__ == '__main__':
    main()
