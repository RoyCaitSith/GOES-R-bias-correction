import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import os, sys
import datetime
import numpy as np
from wrf import getvar, interplevel, latlon_coords
from netCDF4 import Dataset
from scipy.interpolate import griddata

#name = 'Cindy'
name = 'Laura'

#exp_name = 'ASRC04'
#exp_name = 'ASRBC0C04'
#exp_name = 'ASRBC1C04'
#exp_name = 'ASRBC4C04'
#exp_name = 'ASRC12'
#exp_name = 'ASRBC0C12'
#exp_name = 'ASRBC1C12'
#exp_name = 'ASRBC4C12'
#exp_name = 'ASRFDC12'
#exp_name = 'ASRCLDC12'
#exp_name = 'ASRBC0CLDC12'
#exp_name = 'ASRBC1CLDC12'
exp_name = 'ASRBC4CLDC12'

dir_wrfout = []
dir_work = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/24_Revision'
dir_main = dir_work + '/increment'
dir_wrfout.append('/'.join([dir_work, 'cycling_da', 'Data', name, exp_name, 'bkg']))
dir_wrfout.append('/'.join([dir_work, 'cycling_da', 'Data', name, exp_name, 'da']))

domains = ['d01']
cycling_interval = 6

if 'Cindy' in name:
    anl_start_time = datetime.datetime(2017, 6, 20,  6, 0, 0)
    anl_end_time   = datetime.datetime(2017, 6, 20,  6, 0, 0)
if 'Laura' in name:
    anl_start_time = datetime.datetime(2020, 8, 24,  6, 0, 0)
    anl_end_time   = datetime.datetime(2020, 8, 24,  6, 0, 0)
anl_end_time   = anl_start_time + datetime.timedelta(hours=6.0*(int(exp_name[-2:])-1))

analysis_time  = anl_end_time - anl_start_time
analysis_hours = analysis_time.days*24.0 + analysis_time.seconds/3600.0
n_time = int(analysis_hours/cycling_interval) + 1
print(n_time)

variables = {}
variables.update({'ua':     [[925, 850, 700, 500, 300, 200], 'ms-1']})
variables.update({'va':     [[925, 850, 700, 500, 300, 200], 'ms-1']})
variables.update({'temp':   [[925, 850, 700, 500, 300, 200],    'K']})
variables.update({'QVAPOR': [[925, 850, 700, 500, 300, 200], 'null']})
variables.update({'QCLOUD': [[925, 850, 700, 500, 300, 200], 'null']})
variables.update({'QICE':   [[925, 850, 700, 500, 300, 200], 'null']})
variables.update({'QRAIN':  [[925, 850, 700, 500, 300, 200], 'null']})
variables.update({'QSNOW':  [[925, 850, 700, 500, 300, 200], 'null']})
variables.update({'QGRAUP': [[925, 850, 700, 500, 300, 200], 'null']})
variables.update({'rh':     [[925, 850, 700, 500, 300, 200], 'null']})
variables.update({'slp':    [[0],                             'hPa']})

for dom in domains:
    for var in variables.keys():

        (levels, unit) = variables[var]
        n_level = len(levels)

        filename = dir_main + '/' + name + '/' + exp_name + '/' + var + '_da_' + dom + '.nc'
        os.system('rm -rf ' + filename)
        print(filename)

        for idt in range(0, n_time):

            time_now = anl_start_time + datetime.timedelta(hours = idt*cycling_interval)
            print(time_now)

            wrfout_bkg = dir_wrfout[0] + '/wrfout_' + dom + '_' + time_now.strftime('%Y-%m-%d_%H:00:00')
            wrfout_anl = dir_wrfout[1] + '/wrf_inout.' + time_now.strftime('%Y%m%d%H') + '.' + dom

            ncfile = Dataset(wrfout_bkg)
            p_bkg  = getvar(ncfile, 'pressure')
            if unit == 'null':
                var_bkg = getvar(ncfile, var)
            else:
                var_bkg = getvar(ncfile, var, units=unit)
            ncfile.close()

            ncfile = Dataset(wrfout_anl)
            p_anl  = getvar(ncfile, 'pressure')
            if unit == 'null':
                var_anl = getvar(ncfile, var)
            else:
                var_anl = getvar(ncfile, var, units=unit)
            ncfile.close()

            lat, lon = latlon_coords(p_bkg)
            (n_lat, n_lon) = lat.shape

            if idt == 0:

                ncfile_output = Dataset(filename, 'w', format='NETCDF4')
                ncfile_output.createDimension('n_time',  n_time)
                ncfile_output.createDimension('n_level', n_level)
                ncfile_output.createDimension('n_wrf',   2)
                ncfile_output.createDimension('n_lat',   n_lat)
                ncfile_output.createDimension('n_lon',   n_lon)
                ncfile_output.createVariable('level', 'f8', ('n_level'))
                ncfile_output.createVariable('lat',   'f8', ('n_lat',  'n_lon'))
                ncfile_output.createVariable('lon',   'f8', ('n_lat',  'n_lon'))
                ncfile_output.createVariable(var,     'f8', ('n_time', 'n_level', 'n_wrf', 'n_lat', 'n_lon'))
                ncfile_output.variables['level'][:] = levels
                ncfile_output.variables['lat'][:,:] = lat
                ncfile_output.variables['lon'][:,:] = lon
                ncfile_output.description           = var

            if 0 in levels:
                ncfile_output.variables[var][idt,0,0,:,:] = var_bkg
                ncfile_output.variables[var][idt,0,1,:,:] = var_anl
            else:
                temp_bkg = interplevel(var_bkg, p_bkg, levels)
                temp_anl = interplevel(var_anl, p_anl, levels)
                for idl, lev in enumerate(levels):
                    ncfile_output.variables[var][idt,idl,0,:,:] = temp_bkg[idl,:,:]
                    ncfile_output.variables[var][idt,idl,1,:,:] = temp_anl[idl,:,:]

        ncfile_output.close()
