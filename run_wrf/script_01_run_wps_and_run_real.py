import sys
import os
import shutil
import datetime
import numpy as np
from subroutine import file_operations as fo

#name = 'Cindy'
name = 'Laura'

#case = name + '_ASRC04'
#case = name + '_ASRBC0C04'
#case = name + '_ASRBC1C04'
#case = name + '_ASRBC4C04'
#case = name + '_ASRC12'
#case = name + '_ASRBC0C12'
#case = name + '_ASRBC1C12'
#case = name + '_ASRBC4C12'
#case = name + '_ASRFDC12'
#case = name + '_ASRCLDC12'
#case = name + '_ASRBC0CLDC12'
#case = name + '_ASRBC1CLDC12'
case = name + '_ASRBC4CLDC12'

# Set the directories of the input files or procedures
dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/24_Revision/run_wrf'
dir_GFS  = dir_GOES + '/Data/GFS'

# I do not need to set the directories of these files
WRF_dir                 = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng'
namelist_and_script_dir = dir_main + '/namelist_and_script/' + name
namelist_wps_dir        = namelist_and_script_dir + '/namelist.wps'
plotgrids_new_dir       = namelist_and_script_dir + '/plotgrids_new.ncl'
namelist_input_dir      = namelist_and_script_dir + '/namelist.input'
run_wps_dir             = namelist_and_script_dir + '/run_wps.sh'
run_wrf_dir             = namelist_and_script_dir + '/run_wrf.sh'

if 'Cindy' in case:
    initial_time   = datetime.datetime(2017, 6, 20,  0, 0, 0)
    anl_start_time = datetime.datetime(2017, 6, 20,  6, 0, 0)
    anl_end_time   = datetime.datetime(2017, 6, 20,  6, 0, 0)
if 'Laura' in case:
    initial_time   = datetime.datetime(2020, 8, 24,  0, 0, 0)
    anl_start_time = datetime.datetime(2020, 8, 24,  6, 0, 0)
    anl_end_time   = datetime.datetime(2020, 8, 24,  6, 0, 0)

anl_end_time   = anl_start_time + datetime.timedelta(hours=6.0*(int(case[-2:])-1))
analysis_time  = anl_end_time - initial_time
analysis_hours = int(analysis_time.days*24.0 + analysis_time.seconds/3600.0)

wps_interval   = 6
forecast_hours = 48
forecast_hours = forecast_hours + wps_interval

max_dom = 2

# Set the folder name of the new case
time_str     = initial_time.strftime('%Y%m%d%H')
folder_dir   = '/scratch/general/lustre/u1237353/' + case
new_case_dir = folder_dir
print(time_str)

# Set the variables in the namelist.wps
namelist_wps = fo.change_content(namelist_wps_dir)
# Share
start_date     = initial_time
end_date       = anl_end_time + datetime.timedelta(hours = forecast_hours)
start_date_str = "'" + start_date.strftime('%Y-%m-%d_%H:00:00') + "',"
end_date_str   = "'" + end_date.strftime('%Y-%m-%d_%H:00:00') + "',"
start_date_str = start_date_str * max_dom
end_date_str   = end_date_str * max_dom
namelist_wps.substitude_string('max_dom', ' = ', str(max_dom))
namelist_wps.substitude_string('start_date', ' = ', start_date_str)
namelist_wps.substitude_string('end_date', ' = ', end_date_str)
namelist_wps.substitude_string('interval_seconds', ' = ', str(3600*wps_interval))

