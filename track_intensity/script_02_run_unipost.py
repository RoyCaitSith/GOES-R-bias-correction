import os
import re
import sys
import time
import shutil
import datetime
import numpy as np

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

dir_exp = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/24_Revision'
folder_in  = '/'.join([dir_exp, 'track_intensity', name, 'ASRC12'])
folder_out = '/'.join([dir_exp, 'track_intensity', name, exp_name])

print('Create a folder: multi')
folder_multi_in  = folder_in  + '/multi'
folder_multi_out = folder_out + '/multi'
os.system('mkdir ' + folder_multi_out)

print('Copy the files from ', folder_multi_in, ' to ', folder_multi_out)
os.system('cp ' + folder_multi_in + '/fort.* ' + folder_multi_out)
os.system('cp ' + folder_multi_in + '/gettrk.exe ' + folder_multi_out)
os.system('cp ' + folder_multi_in + '/grbindex.exe ' + folder_multi_out)
os.system('cp ' + folder_multi_in + '/input.nml ' + folder_multi_out)
os.system('cp ' + folder_multi_in + '/tcvit_rsmc_storms.txt ' + folder_multi_out)

print('Create a folder: parm')
folder_parm_in  = folder_in  + '/parm'
folder_parm_out = folder_out + '/parm'
os.system('mkdir ' + folder_parm_out)

print('Copy the files from ', folder_parm_in, ' to ', folder_parm_out)
os.system('cp ' + folder_parm_in + '/wrf_cntrl.parm ' + folder_parm_out)

print('Create a folder: postprd')
folder_postprd_in  = folder_in  + '/postprd'
folder_postprd_out = folder_out + '/postprd'
os.system('mkdir ' + folder_postprd_out)

print('Copy the files from ', folder_postprd_in, ' to ', folder_postprd_out)
os.system('cp ' + folder_postprd_in + '/run_unipost ' + folder_postprd_out)

print('Please revise fort.15 in ', folder_multi_out)
print('Please revise input.nml in ', folder_multi_out)
print('Please revise tcvit_rsmc_storms.txt in ', folder_multi_out)
print('Please revise run_unipost in ', folder_postprd_out)
print('Please run run_unipost!')
