import os

dir_main = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/24_Revision'
dir_wrf  = '/'.join([dir_main, 'BC_coeffs/01_run_wrf/wrfout_and_wrfrst'])

files = os.popen('ls ' + dir_wrf).readlines()
for info in files:
    time = info.replace('\n', '')
    print(time)

 45             dir_file = '/'.join([dir_main, time, case])
 46             filename = '_'.join([start_time_str, end_time_str, var, dom + '.nc'])
 47             filename = dir_file + '/' + filename
 48             os.system('mkdir '  + dir_file)
 49             os.system('rm -rf ' + filename)
 50             print(filename)
 51
 52             dir_wrfout = '/'.join([dir_CPEX, 'bkg', time, 'Hybrid_082412'])
 53             wrf_file   = '_'.join(['wrfout', dom, start_time.strftime('%Y-%m-%d_%H:00:00')])
 54             wrfout     = '/'.join([dir_wrfout, wrf_file])
 55
 56             ncfile         = Dataset(wrfout)
 57             p              = getvar(ncfile, 'pressure')
 58             lat, lon       = latlon_coords(p)
 59             (n_lat, n_lon) = lat.shape
 60             ncfile.close()
 61
 62             max_lat = np.array(np.max(np.max(lat)))
 63             min_lat = np.array(np.min(np.min(lat)))
 64             max_lon = np.array(np.max(np.max(lon)))
 65             min_lon = np.array(np.min(np.min(lon)))
 66
 67             ncfile_output = Dataset(filename, 'w', format='NETCDF4')
 68             ncfile_output.createDimension('n_time',  n_time)
 69             ncfile_output.createDimension('n_level', n_level)
 70             ncfile_output.createDimension('n_lat',   n_lat)
 71             ncfile_output.createDimension('n_lon',   n_lon)
 72             ncfile_output.createVariable('level', 'f8', ('n_level'))
 73             ncfile_output.createVariable('lat',   'f8', ('n_lat',  'n_lon'))
 74             ncfile_output.createVariable('lon',   'f8', ('n_lat',  'n_lon'))
 75             ncfile_output.createVariable(var,     'f8', ('n_time', 'n_level', 'n_lat', 'n_lon'))
 76
 77             ncfile_output.variables['level'][:] = levels
 78             ncfile_output.variables['lat'][:,:] = lat
 79             ncfile_output.variables['lon'][:,:] = lon
 80             ncfile_output.description = var


variables = {}
variables.update({'ua':      [[925, 850, 700, 600, 500, 300, 200], 'ms-1', 'VGRD_P0_L100_GLL0']})
variables.update({'va':      [[925, 850, 700, 600, 500, 300, 200], 'ms-1', 'VGRD_P0_L100_GLL0']})
variables.update({'avo':     [[925, 850, 700, 600, 500, 300, 200], 's-1',  'ABSV_P0_L100_GLL0']})
variables.update({'rh':      [[925, 850, 700, 600, 500, 300, 200], '%',      'RH_P0_L100_GLL0']})
variables.update({'geopt':   [[925, 850, 700, 600, 500, 300, 200], 'gpm',   'HGT_P0_L100_GLL0']})
