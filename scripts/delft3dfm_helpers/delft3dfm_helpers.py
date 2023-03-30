from datetime import datetime, date
import os

def get_tref(mdufile):
    # This script reads an MDU file and searches for the line that starts with "RefDate". 
    # It then extracts the date string from that line and converts it to a Python datetime object 
    # using the format '%Y%m%d'. 
    # The resulting datetime object is printed to the console and returned as the output of the function. 
    # The script can be run from the command line with the option to specify the path to the input MDU file.
    # 
    # Example usage:
    #    import delft3dfm_helpers
    #    tref = delft3dfm_helpers.get_tref(mdufile)
    # 
    # Author: [backeb](https://github.com/backeb)
    # This script was written with the assistance of OpenAI. (2021). ChatGPT: a large language model trained 
    # by OpenAI. [Computer software]. Retrieved from https://openai.com/

    # Substitute wildcards in the input path
    mdufile = os.path.expandvars(mdufile)
    
    with open(mdufile, 'r+') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            if lines[i].startswith('RefDate'):
                tref_str=lines[i].split()[2]
                tref=datetime.strptime(tref_str, '%Y%m%d')
                print(lines[i])
    return tref

def update_mdu_tstart_tstop(mdufile, date_min, date_max):
    # This code is a command-line tool that modifies TStart and TStop in a Delft3D FM MDU-file based on the 
    # specified reference time, start date, and end date. 
    # It does so by parsing the MDU-file line by line, identifying the lines containing the start and stop times, 
    # and replacing the values with the updated values.
    # 
    # The tool can be used in a command-line environment by specifying the input MDU-file (mdufile), the reference 
    # time (tref), start date (date_min), and end date (date_max) as options. The tref option should be specified 
    # in the format YYYY-MM-DD. The date_min and date_max options should also be specified in the same format.
    #
    # Example usage:
    #    import delft3dfm_helpers
    #    delft3dfm_helpers.update_mdu_tstart_tstop(mdufile, tref, date_min, date_max)
    #
    # Author: [backeb](https://github.com/backeb)
    # This script was written with the assistance of OpenAI. (2021). ChatGPT: a large language model trained 
    # by OpenAI. [Computer software]. Retrieved from https://openai.com/
    
    # expand the input mdufile to resolve environment variables
    mdufile = os.path.expandvars(mdufile)

    # get tref from mdufile
    tref = get_tref(mdufile=mdufile)

    # Calculate the number of minutes of date_min and date_max since tref
    date_min_str = date_min.strftime('%Y-%m-%d')
    delta = datetime.strptime(date_min_str, '%Y-%m-%d').date() - tref.date()
    date_min_minutes_since_tref = delta.days * 1440 + delta.seconds // 60
    date_min_minutes_since_tref += 720 # add half a day so that delft3dfm starts

    date_max_str = date_max.strftime('%Y-%m-%d')
    delta = datetime.strptime(date_max_str, '%Y-%m-%d').date() - tref.date()
    date_max_minutes_since_tref = delta.days * 1440 + delta.seconds // 60
    date_max_minutes_since_tref += 720 # add half a day so that delft3dfm starts

    # update mdufile with new tstart and tstop
    with open(mdufile, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith('TStart'):
            lines[i] = (f'TStart                                    = '
                        f'{date_min_minutes_since_tref}.            '
                        f'# Start time w.r.t. RefDate (in TUnit)\n')
            print(lines[i])

        elif line.startswith('TStop'):
            lines[i] = (f'TStop                                     = '
                        f'{date_max_minutes_since_tref}.            '
                        f'# Stop time w.r.t. RefDate (in TUnit)\n')
            print(lines[i])

    with open(mdufile, 'w') as f:
        f.writelines(lines)
