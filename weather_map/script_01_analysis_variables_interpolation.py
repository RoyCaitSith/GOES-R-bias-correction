import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import Nio
import os, sys
import datetime
import numpy as np
from wrf import getvar, interplevel, latlon_coords
from netCDF4 import Dataset
from scipy.interpolate import griddata

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_data = dir_GOES + '/Data'
dir_main = dir_GOES + '/24_Revision'

name = 'Cindy'
cases = ['GFS', 'FNL']

domains = ['d01']
cycling_interval = 6
forecast_hours = 48
n_time = 1

if 'Cindy' in name:
    forecast_time  = datetime.datetime(2017, 6, 20,  0, 0, 0)
    anl_start_time = datetime.datetime(2017, 6, 20,  6, 0, 0)
    anl_end_time   = datetime.datetime(2017, 6, 20,  6, 0, 0)

variables = {}
variables.update({'temp': [[200], 'K', 'TMP_P0_L100_GLL0']})

for dom in domains:
    for case in cases:
        for var in variables.keys():

            (levels, unit, GFS_var) = variables[var]
            n_level = len(levels)

            filename = '/'.join([dir_main, 'weather_map', name, case, var + '_' + dom + '.nc'])
            os.system('rm -rf ' + filename)
            print(filename)

            dir_wrfout = '/'.join([dir_main, 'cycling_da', 'Data', name, 'ASRC04', 'bkg'])
            wrfout     = dir_wrfout + '/wrfout_' + dom + '_' + anl_start_time.strftime('%Y-%m-%d_%H:00:00')

            ncfile         = Dataset(wrfout)
            p              = getvar(ncfile, 'pressure')
            lat, lon       = latlon_coords(p)
            (n_lat, n_lon) = lat.shape
            ncfile.close()

            max_lat = np.array(np.max(np.max(lat)))
            min_lat = np.array(np.min(np.min(lat)))
            max_lon = np.array(np.max(np.max(lon)))
            min_lon = np.array(np.min(np.min(lon)))

            ncfile_output = Dataset(filename, 'w', format='NETCDF4')
            ncfile_output.createDimension('n_time',  n_time)
            ncfile_output.createDimension('n_level', n_level)
            ncfile_output.createDimension('n_lat',   n_lat)
            ncfile_output.createDimension('n_lon',   n_lon)
            ncfile_output.createVariable('level', 'f8', ('n_level'))
            ncfile_output.createVariable('lat',   'f8', ('n_lat',  'n_lon'))
            ncfile_output.createVariable('lon',   'f8', ('n_lat',  'n_lon'))
            ncfile_output.createVariable(var,     'f8', ('n_time', 'n_level', 'n_lat', 'n_lon'))

            ncfile_output.variables['level'][:] = levels
            ncfile_output.variables['lat'][:,:] = lat
            ncfile_output.variables['lon'][:,:] = lon
            ncfile_output.description = var

            for idt in range(0, 1):

                time_now = anl_end_time + datetime.timedelta(hours = idt*cycling_interval)
                print(time_now)

                if 'FNL' in case or 'GFS' in case:

                    YYMMDD   = time_now.strftime('%Y%m%d')
                    YYMMDDHH = time_now.strftime('%Y%m%d%H')

                    dir_GFS  = dir_GOES + '/Data/' + case
                    if 'FNL' in case: info = os.popen('ls ' + dir_GFS + '/' + YYMMDD + '/gdas1.fnl0p25.' + YYMMDDHH + '.f00.grib2').readlines()
                    if 'GFS' in case: info = os.popen('ls ' + dir_GFS + '/gfs.0p25.' + YYMMDDHH + '.f000.grib2').readlines()
                    file_GFS = info[0].replace('\n', '')
                    print(file_GFS)

                    GFS_file = Nio.open_file(file_GFS)
                    n_lat    = GFS_file.variables['lat_0'][:].shape[0]
                    n_lon    = GFS_file.variables['lon_0'][:].shape[0]
                    GFS_lat  = np.transpose(np.tile(GFS_file.variables['lat_0'][:], (n_lon, 1)))
                    GFS_lon  = np.tile(GFS_file.variables['lon_0'][:], (n_lat, 1))
                    GFS_lon[GFS_lon > 180.0] = GFS_lon[GFS_lon > 180.0] - 360.0

                    GFS_index = (GFS_lat < max_lat + 15.0) & (GFS_lat > min_lat - 15.0) & \
                                (GFS_lon < max_lon + 15.0) & (GFS_lon > min_lon - 15.0)

                    GFS_lat_1d = GFS_lat[GFS_index]
                    GFS_lon_1d = GFS_lon[GFS_index]

                    GFS_level = GFS_file.variables['lv_ISBL0'][:]/100.0
                    for idl, lev in enumerate(levels):
                        level_index = list(GFS_level).index(lev)
                        GFS_temp    = GFS_file.variables[GFS_var][level_index,:,:]
                        GFS_temp_1d = GFS_temp[GFS_index]
                        ncfile_output.variables[var][idt,idl,:,:] = griddata((GFS_lon_1d, GFS_lat_1d), GFS_temp_1d, (lon, lat), method='linear')

                    GFS_file.close()

            ncfile_output.close()
