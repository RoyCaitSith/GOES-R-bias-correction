import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import h5py
import datetime
import numpy as np
import pandas as pd
from wrf import getvar, latlon_coords
from netCDF4 import Dataset
from scipy.interpolate import griddata

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/24_Revision/rainfall'

#name = 'Cindy'
name = 'Laura'

cases = {}
#cases.update({'IMERG':  4})
cases.update({'IMERG': 12})

if 'Cindy' in name:
    forecast_time  = datetime.datetime(2017, 6, 20,  0, 0, 0)
    anl_start_time = datetime.datetime(2017, 6, 20,  6, 0, 0)
    anl_end_time   = datetime.datetime(2017, 6, 20,  6, 0, 0)
if 'Laura' in name:
    forecast_time  = datetime.datetime(2020, 8, 24,  0, 0, 0)
    anl_start_time = datetime.datetime(2020, 8, 24,  6, 0, 0)
    anl_end_time   = datetime.datetime(2020, 8, 24,  6, 0, 0)

domains = ['d02']
cycling_interval = 6
forecast_hours = 48
n_time = int(forecast_hours/cycling_interval)

for dom in domains:

    domain_file = dir_GOES + '/24_Revision/track_intensity/sample/wrfout_' + dom + '_2017-06-20_00:00:00'
    domain_data = Dataset(domain_file)
    domain_lat  = domain_data.variables['XLAT'][0,:,:]
    domain_lon  = domain_data.variables['XLONG'][0,:,:]
    domain_data.close()
    lon_limit = {dom: [domain_lon[0,0], domain_lon[-1,-1]]}
    lat_limit = {dom: [domain_lat[0,0], domain_lat[-1,-1]]}

    for case in cases.keys():

        (n_cycle) = cases[case]

        for icycle in range(0, n_cycle):

            casename = case + 'C' + str(icycle+1).zfill(2)
            anl_end_time = anl_start_time + datetime.timedelta(hours=6.0*icycle)
            filename = dir_main + '/' + name + '/' + casename
            os.system('mkdir ' + filename)
            filename = filename + '/rainfall_interpolation_6h_' + dom + '.nc'
            os.system('rm -rf ' + filename)
            print(filename)

            ncfile         = Dataset(domain_file)
            p              = getvar(ncfile, 'pressure')
            lat, lon       = latlon_coords(p)
            (n_lat, n_lon) = lat.shape
            ncfile.close()

            ncfile_output = Dataset(filename, 'w', format='NETCDF4')
            ncfile_output.createDimension('n_time', n_time)
            ncfile_output.createDimension('n_lat',  n_lat)
            ncfile_output.createDimension('n_lon',  n_lon)
            ncfile_output.createVariable('lat',      'f8', ('n_lat', 'n_lon'))
            ncfile_output.createVariable('lon',      'f8', ('n_lat', 'n_lon'))
            ncfile_output.createVariable('rainfall', 'f8', ('n_time', 'n_lat', 'n_lon'))
            ncfile_output.variables['lat'][:,:] = lat
            ncfile_output.variables['lon'][:,:] = lon

            for idt in range(0, n_time):

                time_now = anl_end_time + datetime.timedelta(hours = (idt+1)*cycling_interval)
                print(time_now)

                if 'IMERG' in case:

                    IMERG_prep = np.zeros((3600, 1800), dtype=float)

                    for dh in np.arange(-6.0, 0.0, 0.5):

                        time_IMERG = time_now + datetime.timedelta(hours=dh)
                        YYMMDD     = time_IMERG.strftime('%Y%m%d')
                        HHMMSS     = time_IMERG.strftime('%H%M%S')

                        dir_IMERG  = dir_GOES + '/Data/IMERG'
                        info       = os.popen('ls ' + dir_IMERG + '/' + YYMMDD + '/3B-HHR.MS.MRG.3IMERG.' + YYMMDD + '-S' + HHMMSS + '*').readlines()
                        file_IMERG = info[0].replace('\n', '')
                        print(file_IMERG)

                        f          = h5py.File(file_IMERG)
                        IMERG_prep = IMERG_prep + 0.5*f['Grid']['precipitationCal'][0,:,:]

                    IMERG_prep  = IMERG_prep/6.0
                    IMERG_lat   = np.tile(f['Grid']['lat'][:], (3600, 1))
                    IMERG_lon   = np.transpose(np.tile(f['Grid']['lon'][:], (1800, 1)))
                    IMERG_index = (IMERG_lat < lat_limit[dom][1] + 15.0) & (IMERG_lat > lat_limit[dom][0] - 15.0) & \
                                  (IMERG_lon < lon_limit[dom][1] + 15.0) & (IMERG_lon > lon_limit[dom][0] - 15.0)

                    IMERG_prep_1d = IMERG_prep[IMERG_index]
                    IMERG_lat_1d  = IMERG_lat[IMERG_index]
                    IMERG_lon_1d  = IMERG_lon[IMERG_index]
                    ncfile_output.variables['rainfall'][idt,:,:] = griddata((IMERG_lon_1d, IMERG_lat_1d), IMERG_prep_1d, (lon, lat), method='linear')

                    print(np.nanmax(ncfile_output.variables['rainfall'][idt,:,:]))
                    print(np.nanmin(ncfile_output.variables['rainfall'][idt,:,:]))

            ncfile_output.close()
