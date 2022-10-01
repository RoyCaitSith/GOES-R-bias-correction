import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import math
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from wrf import getvar, latlon_coords
from netCDF4 import Dataset
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import griddata

channel        = 8
n_channel      = 10
n_diagbufr     = math.ceil(30/5)
n_diagbufrchan = math.ceil(533/5)
n_diag         = n_diagbufr + n_channel*n_diagbufrchan

(fig_width_1, fig_height_1, n_row_1, n_col_1) = (8.00, 3.50, 1, 2)
(fig_left_1, fig_bottom_1, fig_right_1, fig_top_1, fig_wspace_1, fig_hspace_1) = (0.050, 0.050, 0.975, 0.950, 0.150, 0.200)
(vmin, vmax, vint) = (0, 450, 50)
lb_pad   = 0.075
lb_title = 'BT (K)'

pdfname = './Figure_99_slons_slats.pdf'

with PdfPages(pdfname) as pdf:

    fig, axs = plt.subplots(n_row_1, n_col_1, figsize=(fig_width_1, fig_height_1))
    fig.subplots_adjust(left=fig_left_1, bottom=fig_bottom_1, right=fig_right_1, top=fig_top_1, wspace=fig_wspace_1, hspace=fig_hspace_1)

    dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
    cenlat = [25.04565, 25.56942]
    cenlon = [-86.3698, -89.8358]

    draw_time = datetime.datetime(2017, 6, 20,  6, 0, 0)
    draw_time_str = draw_time.strftime('%Y%m%d%H')

    dom = 'd01'
    lon_limit = {'d01': [-103.56036, -48.264954]}
    lat_limit = {'d01': [  8.740578,  40.992657]}
    extent  = [lon_limit[dom][0], lon_limit[dom][1], lat_limit[dom][0], lat_limit[dom][1]]

    fileBT = dir_GOES + '/23_All_Experiments/BC_coeffs/13_2017051118_CON0_Ch13_Offline_ExBC1_CP0/02_Post_Process/2017051118_06h/2017051118_2017062418_030km_d01_06h_channel_08.nc'
    print(fileBT)

    ncfileBT = Dataset(fileBT)
    qc_temp  = ncfileBT.variables['id_qc'][:,:]
    time     = list(ncfileBT.variables['time'][:])
    itime    = int(time.index(float(draw_time_str))-1)
    id_qc    = qc_temp[itime, :]

    var      = 'BT_obs_before_BC'
    temp     = ncfileBT.variables[var][itime, :]
    index    = (temp < 66666) & (id_qc == 0)
    lat_1d   = ncfileBT.variables['cenlat'][itime, index]
    lon_1d   = ncfileBT.variables['cenlon'][itime, index]
    slons_1d = ncfileBT.variables['slons'][itime, index]
    slats_1d = ncfileBT.variables['slats'][itime, index]
    print('max slons: ', np.max(slons_1d))
    print('min slons: ', np.min(slons_1d))
    print('max slats: ', np.max(slats_1d))
    print('min slats: ', np.min(slats_1d))

    ax = axs[0]
    m = Basemap(llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], \
                projection='lcc', lat_1=40.0, lat_2=20.0, lon_0=-80.0, resolution='i', ax=ax)
    m.drawcoastlines(linewidth=0.2, color='k')
    m.drawparallels(np.arange(0, 70, 10), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])
    m.drawmeridians(np.arange(-120, -35, 10), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])

    lon_1d, lat_1d = m(lon_1d, lat_1d, inverse=False)
    pcm = ax.scatter(lon_1d, lat_1d, marker='s', s=5.0, linewidths=0.0, c=slons_1d, vmin=vmin, vmax=vmax, cmap='coolwarm_r', zorder=0)

    mtitle = '(a) slons'
    ax.set_title(mtitle, fontsize=10.0, pad=4.0)

    lon_line = np.arange(-92.0, -84.0, 0.01)
    lat_line = np.ones((len(lon_line)))*25.0
    lon_line, lat_line = m(lon_line, lat_line, inverse=False)
    ax.plot(lon_line, lat_line, color='k', linewidth=1.5)

    #for idp, (clon, clat) in enumerate(zip(cenlon, cenlat)):
        #index = (lat_1d == clat) & (lon_1d == clon)
        #print(temp_1d[index])

        #clon_m, clat_m = m(clon, clat, inverse=False)
        #ax.plot(clon_m, clat_m, 'x', color='k', markersize=7.5, markeredgewidth=1.0)
        #clon_m, clat_m = m(clon+1.75, clat+1.0, inverse=False)
        #ax.text(clon_m, clat_m, chr(65+idp), horizontalalignment='center', verticalalignment='center', fontsize=10.0)

    ax = axs[1]
    m = Basemap(llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], \
                projection='lcc', lat_1=40.0, lat_2=20.0, lon_0=-80.0, resolution='i', ax=ax)
    m.drawcoastlines(linewidth=0.2, color='k')
    m.drawparallels(np.arange(0, 70, 10), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])
    m.drawmeridians(np.arange(-120, -35, 10), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])

    pcm = ax.scatter(lon_1d, lat_1d, marker='s', s=5.0, linewidths=0.0, c=slats_1d, vmin=vmin, vmax=vmax, cmap='coolwarm_r', zorder=0)

    mtitle = '(b) slats'
    ax.set_title(mtitle, fontsize=10.0, pad=4.0)

    ncfileBT.close()

    lon_line = np.arange(-92.0, -84.0, 0.01)
    lat_line = np.ones((len(lon_line)))*25.0
    lon_line, lat_line = m(lon_line, lat_line, inverse=False)
    ax.plot(lon_line, lat_line, color='k', linewidth=1.5)

    #for idp, (clon, clat) in enumerate(zip(cenlon, cenlat)):
        #index = (lat_1d == clat) & (lon_1d == clon)
        #print(temp_1d[index])

        #clon_m, clat_m = m(clon, clat, inverse=False)
        #ax.plot(clon_m, clat_m, 'x', color='k', markersize=7.5, markeredgewidth=1.0)
        #clon_m, clat_m = m(clon+1.75, clat+1.0, inverse=False)
        #ax.text(clon_m, clat_m, chr(65+idp), horizontalalignment='center', verticalalignment='center', fontsize=10.0)

    clb = fig.colorbar(pcm, ax=axs, ticks=np.arange(vmin, vmax+0.5*vint, vint), orientation='horizontal', pad=lb_pad, aspect=50, shrink=1.00)
    clb.set_label(lb_title, fontsize=10.0, labelpad=4.0)
    clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

    pdf.savefig(fig)
    plt.cla()
    plt.clf()
    plt.close()
