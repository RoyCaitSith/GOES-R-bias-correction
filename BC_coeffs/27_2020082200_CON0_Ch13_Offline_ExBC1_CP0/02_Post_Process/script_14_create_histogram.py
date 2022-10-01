import os
import datetime
import numpy as np
from netCDF4 import Dataset
from scipy.interpolate import griddata
from scipy.stats import skew
from scipy.stats import kurtosis
from scipy.stats import pearsonr

dir_GOES   = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main   = dir_GOES + '/24_Revision/BC_coeffs/27_2020082200_CON0_Ch13_Offline_ExBC1_CP0'
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
variables        = {'BT_obs_before_BC': [100, 300, 1], \
                    'BT_obs_after_BC':  [100, 300, 1], \
                    'BT_bkg':           [100, 300, 1], \
                    'cldeff_obs':       [-100, 40, 1], \
                    'cldeff_bkg':       [-100, 40, 1]}

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

            for idv, var in enumerate(variables.keys()):

                print(var)
                (range_min, range_max, range_interval) = variables[var]

                temp = []
                for itime in range(0, n_time):

                    print(itime, end='\r')
                    var_temp    = ncfile.variables[var][itime, :]
                    id_qc       = ncfile.variables['id_qc'][itime, :]
                    clr_rbc_idx = ncfile.variables['clr_rbc_idx'][itime, :]
                    index       = (var_temp < 66666) & (id_qc != -50) & (id_qc != 50) & (id_qc != -51) & (id_qc != 51)
                    #index       = (var_temp < 66666) & (id_qc != -50) & (id_qc != 50) & (id_qc != -51) & (id_qc != 51) & (clr_rbc_idx == 1)
                    #index       = (var_temp < 66666) & (id_qc != -50) & (id_qc != 50) & (id_qc != -51) & (id_qc != 51) & (clr_rbc_idx == 0)
                    temp        = temp + list(var_temp[index])

                np_temp = np.asarray(temp)
                print(len(np_temp))

                bins = np.arange(range_min-0.5*range_interval, range_max+range_interval, range_interval)
                hist, bin_edges = np.histogram(np_temp, bins, density=False)

                filename = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                           str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_PDF_' + str(idv).zfill(2) + '_All Sky.txt'
                #filename = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                           #str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_PDF_' + str(idv).zfill(2) + '_Clear Sky.txt'
                #filename = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                           #str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_PDF_' + str(idv).zfill(2) + '_Cloudy Sky.txt'
                print(filename)

                fsave = open(filename, 'w')
                for pdf in hist:
                    fsave.write(str(pdf)+'\n')
                fsave.close()

                hist, bin_edges = np.histogram(np_temp, bins, density=True)
                CDF = np.cumsum(hist)

                filename = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                           str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_CDF_' + str(idv).zfill(2) + '_All Sky.txt'
                #filename = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                           #str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_CDF_' + str(idv).zfill(2) + '_Clear Sky.txt'
                #filename = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                           #str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_CDF_' + str(idv).zfill(2) + '_Cloudy Sky.txt'
                print(filename)

                fsave = open(filename, 'w')
                for cdf in CDF:
                    fsave.write(str(cdf)+'\n')
                fsave.close()

            ncfile.close()
