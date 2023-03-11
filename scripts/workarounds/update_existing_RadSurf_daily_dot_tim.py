
import pandas as pd
import click
import warnings

# Ignore FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)

@click.command()
@click.option('--tref', type=str, help='Reference time')
@click.option('--filename_in')
@click.option('--filename_out')
@click.option('--date_max')
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