# Set the variables in the namelist.input
namelist_input = fo.change_content(namelist_input_dir)
# Time_Control
run_days_str  = str((analysis_hours + forecast_hours)//24) + ', '
run_hours_str = str((analysis_hours + forecast_hours)%24) + ', '
YYYY_str      = start_date.strftime('%Y') + ', '
MM_str        = start_date.strftime('%m') + ', '
DD_str        = start_date.strftime('%d') + ', '
HH_str        = start_date.strftime('%H') + ', '
run_days_str  = run_days_str
run_hours_str = run_hours_str
YYYY_str      = YYYY_str * max_dom
MM_str        = MM_str * max_dom
DD_str        = DD_str * max_dom
HH_str        = HH_str * max_dom
namelist_input.substitude_string('run_days', ' = ', run_days_str)
namelist_input.substitude_string('run_hours', ' = ', run_hours_str)
namelist_input.substitude_string('start_year', ' = ', YYYY_str)
namelist_input.substitude_string('start_month', ' = ', MM_str)
namelist_input.substitude_string('start_day', ' = ', DD_str)
namelist_input.substitude_string('start_hour', ' = ', HH_str)

YYYY_str = end_date.strftime('%Y') + ', '
MM_str   = end_date.strftime('%m') + ', '
DD_str   = end_date.strftime('%d') + ', '
HH_str   = end_date.strftime('%H') + ', '
YYYY_str = YYYY_str * max_dom
MM_str   = MM_str * max_dom
DD_str   = DD_str * max_dom
HH_str   = HH_str * max_dom
namelist_input.substitude_string('end_year', ' = ', YYYY_str)
namelist_input.substitude_string('end_month', ' = ', MM_str)
namelist_input.substitude_string('end_day', ' = ', DD_str)
namelist_input.substitude_string('end_hour', ' = ', HH_str)
namelist_input.substitude_string('interval_seconds', ' = ', str(3600*wps_interval))
namelist_input.substitude_string('max_dom', ' = ', str(max_dom) + ', ')

os.system('rm -rf ' + folder_dir)
fo.create_new_case_folder(folder_dir)
print('Create Geogrid_Data in ' + folder_dir)
os.mkdir(folder_dir + '/Geogrid_Data')
print('Create GFS_Boundary_Condition_Data in ' + folder_dir)
os.mkdir(folder_dir + '/GFS_Boundary_Condition_Data')
print('Create Metgrid_Data in ' + folder_dir)
os.mkdir(folder_dir + '/Metgrid_Data')
print('Create Run_WRF in ' + folder_dir)
os.mkdir(folder_dir + '/Run_WRF')
print('Create ' + time_str + ' in ' + folder_dir)
os.mkdir(folder_dir + '/' + time_str)
print('Copy the boundary condition data into GFS_Boundary_Condition_Data')
for fhours in range(0, analysis_hours + wps_interval, wps_interval):
    time_now     = initial_time + datetime.timedelta(hours = fhours)
    time_now_str = time_now.strftime('%Y%m%d%H')
    gfs_name     = dir_GFS + '/gfs.0p25.' + time_now_str + '.f' + str(0).zfill(3) + '.grib2'
    print(gfs_name)
    os.system('cp ' + gfs_name + ' ' + folder_dir + '/GFS_Boundary_Condition_Data')
anl_end_time_str = anl_end_time.strftime('%Y%m%d%H')
for fhours in range(wps_interval, forecast_hours + wps_interval, wps_interval):
    gfs_name = dir_GFS + '/gfs.0p25.' + anl_end_time_str + '.f' + str(fhours).zfill(3) + '.grib2'
    print(gfs_name)
    os.system('cp ' + gfs_name + ' ' + folder_dir + '/GFS_Boundary_Condition_Data')

# Continue to revise the namelist.wps
# Share
namelist_wps.substitude_string('opt_output_from_geogrid_path', ' = ', "'" + new_case_dir + '/Geogrid_Data/' + "'")
# Metgrid
namelist_wps.substitude_string('opt_output_from_metgrid_path', ' = ', "'" + new_case_dir + '/Metgrid_Data/' + "'")
namelist_wps.save_content()

# Continue to revise the namelist.input
namelist_input.substitude_string('input_from_file', ' = ', '.true., ' + '.false., ' * (max_dom-1))
namelist_input.substitude_string('history_outname', ' = ', "'" + new_case_dir + '/' + time_str + '/wrfout_d<domain>_<date>' + "'")
namelist_input.substitude_string('rst_outname', ' = ', "'" + new_case_dir + '/' + time_str + '/wrfrst_d<domain>_<date>' + "'")
namelist_input.save_content()

# Set the variable in the run_wps.sh
run_wps = fo.change_content(run_wps_dir)
run_wps.substitude_string('#SBATCH -J', ' ', time_str[2::])
run_wps.substitude_string('export SCRATCH_DIRECTORY', '=', new_case_dir)
run_wps.save_content()

# Set the variable in the run_wrf.sh
run_wrf = fo.change_content(run_wrf_dir)
run_wrf.substitude_string('#SBATCH -J', ' ', time_str[2::])
run_wrf.substitude_string('export SCRATCH_DIRECTORY', '=', new_case_dir)
run_wrf.save_content()

print('Copy namelist.wps into Run_WRF')
shutil.copy(namelist_wps_dir, folder_dir)
print('Copy plotgrids_new.ncl into Run_WRF')
shutil.copy(plotgrids_new_dir, folder_dir + '/Run_WRF')
print('Copy namelist.input into Run_WRF')
shutil.copy(namelist_input_dir, folder_dir)
print('Copy run_wps.sh into Run_WRF')
shutil.copy(run_wps_dir, folder_dir + '/Run_WRF')
print('Copy run_wrf.sh into Run_WRF')
shutil.copy(run_wrf_dir, folder_dir + '/Run_WRF')
print('\n')
