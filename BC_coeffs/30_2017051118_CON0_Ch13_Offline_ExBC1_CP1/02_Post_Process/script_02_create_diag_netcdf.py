import os
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

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

            anl_start_time_str = anl_start_time[0].strftime('%Y%m%d%H')
            anl_end_time_str   = anl_end_time[n_period-1].strftime('%Y%m%d%H')
            filename           = dir_out + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                                 str(fhours).zfill(2) + 'h_thingrid.nc'

            ncfile  = Dataset(filename)
            obs_idx = ncfile.variables['obs_idx'][:, :]
            n_time  = len(obs_idx[:, 0])
            n_obs   = len(obs_idx[0, :])
            ncfile.close()
            print('n_time: ', n_time)
            print('n_obs: ', n_obs)

            filename = dir_out + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                       str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '.nc'
            print(filename)

            os.system('rm -rf ' + filename)
            ncfile = Dataset(filename, 'w', format='NETCDF4')
            ncfile.createDimension('n_pred', 14)
            ncfile.createDimension('n_time', n_time)
            ncfile.createDimension('n_obs',  n_obs)
            ncfile.createVariable('time',                   'f8', ('n_time'))
            ncfile.createVariable('cenlat',                 'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('cenlon',                 'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('zsges',                  'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('scan_position',          'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('satellite_zenith_angle', 'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('water_coverage',         'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('land_coverage',          'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('ice_coverage',           'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('snow_coverage',          'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('water_temperature',      'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('land_temperature',       'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('ice_temperature',        'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('snow_temperature',       'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('soil_temperature',       'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('soil_moisture_content',  'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('land_type',              'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('wind_speed',             'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('slons',                  'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('slats',                  'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('BT_obs_before_BC',       'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('BT_obs_after_BC',        'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('OmB_before_BC',          'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('OmB_after_BC',           'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('BT_bkg',                 'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('errinv',                 'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('id_qc',                  'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('error0',                 'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('tlapchn',                'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('cld_rbc_idx',            'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('clr_rbc_idx',            'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('cldeff_obs',             'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('cldeff_bkg',             'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('clreff_bkg',             'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('bias',                   'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('C',                      'f8', ('n_time', 'n_obs'))
            ncfile.createVariable('predbias',               'f8', ('n_pred', 'n_time', 'n_obs'))

            time_now = anl_start_time[0]
            itime    = 0

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

                ncfile.variables['time'][itime] = int(time_now_str)

                obs   = 0
                iline = 0
                a     = open(results_ges)
                for line in a:

                    if iline%n_diag == 0:
                        tmp   = line.split()
                        index = np.where(obs_idx[itime, :] == obs)
                        iobs  = index[0][-1]
                        obs   = obs + 1
                        ncfile.variables['cenlat'][itime, iobs]        = round(float(tmp[0]), 10)
                        ncfile.variables['cenlon'][itime, iobs]        = round(float(tmp[1])-360.0, 10)
                        ncfile.variables['zsges'][itime, iobs]         = round(float(tmp[2]), 10)
                        ncfile.variables['scan_position'][itime, iobs] = round(float(tmp[4]), 10)

                    if iline%n_diag == 1:
                        tmp = line.split()
                        ncfile.variables['satellite_zenith_angle'][itime, iobs] = round(float(tmp[0]), 10)

                    if iline%n_diag == 2:
                        tmp = line.split()
                        ncfile.variables['water_coverage'][itime, iobs]    = round(float(tmp[0]), 10)
                        ncfile.variables['land_coverage'][itime, iobs]     = round(float(tmp[1]), 10)
                        ncfile.variables['ice_coverage'][itime, iobs]      = round(float(tmp[2]), 10)
                        ncfile.variables['snow_coverage'][itime, iobs]     = round(float(tmp[3]), 10)
                        ncfile.variables['water_temperature'][itime, iobs] = round(float(tmp[4]), 10)

                    if iline%n_diag == 3:
                        tmp = line.split()
                        ncfile.variables['land_temperature'][itime, iobs]      = round(float(tmp[0]), 10)
                        ncfile.variables['ice_temperature'][itime, iobs]       = round(float(tmp[1]), 10)
                        ncfile.variables['snow_temperature'][itime, iobs]      = round(float(tmp[2]), 10)
                        ncfile.variables['soil_temperature'][itime, iobs]      = round(float(tmp[3]), 10)
                        ncfile.variables['soil_moisture_content'][itime, iobs] = round(float(tmp[4]), 10)

                    if iline%n_diag == 4:
                        tmp = line.split()
                        ncfile.variables['land_type'][itime, iobs]  = round(float(tmp[0]), 10)
                        ncfile.variables['wind_speed'][itime, iobs] = round(float(tmp[3]), 10)

                    if iline%n_diag == 5:
                        tmp = line.split()
                        ncfile.variables['slons'][itime, iobs] = round(float(tmp[1]), 10)
                        ncfile.variables['slats'][itime, iobs] = round(float(tmp[2]), 10)

                    if iline%n_diag == n_diagbufr + n_diagbufrchan*(channel-7):
                        tmp = line.split()
                        ncfile.variables['BT_obs_before_BC'][itime, iobs] = round(float(tmp[0]), 10)
                        ncfile.variables['OmB_after_BC'][itime, iobs]     = round(float(tmp[1]), 10)
                        ncfile.variables['OmB_before_BC'][itime, iobs]    = round(float(tmp[2]), 10)
                        ncfile.variables['BT_bkg'][itime, iobs]           = round(float(tmp[0]) - float(tmp[2]), 10)
                        ncfile.variables['errinv'][itime, iobs]           = round(float(tmp[3]), 10)
                        ncfile.variables['id_qc'][itime, iobs]            = round(float(tmp[4]), 10)
                        ncfile.variables['bias'][itime, iobs]             = ncfile.variables['OmB_before_BC'][itime, iobs] - \
                                                                            ncfile.variables['OmB_after_BC'][itime, iobs]
                        ncfile.variables['BT_obs_after_BC'][itime, iobs]  = ncfile.variables['BT_obs_before_BC'][itime, iobs] - \
                                                                            ncfile.variables['bias'][itime, iobs]

                    if iline%n_diag == n_diagbufr + n_diagbufrchan*(channel-7) + 1:
                        tmp = line.split()
                        ncfile.variables['error0'][itime, iobs]      = round(float(tmp[0]), 10)
                        ncfile.variables['tlapchn'][itime, iobs]     = round(float(tmp[1]), 10)
                        ncfile.variables['cld_rbc_idx'][itime, iobs] = round(float(tmp[2]), 10)
                        ncfile.variables['predbias'][0, itime, iobs] = round(float(tmp[3]), 10)
                        ncfile.variables['predbias'][1, itime, iobs] = round(float(tmp[4]), 10)

                    if iline%n_diag == n_diagbufr + n_diagbufrchan*(channel-7) + 2:
                        tmp = line.split()
                        ncfile.variables['predbias'][2, itime, iobs] = round(float(tmp[0]), 10)
                        ncfile.variables['predbias'][3, itime, iobs] = round(float(tmp[1]), 10)
                        ncfile.variables['predbias'][4, itime, iobs] = round(float(tmp[2]), 10)
                        ncfile.variables['predbias'][5, itime, iobs] = round(float(tmp[3]), 10)
                        ncfile.variables['predbias'][6, itime, iobs] = round(float(tmp[4]), 10)

                    if iline%n_diag == n_diagbufr + n_diagbufrchan*(channel-7) + 3:
                        tmp = line.split()
                        ncfile.variables['predbias'][ 7, itime, iobs] = round(float(tmp[0]), 10)
                        ncfile.variables['predbias'][ 8, itime, iobs] = round(float(tmp[1]), 10)
                        ncfile.variables['predbias'][ 9, itime, iobs] = round(float(tmp[2]), 10)
                        ncfile.variables['predbias'][10, itime, iobs] = round(float(tmp[3]), 10)
                        ncfile.variables['predbias'][11, itime, iobs] = round(float(tmp[4]), 10)

                    if iline%n_diag == n_diagbufr + n_diagbufrchan*(channel-7) + 4:
                        tmp = line.split()
                        ncfile.variables['predbias'][12, itime, iobs] = round(float(tmp[0]), 10)
                        ncfile.variables['predbias'][13, itime, iobs] = round(float(tmp[1]), 10)
                        ncfile.variables['clr_rbc_idx'][itime, iobs]  = round(float(tmp[2]), 10)
                        ncfile.variables['cldeff_obs'][itime, iobs]   = round(float(tmp[3]), 10)
                        ncfile.variables['cldeff_bkg'][itime, iobs]   = round(float(tmp[4]), 10)

                    if iline%n_diag == n_diagbufr + n_diagbufrchan*(channel-7) + 5:
                        tmp = line.split()
                        ncfile.variables['clreff_bkg'][itime, iobs] = round(float(tmp[0]), 10)
                        ncfile.variables['C'][itime, iobs]          = 0.5*abs(ncfile.variables['cldeff_obs'][itime, iobs]) + \
                                                                      0.5*abs(ncfile.variables['cldeff_bkg'][itime, iobs])

                    iline  = iline + 1
                    n_read = math.floor(iline/n_diag)
                    #print(100*n_read/n_obs, end='\r')

                itime    = itime + 1
                time_now = time_now + datetime.timedelta(hours = cycling_interval)

            ncfile.close()
