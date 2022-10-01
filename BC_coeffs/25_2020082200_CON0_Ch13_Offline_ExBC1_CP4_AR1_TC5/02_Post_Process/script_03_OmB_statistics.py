import os
import datetime
import numpy as np
from netCDF4 import Dataset
from scipy.stats import skew
from scipy.stats import kurtosis
from scipy.stats import pearsonr

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/24_Revision/BC_coeffs/25_2020082200_CON0_Ch13_Offline_ExBC1_CP4_AR1_TC5'
dir_netcdf = dir_main + '/02_Post_Process/2020082200_06h'
dir_save   = dir_main + '/02_Post_Process/2020082200_06h'

anl_start_time   = datetime.datetime(2020, 8, 22,  0, 0, 0)
anl_end_time     = datetime.datetime(2020, 8, 23, 18, 0, 0)
n_spin_up        = 0
cycling_interval = 6
forecast_hours   = [6]
domains          = ['d01']
thingrid         = ['030km']
channel          = 8
variables        = ['OmB_before_BC', 'OmB_after_BC']

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

            anl_start_time_str = anl_start_time.strftime('%Y%m%d%H')
            anl_end_time_str   = anl_end_time.strftime('%Y%m%d%H')

            filename = dir_netcdf + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                       str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '.nc'
            print(filename)

            ncfile = Dataset(filename)
            time   = ncfile.variables['time'][n_spin_up:]
            n_time = len(time)

            for var in variables:

                temp = []

                for itime in range(0, n_time):

                    itime    = itime + n_spin_up
                    print(itime, end='\r')
                    var_temp = ncfile.variables[var][itime, :]
                    qc_temp  = ncfile.variables['id_qc'][itime, :]
                    index    = (var_temp < 66666) & (qc_temp != -50) & (qc_temp != 50) & (qc_temp != -51) & (qc_temp != 51)
                    temp     = temp + list(var_temp[index])

                n_obs   = len(temp)
                np_temp = np.asarray(temp)
                print('n_obs: ', n_obs, '\n')

                filename = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                           str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_' + var + '_statistics.txt'
                print(filename)

                fsave  = open(filename, 'w')
                amount = len(np_temp)
                fsave.write(str(amount)+'\n')
                print('Amount of Data: ', amount)

                avg = np.average(np_temp)
                fsave.write(str(avg)+'\n')
                print('Average: ', avg)

                std = np.std(np_temp)
                fsave.write(str(std)+'\n')
                print('Standard Deviation: ', std)

                RMS = np.sqrt(np.average(np.square(np_temp)))
                fsave.write(str(RMS)+'\n')
                print('RMS: ', RMS)

                skewness = skew(np_temp, bias=False, nan_policy='omit')
                fsave.write(str(skewness)+'\n')
                print('Skewness: ', skewness)

                kur = kurtosis(np_temp, fisher=True, bias=False, nan_policy='omit')
                fsave.write(str(kur)+'\n')
                print('Kurtosis: ', kur, '\n')

                fsave.close()

            ncfile.close()
