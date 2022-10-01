import os
import re
import time
import datetime
from subroutine import file_operations as fo

#name = 'Cindy'
name = 'Laura'

exp_name = 'ASRBC0C12'
case = name + '_' + exp_name

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_exp  = dir_GOES + '/24_Revision/cycling_da'
dir_bkg  = dir_exp + '/Data/' + name + '/' + exp_name + '/bkg'
dir_da   = dir_exp + '/Data/' + name + '/' + exp_name + '/da'

if 'Cindy' in case:
    initial_time   = datetime.datetime(2017, 6, 20,  0, 0, 0)
    anl_start_time = datetime.datetime(2017, 6, 20,  6, 0, 0)
    anl_end_time   = datetime.datetime(2017, 6, 20,  6, 0, 0)
if 'Laura' in case:
    initial_time   = datetime.datetime(2020, 8, 24,  0, 0, 0)
    anl_start_time = datetime.datetime(2020, 8, 24,  6, 0, 0)
    anl_end_time   = datetime.datetime(2020, 8, 24,  6, 0, 0)

domains = ['d01']
cycling_interval = 6.0
max_dom = len(domains)
n_cycle = int(case[-2:])-1

for idc in range(0, n_cycle):

    dir_cycle = dir_exp + '/Data/' + name + '/' + exp_name[0:len(exp_name)-2] + str(idc+1).zfill(2)
    dir_bkg_out = dir_cycle + '/bkg'
    dir_da_out = dir_cycle + '/da'
    os.system('mkdir ' + dir_cycle)
    os.system('mkdir ' + dir_bkg_out)
    os.system('mkdir ' + dir_da_out)

    #Copy bkg files
    ctime = initial_time
    anl_end_time = anl_start_time + datetime.timedelta(hours=6.0*idc)
    while ctime <= anl_end_time:
        for dom in domains:
            wrfout_at_dir_bkg = dir_bkg + '/wrfout_' + dom + '_' + ctime.strftime('%Y-%m-%d_%H:%M:00')
            wrfout_at_dir_bkg_out = dir_bkg_out + '/wrfout_' + dom + '_' + ctime.strftime('%Y-%m-%d_%H:%M:00')
            os.system('cp ' + wrfout_at_dir_bkg + ' ' + wrfout_at_dir_bkg_out)
            print(wrfout_at_dir_bkg_out)
        ctime = ctime + datetime.timedelta(hours = cycling_interval)

    #Copy da files
    ctime = anl_start_time
    anl_end_time = anl_start_time + datetime.timedelta(hours=6.0*idc)
    while ctime <= anl_end_time:
        for dom in domains:
            wrfout_at_dir_da = dir_da + '/wrf_inout.' + ctime.strftime('%Y%m%d%H') + '.' + dom
            wrfout_at_dir_da_out = dir_da_out + '/wrf_inout.' + ctime.strftime('%Y%m%d%H') + '.' + dom
            os.system('cp ' + wrfout_at_dir_da + ' ' + wrfout_at_dir_da_out)
            print(wrfout_at_dir_da_out)
        ctime = ctime + datetime.timedelta(hours = cycling_interval)
