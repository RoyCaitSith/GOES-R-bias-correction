import os
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
#cases.update({'IMERG': 4})
#cases.update({'ASR': 4})
#cases.update({'ASRBC0': 4})
#cases.update({'ASRBC1': 4})
#cases.update({'ASRBC4': 4})
cases.update({'IMERG': 12})
#cases.update({'ASR': 12})
#cases.update({'ASRBC0': 12})
cases.update({'ASRBC1': 12})
cases.update({'ASRBC4': 12})
cases.update({'ASRFD': 12})
#cases.update({'ASRCLD': 12})
#cases.update({'ASRBC0CLD': 12})
cases.update({'ASRBC1CLD': 12})
cases.update({'ASRBC4CLD': 12})

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
            filename = filename + '/rainfall_6h_' + dom + '.nc'
            os.system('rm -rf ' + filename)
            print(filename)

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
                    IMERG_index = (IMERG_lat < lat_limit[dom][1] + 5.0) & (IMERG_lat > lat_limit[dom][0] - 5.0) & \
                                  (IMERG_lon < lon_limit[dom][1] + 5.0) & (IMERG_lon > lon_limit[dom][0] - 5.0)

                    IMERG_prep_1d = IMERG_prep[IMERG_index]
                    IMERG_lat_1d  = IMERG_lat[IMERG_index]
                    IMERG_lon_1d  = IMERG_lon[IMERG_index]

                    IMERG_lat       = f['Grid']['lat'][:]
                    IMERG_lon       = f['Grid']['lon'][:]
                    IMERG_lat_index = (IMERG_lat < lat_limit[dom][1] + 5.0) & (IMERG_lat > lat_limit[dom][0] - 5.0)
                    IMERG_lon_index = (IMERG_lon < lon_limit[dom][1] + 5.0) & (IMERG_lon > lon_limit[dom][0] - 5.0)
                    n_lat           = IMERG_lat[IMERG_lat_index].shape[0]
                    n_lon           = IMERG_lon[IMERG_lon_index].shape[0]

                    IMERG_lat_2d  = np.transpose(np.reshape(IMERG_lat_1d,  (n_lon, n_lat)))
                    IMERG_lon_2d  = np.transpose(np.reshape(IMERG_lon_1d,  (n_lon, n_lat)))
                    IMERG_prep_2d = np.transpose(np.reshape(IMERG_prep_1d, (n_lon, n_lat)))

                    if idt == 0:

                        ncfile_output = Dataset(filename, 'w', format='NETCDF4')
                        ncfile_output.createDimension('n_time', n_time)
                        ncfile_output.createDimension('n_lat',  n_lat)
                        ncfile_output.createDimension('n_lon',  n_lon)
                        ncfile_output.createVariable('lat',      'f8', ('n_lat', 'n_lon'))
                        ncfile_output.createVariable('lon',      'f8', ('n_lat', 'n_lon'))
                        ncfile_output.createVariable('rainfall', 'f8', ('n_time', 'n_lat', 'n_lon'))

                    ncfile_output.variables['lat'][:,:]          = IMERG_lat_2d
                    ncfile_output.variables['lon'][:,:]          = IMERG_lon_2d
                    ncfile_output.variables['rainfall'][idt,:,:] = IMERG_prep_2d

                    print(np.nanmax(ncfile_output.variables['rainfall'][idt,:,:]))
                    print(np.nanmin(ncfile_output.variables['rainfall'][idt,:,:]))

                else:

                    dir_wrfout = dir_GOES + '/24_Revision/cycling_da/Data/' + name + '/' + casename + '/bkg'
                    #dir_wrfout = '/scratch/general/lustre/u1237353/' + name + '_' + casename + '/2017062000'
                    #dir_wrfout = '/scratch/general/lustre/u1237353/' + name + '_' + casename + '/2020082400'

                    time_0   = time_now + datetime.timedelta(hours = -6.0)
                    time_1   = time_now + datetime.timedelta(hours =  0.0)
                    wrfout_0 = dir_wrfout + '/wrfout_' + dom + '_' + time_0.strftime('%Y-%m-%d_%H:%M:00')
                    wrfout_1 = dir_wrfout + '/wrfout_' + dom + '_' + time_1.strftime('%Y-%m-%d_%H:%M:00')
                    print(wrfout_0)
                    print(wrfout_1)

                    ncfile   = Dataset(wrfout_0)
                    RAINNC_0 = getvar(ncfile, 'RAINNC')
                    RAINC_0  = getvar(ncfile, 'RAINC')
                    ncfile.close()

                    ncfile   = Dataset(wrfout_1)
                    RAINNC_1 = getvar(ncfile, 'RAINNC')
                    RAINC_1  = getvar(ncfile, 'RAINC')
                    ncfile.close()

                    lat, lon       = latlon_coords(RAINNC_0)
                    (n_lat, n_lon) = lat.shape

                    if time_0 == anl_end_time and case[8:] in dir_wrfout:
                        RAINNC_0 = 0.0
                        RAINC_0  = 0.0

                    rainfall = (RAINNC_1 + RAINC_1 - RAINNC_0 - RAINC_0)/6.0

                    if idt == 0:

                        ncfile_output = Dataset(filename, 'w', format='NETCDF4')
                        ncfile_output.createDimension('n_time', n_time)
                        ncfile_output.createDimension('n_lat',  n_lat)
                        ncfile_output.createDimension('n_lon',  n_lon)
                        ncfile_output.createVariable('lat',      'f8', ('n_lat', 'n_lon'))
                        ncfile_output.createVariable('lon',      'f8', ('n_lat', 'n_lon'))
                        ncfile_output.createVariable('rainfall', 'f8', ('n_time', 'n_lat', 'n_lon'))
                        ncfile_output.variables['lat'][:,:] = lat
                        ncfile_output.variables['lon'][:,:] = lon

                    ncfile_output.variables['rainfall'][idt,:,:] = rainfall
                    print(np.nanmax(ncfile_output.variables['rainfall'][idt,:,:]))
                    print(np.nanmin(ncfile_output.variables['rainfall'][idt,:,:]))

            ncfile_output.close()
