import os
import datetime
import numpy as np
from netCDF4 import Dataset
from scipy.interpolate import griddata
from scipy.stats import skew
from scipy.stats import kurtosis
from scipy.stats import pearsonr

dir_GOES   = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main   = dir_GOES + '/24_Revision/BC_coeffs/29_2017051118_CON0_Ch13_Offline_ExBC1_CP0'
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
n_method         = 5
n_scheme         = 2*n_method
statuses         = {'before_BC': [-60.0, 60.0, 0.2],
                    'after_BC':  [-60.0, 60.0, 0.2]}

cclr = [3.000, 3.000]

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

            anl_start_time_str = anl_start_time.strftime('%Y%m%d%H')
            anl_end_time_str   = anl_end_time.strftime('%Y%m%d%H')

            filename = dir_netcdf + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                       str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '.nc'
            print(filename)

            ncfile           = Dataset(filename)
            BT_obs_temp      = [ncfile.variables['BT_obs_before_BC'][n_spin_up:,:], ncfile.variables['BT_obs_after_BC'][n_spin_up:,:]]
            BT_bkg_temp      = [ncfile.variables['BT_bkg'][n_spin_up:,:], ncfile.variables['BT_bkg'][n_spin_up:,:]]
            OmB_temp         = [ncfile.variables['OmB_before_BC'][n_spin_up:,:], ncfile.variables['OmB_after_BC'][n_spin_up:,:]]
            cldeff_obs_temp  = [ncfile.variables['cldeff_obs'][n_spin_up:,:], ncfile.variables['cldeff_obs'][n_spin_up:,:]]
            cldeff_bkg_temp  = [ncfile.variables['cldeff_bkg'][n_spin_up:,:], ncfile.variables['cldeff_bkg'][n_spin_up:,:]]
            C_temp           = [ncfile.variables['C'][n_spin_up:,:], ncfile.variables['C'][n_spin_up:,:]]
            id_qc_temp       = [ncfile.variables['id_qc'][n_spin_up:,:], ncfile.variables['id_qc'][n_spin_up:,:]]
            clr_rbc_idx_temp = [ncfile.variables['clr_rbc_idx'][n_spin_up:,:], ncfile.variables['clr_rbc_idx'][n_spin_up:,:]]
            cld_rbc_idx_temp = [ncfile.variables['cld_rbc_idx'][n_spin_up:,:], ncfile.variables['cld_rbc_idx'][n_spin_up:,:]]
            ncfile.close()

            filename = dir_netcdf + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                       str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_normalized_OmB.nc'
            print(filename)

            ncfile = Dataset(filename)
            time   = ncfile.variables['time'][:]
            n_time = len(time)
            print(n_time)

            for ids, status in enumerate(statuses.keys()):

                print(status)

                for idscheme in range(0, n_scheme):

                    (range_min, range_max, range_interval) = statuses[status]
                    temp     = []
                    filename = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                               str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_' + status + '_histogram_' + \
                               str(idscheme).zfill(2) + '.txt'
                    print(filename)

                    for itime in range(0, n_time):

                        print(itime, end='\r')
                        if idscheme//n_method == 0:
                            var = 'normalized_OmB'
                        elif idscheme//n_method == 1:
                            var = 'all_sky_scaled_OmB'

                        var_temp    = ncfile.variables[var][ids, itime, :]
                        C           = C_temp[ids][itime, :]
                        BT_obs      = BT_obs_temp[ids][itime, :]
                        BT_bkg      = BT_bkg_temp[ids][itime, :]
                        OmB         = OmB_temp[ids][itime, :]
                        id_qc       = id_qc_temp[ids][itime, :]
                        cldeff_obs  = cldeff_obs_temp[ids][itime, :]
                        cldeff_bkg  = cldeff_bkg_temp[ids][itime, :]
                        clr_rbc_idx = clr_rbc_idx_temp[ids][itime, :]
                        cld_rbc_idx = cld_rbc_idx_temp[ids][itime, :]

                        if idscheme%n_method == 0:
                            index = (var_temp < 66666) & (id_qc != -50) & (id_qc != 50) & (id_qc != -51) & (id_qc != 51)
                        elif idscheme%n_method == 1:
                            index = (var_temp < 66666) & (id_qc != -50) & (id_qc != 50) & (id_qc != -51) & (id_qc != 51) & (clr_rbc_idx == 1)
                        elif idscheme%n_method == 2:
                            index = (var_temp < 66666) & (id_qc != -50) & (id_qc != 50) & (id_qc != -51) & (id_qc != 51) & (clr_rbc_idx == 0)
                        elif idscheme%n_method == 3:
                            index = (var_temp < 66666) & (id_qc != -50) & (id_qc != 50) & (id_qc != -51) & (id_qc != 51) & (clr_rbc_idx == 0) & (C <= 55.0)
                        elif idscheme%n_method == 4:
                            index = (var_temp < 66666) & (id_qc != -50) & (id_qc != 50) & (id_qc != -51) & (id_qc != 51) & (clr_rbc_idx == 0) & (C > 55.0)

                        temp = temp + list(var_temp[index])

                    fsave   = open(filename, 'w')
                    np_temp = np.asarray(temp)
                    print(len(np_temp))
                    print(max(np_temp))
                    print(min(np_temp))

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

                    bins = np.arange(range_min-0.5*range_interval, range_max+range_interval, range_interval)
                    hist, bin_edges = np.histogram(np_temp, bins, density=False)

                    for hi in hist:
                        fsave.write(str(hi)+'\n')
                    fsave.close()

            ncfile.close()
