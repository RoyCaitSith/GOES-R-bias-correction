import os
import math
import datetime
import numpy as np
from netCDF4 import Dataset

dir_GOES   = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main   = dir_GOES + '/24_Revision/BC_coeffs/28_2020082200_CON0_Ch13_Offline_ExBC1_CP1'
dir_netcdf = dir_main + '/02_Post_Process/2020082200_06h'
dir_save   = dir_main + '/01_Var_BC/save_files'

anl_start_time   = [datetime.datetime(2020, 8, 22,  0, 0, 0)]
anl_end_time     = [datetime.datetime(2020, 8, 23, 18, 0, 0)]
cycling_interval = 6
channel          = 8
forecast_hours   = [6]
domains          = ['d01']
thingrid         = ['030km']
periods          = {'Spin-up': (10, 0.025)}
n_period         = len(periods.keys())

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

            anl_start_time_str = anl_start_time[0].strftime('%Y%m%d%H')
            anl_end_time_str   = anl_end_time[n_period-1].strftime('%Y%m%d%H')

            filename = dir_netcdf + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                       str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '.nc'
            print(filename)

            ncfile   = Dataset(filename)
            predbias = ncfile.variables['predbias'][:, :, :]
            time     = ncfile.variables['time'][:]
            C        = ncfile.variables['C'][:,:]
            ncfile.close()

            n_pred = len(predbias[:, 0, 0])
            n_time = len(predbias[0, :, 0])
            n_obs  = len(predbias[0, 0, :])

            filename = dir_netcdf + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                       str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_pred.nc'
            print(filename)

            ncfile = Dataset(filename, 'w', format='NETCDF4')
            ncfile.createDimension('n_pred', n_pred)
            ncfile.createDimension('n_time', n_time)
            ncfile.createDimension('n_obs',  n_obs)
            ncfile.createVariable('time',     'f8', ('n_time'))
            ncfile.createVariable('predchan', 'f8', ('n_pred', 'n_time'))
            ncfile.createVariable('predbias', 'f8', ('n_pred', 'n_time', 'n_obs'))
            ncfile.createVariable('pred',     'f8', ('n_pred', 'n_time', 'n_obs'))

            ncfile.variables['time'][:] = time
            ncfile.variables['predbias'][:, :, :] = predbias

            time_now = anl_start_time[0]
            itime    = 0

            while time_now <= anl_end_time[n_period-1]:

                time_now_str = time_now.strftime('%Y%m%d%H')
                ftime        = time_now + datetime.timedelta(hours = fhours)
                ftime_str    = ftime.strftime('%Y%m%d%H')

                for idpk, pk in enumerate(list(periods.keys())):
                    if time_now >= anl_start_time[idpk] and time_now <= anl_end_time[idpk]:
                        ict_str = str(periods[pk][0]).zfill(2)

                #file_satbias = dir_save + '/' + time_now_str + '/satbias_in.' + ftime_str + '.' + dom
                file_satbias = dir_save + '/' + time_now_str + '_' + ict_str + '/satbias_in.' + ftime_str + '.' + dom
                print(file_satbias)

                a     = open(file_satbias)
                iline = 0
                for line in a:
                    iline = iline + 1
                    if iline == 9653 + (channel-8)*3 + 0:
                        temp = line.replace('\n', '')
                    if iline == 9653 + (channel-8)*3 + 1:
                        temp = temp + ' ' + line
                        pred = temp.split()
                        for idp, pd in enumerate(pred):
                            ncfile.variables['predchan'][idp, itime] = float(pd)
                            ncfile.variables['pred'][idp, itime, :]  = ncfile.variables['predbias'][idp, itime, :]/float(pd)
                a.close()

                itime    = itime + 1
                time_now = time_now + datetime.timedelta(hours = cycling_interval)

            ncfile.variables['pred'][12,:,:] = C
            ncfile.variables['pred'][13,:,:] = C/20.0
            #print(ncfile.variables['pred'][1,:,:])
            #print(ncfile.variables['pred'][13,:,:])

            for idp in range(0, n_pred):
                print(idp, np.nanmin(ncfile.variables['pred'][idp, :, :]), np.nanmax(ncfile.variables['pred'][idp, :, :]))

            ncfile.close()
