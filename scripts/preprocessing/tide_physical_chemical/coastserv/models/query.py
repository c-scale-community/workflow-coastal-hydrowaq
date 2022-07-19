'''
Query

Class that can create batch files for downloading data from CMEMS
'''
import os
import json
import pandas as pd
import numpy as np 
import sys

class Query(object):

    def __init__(self, time_vect, dataset, coords, credentials, out):
        """
        Query class
        
        Arguments:
            time_vect {dictionary} -- {'t_start' : 'yyyyy-mm-dd 12:00:00',
                                       't_end'   : 'yyyy-mm-dd 12:00:00'}
            dataset {str} -- 'physchem' or' bio'
            coords {list} -- [xmin, xmax, ymin, ymax]
            user {str} -- username
            pwd {str} -- password
            out {str} -- path for output of batch files
        """
        self.time_vect  = time_vect
        self.dataset    = dataset
        self.coords     = coords

        self.user       = credentials['user']
        self.pwd        = credentials['pwd']
        self.out        = out
        
        if True: # multiyear reanalysis data (01-01-1993 12:00 till 31-05-2020 12:00)
            self.url = 'http://my.cmems-du.eu/motu-web/Motu'
            self.datasets = {'physchem' : ['GLOBAL_MULTIYEAR_PHY_001_030-TDS', 'cmems_mod_glo_phy_my_0.083_P1D-m'],
                             'bio'      : ['GLOBAL_MULTIYEAR_BGC_001_029-TDS', 'cmems_mod_glo_bgc_my_0.25_P1D-m']}
        else: # operational forecast data (01-01-2019 12:00 till now + several days)
            self.url = 'http://nrt.cmems-du.eu/motu-web/Motu'
            self.datasets = {'physchem' : ['GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS', 'global-analysis-forecast-phy-001-024'],
                             'bio'      : ['GLOBAL_ANALYSIS_FORECAST_BIO_001_028-TDS', 'global-analysis-forecast-bio-001-028-daily']}

        self.all_subs = {'physchem' : ['thetao', 'so', 'zos', 'uo', 'vo'], #, 'bottomT'
                         'bio'      : ['chl', 'o2','no3','po4','si']} #, 'nppv'

    def build_query(self):
        # to remove need to write self. in all of the functions that were previously not part of this class
        self.create_query(self.time_vect, self.dataset, self.coords, self.user, self.pwd, self.out)


    def create_query(self, time_vect, dataset, coords, user, pwd, out):

        '''
        writes the bat and sh files required to download the requested parameters from CMEMS
        only linux has capabilities to retry the download if it failed NOT YET COMPLETE
        '''

        # quarter of a year is a good size based on trial and error, but this depends on the extent!
        # changed to 30 days based on communication with CMEMS
        #max_time = np.ceil(365/4)
        max_time = 7
        tot_time = pd.Timestamp(time_vect['t_end']) - pd.Timestamp(time_vect['t_start'])
        num_time_intervals = np.ceil(tot_time.days / max_time)

        if np.abs(coords[1] - coords[0]) * np.abs(coords[3] - coords[2]) > 858:
            print('WARNING: REQUESTED SPATIAL EXTENT MAY BE TOO BIG FOR SERVER. TRY REDUCING SPATIAL EXTENT')

        times = []
        for tt in range(0, int(num_time_intervals)):
            times.append([pd.Timestamp(time_vect['t_start']) + pd.Timedelta(days = int(max_time * tt)), pd.Timestamp(time_vect['t_start']) + pd.Timedelta(days = int(max_time * (tt+1)-1))])  


        subs = self.all_subs[dataset]

        self.args = {'motu'         : self.url, 
                'service-id'   : self.datasets[dataset][0], 
                'product-id'   : self.datasets[dataset][1], 
                'longitude-min': coords[0], 
                'longitude-max': coords[1], 
                'latitude-min' : coords[2], 
                'latitude-max' : coords[3], 
                'date-min'     : None, 
                'date-max'     : None, 
                'depth-min'    : '0.493', 
                'depth-max'    : '5727.918000000001', 
                'variable'     : None, 
                'out-dir'      : '"data"', 
                'out-name'     : None, 
                'user'         : user, 
                'pwd'          : pwd}

        if not os.path.exists(os.path.join(out, self.args['out-dir'].replace('"',''))):
            os.mkdir(os.path.join(out, self.args['out-dir'].replace('"','')))
        
        print('writing query')

        # WINDOWS

        self.bat = os.path.join(out, 'CMEMS_download_%s.bat' % dataset)

        with open(self.bat, 'w') as bat:
            chk = 0
            for sub in subs:
                for tt in range(0, int(num_time_intervals)):
                    out_name = sub + '_' + str(times[tt][0]).replace(':','-').replace(' ','_') + '_' + str(times[tt][1]).replace(':','-').replace(' ','_') + '.nc'      
                    file_name = sub + '_' + str(times[tt][0]).replace(':','-').replace(' ','_') + '_' + str(times[tt][1]).replace(':','-').replace(' ','_') + '.nc'
                    #bat.write('echo "downloading %s"\n' % out_name)
                    bat.write('if exist %s ( \n' % (os.path.join(os.getcwd(), out, self.args['out-dir'].replace('"',''), out_name)))
                    bat.write('\tgoto skipdownload%i\n' % chk)
                    bat.write('\t)\n\n')

                    self.write_request(bat, sub, times, tt, out_name)

                    bat.write('\n')
                    bat.write(':chkretry%i\n' % chk)
                    bat.write('if not exist %s ( \n' % (os.path.join(os.getcwd(), out, self.args['out-dir'].replace('"',''), out_name)))
                    bat.write('\techo "download failed, giving the server a break..."\n')
                    bat.write('\ttimeout 10\n')
                    bat.write('\t')

                    self.write_request(bat, sub, times, tt, file_name)

                    bat.write('\n\tgoto chkretry%i \n' % chk)

                    bat.write('\t)\n\n')
                    bat.write(':skipdownload%i\n\n' % chk)

                    chk+=1

                  
        # LINUX 
        
        self.sh = os.path.join(out, 'CMEMS_download_%s.sh' % dataset)

        with open(self.sh,'w') as shell:
            shell.write('#!/bin/bash\n')
            for sub in subs:
                for tt in range(0, int(num_time_intervals)):
                    out_name = sub + '_' + str(times[tt][0]).replace(':','-').replace(' ','_') + '_' + str(times[tt][1]).replace(':','-').replace(' ','_') + '.nc'
                    file_name = sub + '_' + str(times[tt][0]).replace(':','-').replace(' ','_') + '_' + str(times[tt][1]).replace(':','-').replace(' ','_') + '.nc' 

                    self.write_request(shell, sub, times, tt, out_name)    
                    
                    shell.write('\n')
                    shell.write('if [ ! -f "%s" ]; then\n' % (os.path.join(os.getcwd(), out, self.args['out-dir'].replace('"',''), out_name)))
                    shell.write('   while (( ! -f "%s" ))\n' % (os.path.join(os.getcwd(), out, self.args['out-dir'].replace('"',''), out_name)))
                    shell.write('   do\n')
                    shell.write('       echo "ERROR: download failed on server end, retrying..."\n')
                    shell.write('       echo "giving the server a break..."\n')
                    shell.write('       sleep 10s\n')

                    self.write_request(shell, sub, times, tt, file_name)
                    
                    shell.write('\n')
                    shell.write('   done\n')
                    shell.write('fi\n')                

        print('finished writing query')
    

    def write_request(self, bat, sub, times, tt, out_name):
        bat.write('python -m motuclient ')
        for arg in self.args.keys():
                if arg == 'variable':
                    bat.write('--variable ' + sub + ' ')
                elif arg == 'date-min':
                    bat.write('--date-min "' + str(times[tt][0]) + '" ')
                elif arg == 'date-max':
                    bat.write('--date-max "' + str(times[tt][1]) + '" ')
                elif arg == 'out-name':
                    bat.write('--out-name ' + out_name + ' ')
                else:
                    bat.write('--%s %s ' % (arg, self.args[arg]))


    def send_request(self):
        if sys.platform == 'linux':
            self.send_request_linux()
        else:
            self.send_request_windows()


    def send_request_windows(self):
        """
        runs the created batch file
        """
        print('sending request via *.bat file')
        print(self.bat)
        path = os.getcwd()
        os.chdir(os.path.split(self.bat)[0])
        os.system(self.bat)
        print('request processing finished')
        os.chdir(path)


    def send_request_linux(self):
        """
        runs the created shell script
        """
        print('sending request via *.sh file')
        path = os.getcwd()

        print(self.sh)

        os.system('chmod 777 ' + self.sh)
        # will not work if sudo python environment variables are not the same as user
        os.chdir(os.path.split(self.bat)[0])

        #os.system('sudo ' + self.sh)
        os.system(self.sh)
        print('request processing finished')

        os.chdir(path)
