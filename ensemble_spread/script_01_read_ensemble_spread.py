import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import os, sys
import datetime
import numpy as np
from wrf import getvar, interplevel, latlon_coords
from netCDF4 import Dataset
from scipy.interpolate import griddata

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/17_2020Laura_Experiments/ensemble_spread'
dir_anl  = dir_GOES + '/17_2020Laura_Experiments/da'
dir_inc  = dir_GOES + '/17_2020Laura_Experiments/increment'

cases = ['case_02_ASRCON06hENS50024AugC1']

domains = ['d01']
levels = [925, 850, 700, 500, 300, 200]
n_level = len(levels)

if 'case_02' in cases[0] and '0024Aug' in cases[0]:
    anl_start_time = datetime.datetime(2020, 8, 24,  6, 0, 0)
    anl_end_time   = datetime.datetime(2020, 8, 24,  6, 0, 0)
anl_end_time = anl_start_time + datetime.timedelta(hours=6.0*(int(cases[0][-1])-1))

if '6h' in cases[0]: cycling_interval = 6
analysis_time  = anl_end_time - anl_start_time
analysis_hours = analysis_time.days*24.0 + analysis_time.seconds/3600.0
n_time = int(analysis_hours/cycling_interval) + 1

variables = {}
variables.update({'st': ''})
variables.update({'vp': ''})
variables.update({'tv': ''})
variables.update({'rh': ''})
variables.update({'oz': ''})
variables.update({'cw': ''})
variables.update({'ql': 'QCLOUD'})
variables.update({'qr': 'QRAIN'})
variables.update({'qi': 'QICE'})
variables.update({'qs': 'QSNOW'})
variables.update({'qg': 'QGRAUP'})
(nvar, n_lat, n_lon, n_sig) = (len(variables.keys()), 349, 449, 60)

idv = 0

for dom in domains:
    for case in cases:
        for var in variables.keys():

            wrfvar = variables[var]
            idv = idv + 1
            #print(wrfvar)

            filename = dir_main + '/' + case[0:7] + '/' + case[8:]  + '/' + var + '_' + dom + '.nc'
            print(filename)

            ncfile_output = Dataset(filename, 'w', format='NETCDF4')
            ncfile_output.createDimension('n_wrf',   2)
            ncfile_output.createDimension('n_time',  n_time)
            ncfile_output.createDimension('n_level', n_level)
            ncfile_output.createDimension('n_lat',   n_lat)
            ncfile_output.createDimension('n_lon',   n_lon)
            ncfile_output.createVariable('level', 'f8', ('n_level'))
            ncfile_output.createVariable('lat',   'f8', ('n_lat', 'n_lon'))
            ncfile_output.createVariable('lon',   'f8', ('n_lat', 'n_lon'))
            ncfile_output.createVariable(var,     'f8', ('n_wrf', 'n_time', 'n_level', 'n_lat', 'n_lon'))
            ncfile_output.variables['level'][:] = levels
            ncfile_output.description = var

            if 'q' in var:

                filename = dir_inc + '/' + case[0:7] + '/' + case[8:] + '/' + wrfvar + '_da_' + dom + '.nc'
                ncfile_inc = Dataset(filename)
                temp_inc = ncfile_inc.variables[wrfvar][:,:,0,:,:]
                temp_inc = np.where(temp_inc < 1e-10, 1e-10, 0.05*temp_inc)
                ncfile_inc.close()

            for idt in range(0, n_time):

                time_now = anl_start_time + datetime.timedelta(hours = idt*cycling_interval)
                time_now_str = time_now.strftime('%Y%m%d%H')
                print(time_now)

                file_ens = dir_anl + '/' + case[0:7] + '/' + case[8:] + '/ens_spread_' + time_now_str + '_' + dom + '.grd'
                f = open(file_ens, 'rb')
                reclen = n_lat*n_lon*n_sig

                wrfout_anl = dir_anl + '/' + case[0:7] + '/' + case[8:] + '/wrf_inout.' + time_now.strftime('%Y%m%d%H') + '.' + dom
                ncfile = Dataset(wrfout_anl)
                p = getvar(ncfile, 'pressure')
                ncfile.close()

                lat, lon = latlon_coords(p)
                ncfile_output.variables['lat'][:,:] = lat
                ncfile_output.variables['lon'][:,:] = lon

                if 'q' in var:
                    ncfile_output.variables[var][0,idt,:,:,:] = temp_inc[idt,:,:,:]
                else:
                    ncfile_output.variables[var][0,idt,:,:,:] = 0.0

                temp = np.fromfile(f, dtype='<f4', count=idv*reclen)
                ncfile_output.variables[var][1,idt,:,:,:] = interplevel(temp[(idv-1)*reclen:idv*reclen].reshape(n_sig,n_lat,n_lon), p, levels)

                ncfile_output.close()

                f.close()
