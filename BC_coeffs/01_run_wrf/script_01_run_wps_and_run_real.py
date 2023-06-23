import sys
import os
import shutil
import datetime
import numpy as np
from subroutine import file_operations as fo

name = 'Laura'

# Set the directories of the input files or procedures
dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/24_Revision/BC_coeffs/01_run_wrf'
dir_GFS  = dir_GOES + '/Data/GFS'

# I do not need to set the directories of these files
WRF_dir                 = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng'
namelist_and_script_dir = dir_main + '/namelist_and_script/' + name
namelist_wps_dir        = namelist_and_script_dir + '/namelist.wps'
plotgrids_new_dir       = namelist_and_script_dir + '/plotgrids_new.ncl'
namelist_input_dir      = namelist_and_script_dir + '/namelist.input'
run_wrf_dir             = namelist_and_script_dir + '/run_wrf.sh'

if 'Cindy' in name:
    anl_start_time   = datetime.datetime(2017, 5, 11, 18, 0, 0)
    anl_end_time     = datetime.datetime(2017, 6, 24, 18, 0, 0)
if 'Laura' in name:
    anl_start_time   = datetime.datetime(2020, 8, 22,  0, 0, 0)
    anl_end_time     = datetime.datetime(2020, 8, 23, 18, 0, 0)

cycling_interval = 6
wps_interval     = 6
forecast_hours   = 6
max_dom          = 1

time_now = anl_start_time
while time_now <= anl_end_time:

    # Set the folder name of the new case
    time_str     = time_now.strftime('%Y%m%d%H')
    print(time_str)
    folder_dir   = '/scratch/general/lustre/u1237353/CHPC_' + time_str
    new_case_dir = folder_dir

    # Set the variables in the namelist.wps
    namelist_wps = fo.change_content(namelist_wps_dir)
    # Share
    start_date     = time_now
    end_date       = time_now + datetime.timedelta(hours = forecast_hours)
    start_date_str = "'" + start_date.strftime('%Y-%m-%d_%H:00:00') + "',"
    end_date_str   = "'" + end_date.strftime('%Y-%m-%d_%H:00:00') + "',"
    start_date_str = start_date_str * max_dom
    end_date_str   = end_date_str * max_dom
    namelist_wps.substitude_string('max_dom', ' = ', str(max_dom))
    namelist_wps.substitude_string('start_date', ' = ', start_date_str)
    namelist_wps.substitude_string('end_date', ' = ', end_date_str)

    # Set the variables in the namelist.input
    namelist_input = fo.change_content(namelist_input_dir)
    # Time_Control
    run_days_str  = str(forecast_hours//24) + ', '
    run_hours_str = str(forecast_hours%24) + ', '
    YYYY_str      = start_date.strftime('%Y') + ', '
    MM_str        = start_date.strftime('%m') + ', '
    DD_str        = start_date.strftime('%d') + ', '
    HH_str        = start_date.strftime('%H') + ', '
    YYYY_str      = YYYY_str * max_dom
    MM_str        = MM_str * max_dom
    DD_str        = DD_str * max_dom
    HH_str        = HH_str * max_dom
    namelist_input.substitude_string('max_dom', ' = ', str(max_dom))
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

    os.system('rm -rf ' + folder_dir)
    fo.create_new_case_folder(folder_dir)
    print('Create Geogrid_Data in ' + folder_dir)
    os.mkdir(folder_dir + '/Geogrid_Data')
    print('Create GFS_Anl_Boundary_Condition_Data in ' + folder_dir)
    os.mkdir(folder_dir + '/GFS_Anl_Boundary_Condition_Data')
    print('Create Metgrid_Data in ' + folder_dir)
    os.mkdir(folder_dir + '/Metgrid_Data')
    print('Create Run_WRF in ' + folder_dir)
    os.mkdir(folder_dir + '/Run_WRF')
    print('Create ' + time_str + ' in ' + folder_dir)
    os.mkdir(folder_dir + '/' + time_str)
    print('Copy the boundary condition data into GFS_Anl_Boundary_Condition_Data')
    for fhours in range(0, forecast_hours + wps_interval, wps_interval):
        time_wps     = time_now + datetime.timedelta(hours = fhours)
        time_wps_str = time_wps.strftime('%Y%m%d%H')
        gfs_name = dir_GFS + '/gfs.0p25.' + time_wps_str + '.f' + str(0).zfill(3) + '.grib2'
        print(gfs_name)
        os.system('cp ' + gfs_name + ' ' + folder_dir + '/GFS_Anl_Boundary_Condition_Data')

    # Continue to revise the namelist.wps
    # Share
    namelist_wps.substitude_string('opt_output_from_geogrid_path', ' = ', "'" + new_case_dir + '/Geogrid_Data/' + "'")
    # Metgrid
    namelist_wps.substitude_string('opt_output_from_metgrid_path', ' = ', "'" + new_case_dir + '/Metgrid_Data/' + "'")
    namelist_wps.save_content()

    # Continue to revise the namelist.input
    namelist_input.substitude_string('history_outname', ' = ', "'" + new_case_dir + '/' + time_str + '/wrfout_d<domain>_<date>' + "'")
    namelist_input.substitude_string('rst_outname', ' = ', "'" + new_case_dir + '/' + time_str + '/wrfrst_d<domain>_<date>' + "'")
    namelist_input.save_content()

    # Set the variable in the run_wrf.sh
    run_wrf = fo.change_content(run_wrf_dir)
    #run_wrf.substitude_string('#PBS -N', ' ', time_str[2::])
    run_wrf.substitude_string('#SBATCH -J', ' ', time_str[2::])
    run_wrf.substitude_string('export SCRATCH_DIRECTORY', '=', new_case_dir)
    run_wrf.save_content()

    print('Copy namelist.wps into Run_WRF')
    shutil.copy(namelist_wps_dir, folder_dir)
    print('Copy plotgrids_new.ncl into Run_WRF')
    shutil.copy(plotgrids_new_dir, folder_dir + '/Run_WRF')
    print('Copy namelist.input into Run_WRF')
    shutil.copy(namelist_input_dir, folder_dir)
    print('Copy run_wrf.sh into Run_WRF')
    shutil.copy(run_wrf_dir, folder_dir + '/Run_WRF')
    print('\n')

    time_now = time_now + datetime.timedelta(hours = cycling_interval)
