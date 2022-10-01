import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import datetime
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap

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
#exp_name = 'ASRBC4CLDC12'

draw_scheme = 2

if draw_scheme == 1:
    name     = 'Cindy'
    exp      = 'ASRBC4C04'
    dir_main = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/24_Revision/increment/' + name + '/' + exp
    (fig_width, fig_height, n_row, n_col) = (9.00, 2.75, 1, 3)
    (fig_left, fig_bottom, fig_right, fig_top, fig_wspace, fig_hspace) = (0.050, 0.010, 0.985, 0.950, 0.200, 0.250)
    lb_pad   = 0.100
if draw_scheme == 2:
    name     = 'Laura'
    exp      = 'ASRBC4CLDC12'
    dir_main = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/24_Revision/increment/' + name + '/' + exp
    (fig_width, fig_height, n_row, n_col) = (9.00, 2.75, 1, 3)
    (fig_left, fig_bottom, fig_right, fig_top, fig_wspace, fig_hspace) = (0.050, 0.010, 0.985, 0.950, 0.200, 0.250)
    lb_pad   = 0.100

if 'Cindy' in name:
    anl_start_time = datetime.datetime(2017, 6, 20,  6, 0, 0)
    anl_end_time   = datetime.datetime(2017, 6, 20,  6, 0, 0)
if 'Laura' in name:
    anl_start_time = datetime.datetime(2020, 8, 24,  6, 0, 0)
    anl_end_time   = datetime.datetime(2020, 8, 24,  6, 0, 0)
anl_end_time   = anl_start_time + datetime.timedelta(hours=6.0*(int(exp[-2:])-1))

cycling_interval = 6

analysis_time  = anl_end_time - anl_start_time
analysis_hours = analysis_time.days*24.0 + analysis_time.seconds/3600.0
n_time = int(analysis_hours/cycling_interval) + 1

status = ['bkg', 'anl', 'anl-bkg']
domains = ['d01']

lon_limit = {'d01': [-103.424225, -45.91736 ]}
lat_limit = {'d01': [   8.879852,  45.190746]}

