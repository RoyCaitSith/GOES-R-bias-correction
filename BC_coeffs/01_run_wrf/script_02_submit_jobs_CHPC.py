import os
import datetime

#anl_start_time   = datetime.datetime(2017, 5, 11, 18, 0, 0)
#anl_end_time     = datetime.datetime(2017, 5, 31, 18, 0, 0)
#anl_start_time   = datetime.datetime(2017, 6,  1,  0, 0, 0)
#anl_end_time     = datetime.datetime(2017, 6, 24, 18, 0, 0)
anl_start_time   = datetime.datetime(2020, 8, 22,  0, 0, 0)
anl_end_time     = datetime.datetime(2020, 8, 23, 18, 0, 0)
cycling_interval = 6

time_now = anl_start_time
while time_now <= anl_end_time:

    time_str     = time_now.strftime('%Y%m%d%H')
    new_case_dir = '/scratch/general/lustre/u1237353/CHPC_' + time_str
    command      = 'cd ' + new_case_dir + '/Run_WRF && sbatch run_wrf.sh'
    print(command)
    os.system(command)

    time_now = time_now + datetime.timedelta(hours = cycling_interval)
