import os
import datetime
import numpy as np
from netCDF4 import Dataset
from scipy.interpolate import griddata

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/24_Revision/BC_coeffs/30_2017051118_CON0_Ch13_Offline_ExBC1_CP1'
dir_netcdf = dir_main + '/02_Post_Process/2017051118_06h'
dir_statis = dir_main + '/02_Post_Process/2017051118_06h'
dir_save   = dir_main + '/02_Post_Process/2017051118_06h'

anl_start_time   = datetime.datetime(2017, 5, 11, 18, 0, 0)
anl_end_time     = datetime.datetime(2017, 6, 24, 18, 0, 0)
n_spin_up        = 8
cycling_interval = 6
forecast_hours   = [6]
domains          = ['d01']
thingrid         = ['030km']
channel          = 8

variables = {'OmB_after_BC': [-74.75, 150.25, 0.5, 'C', '#1f77b4']}

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

            for var in variables.keys():

                (range_min, range_max, range_interval, cname, var_color) = variables[var]
                bin_center = np.arange(range_min, range_max + range_interval, range_interval)

                OmB = []
                C   = []
                qc  = []

                for itime in range(0, n_time):

                    itime    = itime + n_spin_up
                    print(itime, end='\r')
                    temp_OmB = ncfile.variables[var][itime, :]
                    temp_C   = ncfile.variables[cname][itime, :]
                    temp_qc  = ncfile.variables['id_qc'][itime, :]
                    index    = temp_OmB < 66666
                    OmB      = OmB + list(temp_OmB[index])
                    C        = C + list(temp_C[index])
                    qc       = qc + list(temp_qc[index])

                filename = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                           str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_' + var + '_SOEM.txt'
                print(filename)

                fsave = open(filename, 'w')
                n_bin = len(bin_center)
                OmB   = np.asarray(OmB)
                C     = np.asarray(C)
                qc    = np.asarray(qc)

                for (ibin, bcenter) in enumerate(bin_center):

                    index = (C >= bcenter - 0.5*range_interval) &  (C < bcenter + 0.5*range_interval) & (qc != -50) & (qc != 50) & (qc != -51) & (qc != 51)

                    n_index = sum(index==True)
                    if n_index == 0:
                        stream = str(bcenter) + ' ' + str(66666) + ' ' + str(n_index) + '\n'
                    else:
                        std    = np.std(OmB[index])
                        stream = str(bcenter) + ' ' + str(std) + ' ' + str(n_index) + '\n'
                    percent = round(ibin*100.0/n_bin, 2)
                    fsave.write(stream)
                    print(percent, '%', end='\r')
                fsave.close()

            ncfile.close()
