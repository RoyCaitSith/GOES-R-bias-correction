import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import re
import sys
import time
import shutil
import datetime
import numpy as np
from wrf import getvar, interplevel, latlon_coords
from netCDF4 import Dataset

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
exp_name = 'ASRBC0CLDC12'
#exp_name = 'ASRBC1CLDC12'
#exp_name = 'ASRBC4CLDC12'

case = name + '_' + exp_name
print(case)

dir_exp = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/24_Revision'
dir_scr = '/scratch/general/lustre/u1237353'
dir_bkg = '/'.join([dir_exp, 'cycling_da', 'Data', name, exp_name, 'bkg'])
dir_out = '/'.join([dir_exp, 'track_intensity', name, exp_name])

if 'Cindy' in case:
    anl_time_str = datetime.datetime(2017, 6, 20,  0, 0, 0)
    anl_time_end = datetime.datetime(2017, 6, 20,  6, 0, 0)
if 'Laura' in case:
    anl_time_str = datetime.datetime(2020, 8, 24,  0, 0, 0)
    anl_time_end = datetime.datetime(2020, 8, 24,  6, 0, 0)

anl_time_end      = anl_time_end + datetime.timedelta(hours=6.0*(int(exp_name[-2:])-1))
forecast_time_end = anl_time_end + datetime.timedelta(hours=48.0)
cycling_interval  = 6
Domain            = 'd01'

os.system('mkdir ' + dir_out)
dir_out = dir_out + '/wrfprd'
os.system('mkdir ' + dir_out)

anl_tstr = anl_time_str.strftime('%Y%m%d%H')
time_str = anl_time_str.strftime('%Y-%m-%d_%H:00:00')
dir_in   = '/'.join([dir_scr, case, anl_tstr])
print('time start: ', time_str)
forecast_time_now = anl_time_str
while forecast_time_now <= forecast_time_end:

    print('Copy the wrfout files to wrfprd at ', forecast_time_now)
    time        = forecast_time_now.strftime('%Y%m%d%H')
    wrfout_time = forecast_time_now.strftime('%Y-%m-%d_%H:00:00')
    wrfout_name = 'wrfout_' + Domain + '_' + wrfout_time
    wrfout      = dir_bkg + '/' + wrfout_name
    os.system('cp ' + wrfout + ' ' + dir_out)
    print(wrfout)

    wrfout_read = Dataset(dir_out + '/' + wrfout_name, 'r+')
    wrfout_read.START_DATE = time_str
    wrfout_read.SIMULATION_START_DATE = time_str

    forecast_time_now = forecast_time_now + datetime.timedelta(hours = cycling_interval)

#while forecast_time_now <= forecast_time_end:

    #print('Copy the wrfout files to wrfprd at ', forecast_time_now)
    #time        = forecast_time_now.strftime('%Y%m%d%H')
    #wrfout_time = forecast_time_now.strftime('%Y-%m-%d_%H:00:00')
    #wrfout_name = 'wrfout_' + Domain + '_' + wrfout_time
    #wrfout      = dir_in + '/' + wrfout_name
    #os.system('cp ' + wrfout + ' ' + dir_out)
    #print(wrfout)

    #wrfout_read = Dataset(dir_out + '/' + wrfout_name, 'r+')
    #wrfout_read.START_DATE = time_str
    #wrfout_read.SIMULATION_START_DATE = time_str

    #forecast_time_now = forecast_time_now + datetime.timedelta(hours = cycling_interval)
