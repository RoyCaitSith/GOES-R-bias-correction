import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import datetime
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap

dir_main = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/15_WRF_Experiments/other/berror'
dir_save = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/15_WRF_Experiments/other/increment/case_01'

cases = ['case_01_ASR']
var   = 'QICE'

if '01' in cases[0]:
    anl_start_time = datetime.datetime(2017, 5, 27,  6, 0, 0)
    anl_end_time   = datetime.datetime(2017, 5, 27, 12, 0, 0)

levels = {}
levels.update({200: [0, 5e-8, 'YlGn']})
domains = ['d01']
cycling_interval = 1
n_time = 7

for idt in range(0, n_time):

    time_now     = anl_start_time + datetime.timedelta(hours = idt*cycling_interval)
    time_now_str = time_now.strftime('%Y%m%d%H')

    for dom in domains:

        pdfname = dir_main + '/Figures/' + var + '_V_' + dom + '_' + time_now_str + '.pdf'
        print(time_now)

        with PdfPages(pdfname) as pdf:

            for lev in levels.keys():

                fig_width  = 3.00
                fig_height = 2.00
                fig, axs   = plt.subplots(1, 1, figsize=(fig_width, fig_height))
                fig.subplots_adjust(left=0.100, bottom=0.075, right=0.985, top=0.965, wspace=0.150, hspace=0.100)

                suptitle_str = var + ', ' + time_now_str + ', ' + dom + ', ' + str(lev) + ' hPa'
                fig.suptitle(suptitle_str, fontsize=7.5)

                for idc, case in enumerate(cases):

                    filename = dir_save + '/' + case[8:] + '/' + var + '_da_' + dom + '.nc'
                    ncfile   = Dataset(filename)
                    lat      = ncfile.variables['lat'][:,:]
                    lon      = ncfile.variables['lon'][:,:]
                    level    = ncfile.variables['level'][:]
                    extent   = [lon.min(), lon.max(), lat.min(), lat.max()]

                    idl = list(level).index(lev)
                    (vmin1, vmax1, cmap1) = levels[lev]

                    ax = axs
                    m  = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                    m.drawcoastlines(linewidth=0.2, color='k')
                    #m.fillcontinents(color=[0.9375, 0.9375, 0.859375])

                    temp = ncfile.variables[var][idt,idl,0,:,:]
                    temp = np.where(temp < 1e-10, 1e-10, 0.05*temp)
                    pcm1 = ax.imshow(temp, cmap=cmap1, interpolation='none', origin='lower', vmin=vmin1, vmax=vmax1, extent=extent, zorder=0)
                    print(np.nanmin(temp), np.nanmax(temp))

                    ax.set_xticks(np.arange(-105, -45, 10))
                    ax.set_xticklabels(['105W', '95W', '85W', '75W', '65W', '55W'])
                    ax.set_yticks(np.arange(5, 45, 10))
                    ax.set_yticklabels(['5N', '15N', '25N', '35N'])
                    ax.tick_params('both', direction='in', labelsize=7.5)
                    ax.axis(extent)

                    clb1 = fig.colorbar(pcm1, ax=axs, orientation='horizontal', pad=0.100, aspect=50, shrink=0.95)
                    clb1.set_label('V of QICE ' + '($\mathregular{kgkg^{-1}}$)', fontsize=7.5, labelpad=4.0)
                    clb1.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=7.5)

                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()

    ncfile.close()
