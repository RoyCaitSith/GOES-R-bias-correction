import os
import datetime
import numpy as np
from netCDF4 import Dataset
from scipy.interpolate import griddata

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/24_Revision/BC_coeffs/04_estimate_SOEM_sea'
dir_netcdf = dir_main + '/02_Post_Process/2017051118_06h'
dir_statis = dir_main + '/02_Post_Process/2017051118_06h'
dir_save   = dir_main + '/02_Post_Process/2017051118_06h'
#dir_netcdf = dir_main + '/02_Post_Process/2020082200_06h'
#dir_statis = dir_main + '/02_Post_Process/2020082200_06h'
#dir_save   = dir_main + '/02_Post_Process/2020082200_06h'

anl_start_time   = datetime.datetime(2017, 5, 11, 18, 0, 0)
anl_end_time     = datetime.datetime(2017, 6, 24, 18, 0, 0)
#anl_start_time   = datetime.datetime(2020, 8, 22,  0, 0, 0)
#anl_end_time     = datetime.datetime(2020, 8, 23, 18, 0, 0)

#2017051118_06h
cclr = 3.000
ccld = 25.00
eclr = 1.750
ecld = 10.55

#2020082206_06h
#cclr = 2.500
#ccld = 23.50
#eclr = 1.750
#ecld = 12.00

cycling_interval = 6
forecast_hours   = [6]
domains          = ['d01']
thingrid         = ['030km']
channel          = 8

statuses  = ['before_BC']

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

            anl_start_time_str = anl_start_time.strftime('%Y%m%d%H')
            anl_end_time_str   = anl_end_time.strftime('%Y%m%d%H')

            filename = dir_netcdf + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                       str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '.nc'
            print(filename)

            ncfile   = Dataset(filename)
            var_temp = ncfile.variables['OmB_before_BC'][:, :]
            n_time   = len(var_temp[:, 0])
            n_obs    = len(var_temp[0, :])

            fileoutput = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                         str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_normalized_OmB.nc'
            print(fileoutput)

            os.system('rm -rf ' + fileoutput)
            ncfileoutput = Dataset(fileoutput, 'w', format='NETCDF4')
            ncfileoutput.createDimension('n_status', len(statuses))
            ncfileoutput.createDimension('n_time', n_time)
            ncfileoutput.createDimension('n_obs',  n_obs)
            ncfileoutput.createVariable('time', 'f8', ('n_time'))
            ncfileoutput.createVariable('C',                    'f8', ('n_status', 'n_time', 'n_obs'))
            ncfileoutput.createVariable('normalized_OmB',       'f8', ('n_status', 'n_time', 'n_obs'))
            ncfileoutput.createVariable('observation_error',    'f8', ('n_status', 'n_time', 'n_obs'))
            ncfileoutput.createVariable('all_sky_scaled_OmB',   'f8', ('n_status', 'n_time', 'n_obs'))

            ncfileoutput.variables['time'][:] = ncfile.variables['time'][:]

            std_OmB = np.zeros((len(statuses), n_obs))
            for ids, status in enumerate(statuses):
                filename = dir_statis + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                           str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_OmB_' + status + '_statistics.txt'
                temp     = []
                a        = open(filename)
                for line in a:
                    item = line.replace('\n', '')
                    temp.append(float(item))
                a.close()
                std_OmB[ids, :] = temp[2]

            print(std_OmB)

            for itime in range(0, n_time):

                OmB_before_BC = ncfile.variables['OmB_before_BC'][itime, :]
                C_temp        = ncfile.variables['C'][itime, :]

                index = OmB_before_BC < 66666

                if np.sum(index==True) > 0:

                    ncfileoutput.variables['C'][0, itime, index] = C_temp[index]
                    ncfileoutput.variables['normalized_OmB'][0, itime, index] = OmB_before_BC[index]/std_OmB[0, index]

                    a_Cy = (eclr-ecld)/(cclr-ccld)
                    b_Cy = cclr-eclr/a_Cy
                    min_Cy = eclr
                    max_Cy = ecld

                    Cy = np.zeros((n_obs))
                    for idc, C in enumerate(C_temp):
                        if C < 66666:
                            Cy[idc] = np.min([np.max([a_Cy*(C-b_Cy), min_Cy]), max_Cy])

                    ncfileoutput.variables['observation_error'][0, itime, index] = Cy[index]
                    ncfileoutput.variables['all_sky_scaled_OmB'][0, itime, index] = OmB_before_BC[index]/Cy[index]

                    print(itime, end='\r')

            ncfile.close()
            ncfileoutput.close()
