from __future__ import print_function
import os, sys
import shutil
import string
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
#exp_name = 'ASRBC0CLDC12'
#exp_name = 'ASRBC1CLDC12'
exp_name = 'ASRBC4CLDC12'

case = name + '_' + exp_name

dir_exp   = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/24_Revision'
files_exp = '/'.join([dir_exp, 'track_intensity', name, exp_name])

if 'Cindy' in name:
    files_hwrf = files_exp + '/multi/hwrf.18x18.AL032017.2017062000.f'
if 'Laura' in name:
    files_hwrf = files_exp + '/multi/hwrf.18x18.AL132020.2020082400.f'

n_time       = 9 + int(exp_name[-2:])
input_domain = 'd01'

files_dir = files_exp + '/postprd'
files_out = files_exp + '/multi'
dh        = 6
dtime     = 360

for i in range(0, n_time, 1):

    input_file = files_dir + '/FINAL_' + input_domain + '.' + str(i*dh).zfill(2)
    out_file   = files_dir + '/FINAL.' + str(i*dh).zfill(2)
    print(input_file)
    print(out_file)

    print('Simply copy ', input_file)
    os.system('cp ' + input_file + ' ' + out_file)

    flnm_hwrf = files_hwrf + str(i*dtime).zfill(5)
    flnm_hwrf_ix = flnm_hwrf + '.ix'
    shutil.copyfile(out_file, flnm_hwrf)
    os.system(files_out + '/grbindex.exe ' + flnm_hwrf + ' ' + flnm_hwrf_ix)
