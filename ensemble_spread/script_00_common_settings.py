import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import datetime
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/17_2020Laura_Experiments/ensemble_spread/case_02'

case = 'ASRCON06hENS50024AugC1'
dir_pdf  = dir_main + '/figures_' + case
(fig_width, fig_height, n_row, n_col) = (6.00, 3.00, 1, 2)
(fig_left, fig_bottom, fig_right, fig_top, fig_wspace, fig_hspace) = (0.075, 0.025, 0.975, 0.950, 0.200, 0.250)
lb_pad = 0.075

if '0024Aug' in case:
    anl_start_time = datetime.datetime(2020, 8, 24,  6, 0, 0)
    anl_end_time = datetime.datetime(2020, 8, 24,  6, 0, 0)
anl_end_time = anl_start_time + datetime.timedelta(hours=6.0*(int(case[-1])-1))

if '6h' in case: cycling_interval = 6
analysis_time = anl_end_time - anl_start_time
analysis_hours = analysis_time.days*24.0 + analysis_time.seconds/3600.0
n_time = int(analysis_hours/cycling_interval) + 1

status = ['static', 'flow-dependent']
domains = ['d01']

lon_limit = {'d01': [-103.424225, -45.91736]}
lat_limit = {'d01': [   8.879852,  45.190746]}

def set_parameters(var):

    levels = {}

    if 'ql' in var:
        lb_title = 'ql ' + '($\mathregular{10^{-2} gkg^{-1}}$)'
        factor   = 100000.0
        levels.update({925: [0.0, 2.5, 0.5, 'YlGn', 0.0, 25.0, 5.0, 'YlGn']})
        levels.update({850: [0.0, 2.5, 0.5, 'YlGn', 0.0, 25.0, 5.0, 'YlGn']})
        levels.update({700: [0.0, 2.5, 0.5, 'YlGn', 0.0, 25.0, 5.0, 'YlGn']})
        levels.update({500: [0.0, 2.5, 0.5, 'YlGn', 0.0, 25.0, 5.0, 'YlGn']})
        levels.update({300: [0.0, 2.5, 0.5, 'YlGn', 0.0, 25.0, 5.0, 'YlGn']})
        levels.update({200: [0.0, 2.5, 0.5, 'YlGn', 0.0, 25.0, 5.0, 'YlGn']})
    elif 'qr' in var:
        lb_title = 'qr ' + '($\mathregular{10^{-2} gkg^{-1}}$)'
        factor   = 100000.0
        levels.update({925: [0.0, 25.0, 5.0, 'YlGn', 0.0, 25.0, 5.0, 'YlGn']})
        levels.update({850: [0.0, 25.0, 5.0, 'YlGn', 0.0, 25.0, 5.0, 'YlGn']})
        levels.update({700: [0.0, 25.0, 5.0, 'YlGn', 0.0, 25.0, 5.0, 'YlGn']})
        levels.update({500: [0.0, 25.0, 5.0, 'YlGn', 0.0, 25.0, 5.0, 'YlGn']})
        levels.update({300: [0.0, 25.0, 5.0, 'YlGn', 0.0, 25.0, 5.0, 'YlGn']})
        levels.update({200: [0.0, 25.0, 5.0, 'YlGn', 0.0, 25.0, 5.0, 'YlGn']})
    elif 'qi' in var:
        lb_title = 'qi ' + '($\mathregular{10^{-3} gkg^{-1}}$)'
        factor   = 1000000.0
        levels.update({925: [0.0, 10.0, 2.0, 'YlGn', 0.0, 100.0, 20.0, 'YlGn']})
        levels.update({850: [0.0, 10.0, 2.0, 'YlGn', 0.0, 100.0, 20.0, 'YlGn']})
        levels.update({700: [0.0, 10.0, 2.0, 'YlGn', 0.0, 100.0, 20.0, 'YlGn']})
        levels.update({500: [0.0, 10.0, 2.0, 'YlGn', 0.0, 100.0, 20.0, 'YlGn']})
        levels.update({300: [0.0, 10.0, 2.0, 'YlGn', 0.0, 100.0, 20.0, 'YlGn']})
        levels.update({200: [0.0, 10.0, 2.0, 'YlGn', 0.0, 100.0, 20.0, 'YlGn']})
    elif 'qs' in var:
        lb_title = 'qs ' + '($\mathregular{10^{-2} gkg^{-1}}$)'
        factor   = 100000.0
        levels.update({925: [0.0, 15.0, 3.0, 'YlGn', 0.0, 15.0, 3.0, 'YlGn']})
        levels.update({850: [0.0, 15.0, 3.0, 'YlGn', 0.0, 15.0, 3.0, 'YlGn']})
        levels.update({700: [0.0, 15.0, 3.0, 'YlGn', 0.0, 15.0, 3.0, 'YlGn']})
        levels.update({500: [0.0, 15.0, 3.0, 'YlGn', 0.0, 15.0, 3.0, 'YlGn']})
        levels.update({300: [0.0, 15.0, 3.0, 'YlGn', 0.0, 15.0, 3.0, 'YlGn']})
        levels.update({200: [0.0, 15.0, 3.0, 'YlGn', 0.0, 15.0, 3.0, 'YlGn']})
    elif 'qg' in var:
        lb_title = 'qg ' + '($\mathregular{10^{-2} gkg^{-1}}$)'
        factor   = 100000.0
        levels.update({925: [0.0, 25.0, 5.0, 'YlGn', 0.0, 25.0, 5.0, 'YlGn']})
        levels.update({850: [0.0, 25.0, 5.0, 'YlGn', 0.0, 25.0, 5.0, 'YlGn']})
        levels.update({700: [0.0, 25.0, 5.0, 'YlGn', 0.0, 25.0, 5.0, 'YlGn']})
        levels.update({500: [0.0, 25.0, 5.0, 'YlGn', 0.0, 25.0, 5.0, 'YlGn']})
        levels.update({300: [0.0, 25.0, 5.0, 'YlGn', 0.0, 25.0, 5.0, 'YlGn']})
        levels.update({200: [0.0, 25.0, 5.0, 'YlGn', 0.0, 25.0, 5.0, 'YlGn']})

    return [lb_title, factor, levels]