def set_parameters(var):

    levels = {}

    if 'ua' in var:
        lb_title = 'ua (m/s)'
        factor   = 1.0
        levels.update({925: [-18.0, 20.0, 4.0, 'RdBu_r', -1.8, 2.0, 0.4, 'RdBu_r']})
        levels.update({850: [-18.0, 20.0, 4.0, 'RdBu_r', -1.8, 2.0, 0.4, 'RdBu_r']})
        levels.update({700: [-22.5, 25.0, 5.0, 'RdBu_r', -1.8, 2.0, 0.4, 'RdBu_r']})
        levels.update({500: [-22.5, 25.0, 5.0, 'RdBu_r', -1.8, 2.0, 0.4, 'RdBu_r']})
        levels.update({300: [-36.0, 40.0, 8.0, 'RdBu_r', -1.8, 2.0, 0.4, 'RdBu_r']})
        levels.update({200: [-36.0, 40.0, 8.0, 'RdBu_r', -1.8, 2.0, 0.4, 'RdBu_r']})
    elif 'va' in var:
        lb_title = 'va (m/s)'
        factor   = 1.0
        levels.update({925: [-18.0, 20.0, 4.0, 'RdBu_r', -1.8, 2.0, 0.4, 'RdBu_r']})
        levels.update({850: [-18.0, 20.0, 4.0, 'RdBu_r', -1.8, 2.0, 0.4, 'RdBu_r']})
        levels.update({700: [-13.5, 15.0, 3.0, 'RdBu_r', -1.8, 2.0, 0.4, 'RdBu_r']})
        levels.update({500: [-13.5, 15.0, 3.0, 'RdBu_r', -1.8, 2.0, 0.4, 'RdBu_r']})
        levels.update({300: [-18.0, 20.0, 4.0, 'RdBu_r', -1.8, 2.0, 0.4, 'RdBu_r']})
        levels.update({200: [-18.0, 20.0, 4.0, 'RdBu_r', -1.8, 2.0, 0.4, 'RdBu_r']})
    elif 'temp' in var:
        lb_title = 'T (K)'
        factor   = 1.0
        levels.update({925: [285, 305, 2.0, 'rainbow', -0.36, 0.40, 0.08, 'RdBu_r']})
        levels.update({850: [280, 300, 2.0, 'rainbow', -0.36, 0.40, 0.08, 'RdBu_r']})
        levels.update({700: [275, 290, 1.5, 'rainbow', -0.36, 0.40, 0.08, 'RdBu_r']})
        levels.update({500: [260, 270, 1.0, 'rainbow', -0.36, 0.40, 0.08, 'RdBu_r']})
        levels.update({300: [230, 250, 2.0, 'rainbow', -1.35, 1.50, 0.30, 'RdBu_r']})
        levels.update({200: [210, 225, 1.5, 'rainbow', -0.45, 0.50, 0.10, 'RdBu_r']})
    elif 'QVAPOR' in var:
        lb_title = 'QVAPOR ' + '($\mathregular{gkg^{-1}}$)'
        factor   = 1000.0
        levels.update({925: [0.0, 20.0, 2.00, 'YlGn', -0.360, 0.40, 0.08, 'BrBG']})
        levels.update({850: [0.0, 15.0, 1.50, 'YlGn', -0.360, 0.40, 0.08, 'BrBG']})
        levels.update({700: [0.0, 10.0, 1.00, 'YlGn', -0.360, 0.40, 0.08, 'BrBG']})
        levels.update({500: [0.0, 5.00, 0.50, 'YlGn', -0.540, 0.60, 0.12, 'BrBG']})
        levels.update({300: [0.0, 1.00, 0.10, 'YlGn', -0.180, 0.20, 0.04, 'BrBG']})
        levels.update({200: [0.0, 0.10, 0.01, 'YlGn', -.0045, .005, .001, 'BrBG']})
    elif 'QCLOUD' in var:
        lb_title = 'QCLOUD ' + '($\mathregular{10^{-2} gkg^{-1}}$)'
        factor   = 100000.0
        levels.update({925: [0, 30.0, 3.0, 'YlGn', -0.90, 1.00, 0.20, 'BrBG']})
        levels.update({850: [0, 30.0, 3.0, 'YlGn', -0.90, 1.00, 0.20, 'BrBG']})
        levels.update({700: [0, 30.0, 3.0, 'YlGn', -0.90, 1.00, 0.20, 'BrBG']})
        levels.update({500: [0, 30.0, 3.0, 'YlGn', -0.90, 1.00, 0.20, 'BrBG']})
        levels.update({300: [0, 5.00, 0.5, 'YlGn', -0.45, 0.50, 0.10, 'BrBG']})
        levels.update({200: [0, 5.00, 0.5, 'YlGn', -0.45, 0.50, 0.10, 'BrBG']})
    elif 'QICE' in var:
        lb_title = 'QICE ' + '($\mathregular{10^{-3} gkg^{-1}}$)'
        factor   = 1000000.0
        levels.update({925: [0.0, 10.0, 1.0, 'YlGn', -0.45, 0.50, 0.10, 'BrBG']})
        levels.update({850: [0.0, 10.0, 1.0, 'YlGn', -0.45, 0.50, 0.10, 'BrBG']})
        levels.update({700: [0.0, 10.0, 1.0, 'YlGn', -0.45, 0.50, 0.10, 'BrBG']})
        levels.update({500: [0.0, 10.0, 1.0, 'YlGn', -0.45, 0.50, 0.10, 'BrBG']})
        levels.update({300: [0.0, 10.0, 1.0, 'YlGn', -0.45, 0.50, 0.10, 'BrBG']})
        levels.update({200: [0.0, 5.00, 0.5, 'YlGn', -0.45, 0.50, 0.10, 'BrBG']})
    elif 'QRAIN' in var:
        lb_title = 'QRAIN ' + '($\mathregular{10^{-2} gkg^{-1}}$)'
        factor   = 100000.0
        levels.update({925: [0.0, 10.0, 1.0, 'YlGn', -0.09, 0.10, 0.02, 'BrBG']})
        levels.update({850: [0.0, 10.0, 1.0, 'YlGn', -0.09, 0.10, 0.02, 'BrBG']})
        levels.update({700: [0.0, 10.0, 1.0, 'YlGn', -0.09, 0.10, 0.02, 'BrBG']})
        levels.update({500: [0.0, 10.0, 1.0, 'YlGn', -0.09, 0.10, 0.02, 'BrBG']})
        levels.update({300: [0.0, 10.0, 1.0, 'YlGn', -0.09, 0.10, 0.02, 'BrBG']})
        levels.update({200: [0.0, 10.0, 1.0, 'YlGn', -0.09, 0.10, 0.02, 'BrBG']})
    elif 'QSNOW' in var:
        lb_title = 'QSNOW ' + '($\mathregular{10^{-2} gkg^{-1}}$)'
        factor   = 100000.0
        levels.update({925: [0.0, 10.0, 1.0, 'YlGn', -0.09, 0.10, 0.02, 'BrBG']})
        levels.update({850: [0.0, 10.0, 1.0, 'YlGn', -0.09, 0.10, 0.02, 'BrBG']})
        levels.update({700: [0.0, 10.0, 1.0, 'YlGn', -0.09, 0.10, 0.02, 'BrBG']})
        levels.update({500: [0.0, 10.0, 1.0, 'YlGn', -0.09, 0.10, 0.02, 'BrBG']})
        levels.update({300: [0.0, 10.0, 1.0, 'YlGn', -0.09, 0.10, 0.02, 'BrBG']})
        levels.update({200: [0.0, 10.0, 1.0, 'YlGn', -0.09, 0.10, 0.02, 'BrBG']})
    elif 'QGRAUP' in var:
        lb_title = 'QGRAUP ' + '($\mathregular{10^{-2} gkg^{-1}}$)'
        factor   = 100000.0
        levels.update({925: [0.0, 10.0, 1.0, 'YlGn', -0.09, 0.10, 0.02, 'BrBG']})
        levels.update({850: [0.0, 10.0, 1.0, 'YlGn', -0.09, 0.10, 0.02, 'BrBG']})
        levels.update({700: [0.0, 10.0, 1.0, 'YlGn', -0.09, 0.10, 0.02, 'BrBG']})
        levels.update({500: [0.0, 10.0, 1.0, 'YlGn', -0.09, 0.10, 0.02, 'BrBG']})
        levels.update({300: [0.0, 10.0, 1.0, 'YlGn', -0.09, 0.10, 0.02, 'BrBG']})
        levels.update({200: [0.0, 10.0, 1.0, 'YlGn', -0.09, 0.10, 0.02, 'BrBG']})
    elif 'rh' in var:
        lb_title = 'RH ' + '(%)'
        factor   = 1.0
        levels.update({925: [0.0, 100.0, 10.0, 'YlGn', -18.0, 20.0, 4.0, 'BrBG']})
        levels.update({850: [0.0, 100.0, 10.0, 'YlGn', -18.0, 20.0, 4.0, 'BrBG']})
        levels.update({700: [0.0, 100.0, 10.0, 'YlGn', -18.0, 20.0, 4.0, 'BrBG']})
        levels.update({500: [0.0, 100.0, 10.0, 'YlGn', -18.0, 20.0, 4.0, 'BrBG']})
        levels.update({300: [0.0, 80.00, 8.00, 'YlGn', -18.0, 20.0, 4.0, 'BrBG']})
        levels.update({200: [0.0, 80.00, 8.00, 'YlGn', -18.0, 20.0, 4.0, 'BrBG']})
    elif 'slp' in var:
        lb_title = 'slp (hPa)'
        factor = 1.0
        levels.update({0: [1005.0, 1025.0, 2.0, 'gist_rainbow_r', -0.45, 0.50, 0.10, 'RdBu_r']})

    return [lb_title, factor, levels]
