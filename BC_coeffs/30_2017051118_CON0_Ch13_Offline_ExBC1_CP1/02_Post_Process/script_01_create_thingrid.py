import os
import csv
import math
import datetime
import numpy as np
from netCDF4 import Dataset

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/24_Revision/BC_coeffs/30_2017051118_CON0_Ch13_Offline_ExBC1_CP1'
dir_save = dir_main + '/01_Var_BC/save_files'
dir_out  = dir_main + '/02_Post_Process/2017051118_06h'

anl_start_time   = [datetime.datetime(2017, 5, 11, 18, 0, 0), datetime.datetime(2017, 5, 13, 18, 0, 0)]
anl_end_time     = [datetime.datetime(2017, 5, 13, 12, 0, 0), datetime.datetime(2017, 6, 24, 18, 0, 0)]
cycling_interval = 6
forecast_hours   = [6]
domains          = ['d01']
thingrid         = ['030km']
periods          = {'Spin-up': (10, 0.025), \
                    'Monitor': ( 1,  0.25)}
n_period         = len(periods.keys())

channel          = 8
n_channel        = 10
n_diagbufr       = math.ceil(30/5)
n_diagbufrchan   = math.ceil(26/5)
n_diag           = n_diagbufr + n_channel*n_diagbufrchan

n_we             = 253
n_sn             = 148
n_obs            = n_we*n_sn

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

            glon = np.zeros((n_we, n_sn))
            glat = np.zeros((n_sn))

            with open(dir_out + '/glon' + '_' + datathinning + '_' + dom + '.csv') as csvfile:
                readCSV = csv.DictReader(csvfile, delimiter=',')
                for row in readCSV:
                    glon[int(row['i'])-1, int(row['j'])-1] = float(row['value'])*180/np.pi

            with open(dir_out + '/glat' + '_' + datathinning + '_' + dom + '.csv') as csvfile:
                readCSV = csv.DictReader(csvfile, delimiter=',')
                for row in readCSV:
                    glat[int(row['i'])-1] = float(row['value'])*180/np.pi

            n_time   = 0
            time_now = anl_start_time[0]
            while time_now <= anl_end_time[n_period-1]:
                n_time   = n_time + 1
                time_now = time_now + datetime.timedelta(hours = cycling_interval)
            print('n_time: ', n_time)

            anl_start_time_str = anl_start_time[0].strftime('%Y%m%d%H')
            anl_end_time_str   = anl_end_time[n_period-1].strftime('%Y%m%d%H')
            filename           = dir_out + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                                 str(fhours).zfill(2) + 'h_thingrid.nc'
            print(filename)

            os.system('rm -rf ' + filename)
            ncfile = Dataset(filename, 'w', format='NETCDF4')
            ncfile.createDimension('n_time', n_time)
            ncfile.createDimension('n_obs',  n_obs)
            ncfile.createVariable('obs_idx', 'f8', ('n_time', 'n_obs'))

            itime    = 0
            time_now = anl_start_time[0]
            while time_now <= anl_end_time[n_period-1]:

                time_now_str = time_now.strftime('%Y%m%d%H')
                ftime        = time_now + datetime.timedelta(hours = fhours)
                ftime_str    = ftime.strftime('%Y%m%d%H')

                for idpk, pk in enumerate(list(periods.keys())):
                    if time_now >= anl_start_time[idpk] and time_now <= anl_end_time[idpk]:
                        ict_str = str(periods[pk][0]).zfill(2)
                #results_ges = dir_save + '/' + time_now_str + '/results_abi_g16_ges.' + ftime_str + '.' + dom
                results_ges = dir_save + '/' + time_now_str + '_' + ict_str + '/results_abi_g16_ges.' + ftime_str + '.' + dom
                print(results_ges)

                iobs  = 0
                iline = 0
                a     = open(results_ges)
                for line in a:

                    if iline%n_diag == 0:
                        tmp      = line.split()
                        lat_temp = round(float(tmp[0]), 10)
                        lon_temp = round(float(tmp[1]), 10)

                        index   = np.where(glat < lat_temp)
                        lat_idx = index[0][-1]
                        index   = np.where((glon[:, lat_idx] < lon_temp) & (glon[:, lat_idx] > 0))
                        lon_idx = index[0][-1]
                        index   = (lat_idx-1)*n_we + (lon_idx-1)

                        if ncfile.variables['obs_idx'][itime, index] >= 0:
                            print('Error!')
                            print(miao)
                        else:
                            ncfile.variables['obs_idx'][itime, index] = iobs
                            iobs = iobs + 1

                    iline  = iline + 1
                    n_read = math.floor(iline/n_diag)
                    print(100*n_read/n_obs, end='\r')

                itime    = itime + 1
                time_now = time_now + datetime.timedelta(hours = cycling_interval)

            ncfile.close()
