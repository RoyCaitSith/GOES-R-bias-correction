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

schemes = {'00': ['Tlap',          'All-sky Scaled OmB',  4, 'all_sky_scaled_OmB', 0,   -4.0,    4.0,  0.2, -60.0, 60.0, 0.2],
           '01': ['Tlap',          'All-sky Scaled OmB',  4, 'all_sky_scaled_OmB', 1,   -4.0,    4.0,  0.2, -60.0, 60.0, 0.2],
           '02': ['Scan Position', 'All-sky Scaled OmB', 11, 'all_sky_scaled_OmB', 0,  0.025,  1.225, 0.05, -60.0, 60.0, 0.2],
           '03': ['Scan Position', 'All-sky Scaled OmB', 11, 'all_sky_scaled_OmB', 1,  0.025,  1.225, 0.05, -60.0, 60.0, 0.2],
           '04': ['Normalized C',  'All-sky Scaled OmB', 12, 'all_sky_scaled_OmB', 0,   0.50,  100.5,  1.0, -60.0, 60.0, 0.2],
           '05': ['Normalized C',  'All-sky Scaled OmB', 12, 'all_sky_scaled_OmB', 1,   0.50,  100.5,  1.0, -60.0, 60.0, 0.2]}

cclr = [2.50, 2.50]

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

            anl_start_time_str = anl_start_time.strftime('%Y%m%d%H')
            anl_end_time_str   = anl_end_time.strftime('%Y%m%d%H')

            filename = dir_netcdf + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                       str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '.nc'
            print(filename)

            filex = dir_netcdf + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                    str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_pred.nc'
            print(filex)

            filey = dir_netcdf + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                    str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_normalized_OmB.nc'
            print(filey)

            ncfile  = Dataset(filename)
            ncfilex = Dataset(filex)
            ncfiley = Dataset(filey)

            time             = ncfile.variables['time'][n_spin_up:]
            n_time           = len(time)
            cldeff_obs_temp  = abs(ncfile.variables['cldeff_obs'][n_spin_up:,:])
            cldeff_bkg_temp  = abs(ncfile.variables['cldeff_bkg'][n_spin_up:,:])
            id_qc_temp       = ncfile.variables['id_qc'][n_spin_up:,:]
            clr_rbc_idx_temp = ncfile.variables['clr_rbc_idx'][n_spin_up:,:]
            ncfile.close()

            for ids, ids_str in enumerate(schemes.keys()):

                (xname, yname, xid, yvar, yid, xrange_min, xrange_max, xrange_interval, yrange_min, yrange_max, yrange_interval) = schemes[ids_str]

                xvar_value_temp = ncfilex.variables['pred'][xid, n_spin_up:, :]
                yvar_value_temp = ncfiley.variables[yvar][yid, :, :]

                #filename = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                           #str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_pred_histogram2d_' + ids_str + '_All Sky.txt'
                #filename = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                           #str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_pred_histogram2d_' + ids_str + '_Clear Sky.txt'
                filename = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                           str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_pred_histogram2d_' + ids_str + '_Cloudy Sky.txt'
                print(filename)

                (xtemp, ytemp) = ([], [])
                for itime in range(0, n_time):

                    print(itime, end='\r')

                    xvar_value = xvar_value_temp[itime, :]
                    yvar_value = yvar_value_temp[itime, :]

                    cldeff_obs  = cldeff_obs_temp[itime, :]
                    cldeff_bkg  = cldeff_bkg_temp[itime, :]
                    id_qc       = id_qc_temp[itime, :]
                    clr_rbc_idx = clr_rbc_idx_temp[itime, :]

                    if ids >= 0 and ids <= 5:
                        #index = (xvar_value < 66666) & (id_qc != -50) & (id_qc != 50) & (id_qc != -51) & (id_qc != 51)
                        #index = (xvar_value < 66666) & (id_qc != -50) & (id_qc != 50) & (id_qc != -51) & (id_qc != 51) & (clr_rbc_idx == 1)
                        index = (xvar_value < 66666) & (id_qc != -50) & (id_qc != 50) & (id_qc != -51) & (id_qc != 51) & (clr_rbc_idx == 0)

                    xtemp = xtemp + list(xvar_value[index])
                    ytemp = ytemp + list(yvar_value[index])

                xtemp = np.asarray(xtemp)
                ytemp = np.asarray(ytemp)

                xbin_center = np.arange(xrange_min, xrange_max+0.99*xrange_interval, xrange_interval)
                xbins       = np.arange(xrange_min-0.5*xrange_interval, xrange_max+xrange_interval, xrange_interval)
                ybins       = np.arange(yrange_min-0.5*yrange_interval, yrange_max+yrange_interval, yrange_interval)

                ytemp_avg = np.zeros((len(xbin_center)))
                for idxbc, xbc in enumerate(xbin_center):
                    index = (xtemp >= xbins[idxbc]) & (xtemp < xbins[idxbc+1])
                    if np.sum(index==True) > 10:
                        ytemp_avg[idxbc] = np.average(ytemp[index]) - np.average(ytemp)

                hist, xedges, yedges = np.histogram2d(xtemp, ytemp, bins=(xbins, ybins))
                hist = hist.T

                output        = np.zeros((len(ybins), len(xbin_center)))
                output[0][:]  = ytemp_avg.copy()
                output[1:][:] = hist.copy()
                np.savetxt(filename, output)

            ncfilex.close()
            ncfiley.close()
