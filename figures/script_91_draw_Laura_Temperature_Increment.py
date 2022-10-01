import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import datetime
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap

cases = ['ASRBC0C12', 'ASRBC1C12', 'ASRBC4C12']
cases_CLD = ['ASRBC0CLDC12', 'ASRBC1CLDC12', 'ASRBC4CLDC12']
dir_main_in = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/24_Revision/increment/Laura'
(fig_width, fig_height, n_row, n_col) = (12.00, 8.50, 2, 4)
(fig_left, fig_bottom, fig_right, fig_top, fig_wspace, fig_hspace) = (0.050, 0.030, 0.975, 0.975, 0.300, 0.100)
(lb_pad, lb_aspect, lb_shrink) = (0.075, 40, 1.00)

Exps = ['ASRBC0, Diff', 'ASRBC1, Diff', 'ASRBC4, Diff']
Exps_CLD = ['ASRBC0CLD, Diff', 'ASRBC1CLD, Diff', 'ASRBC4CLD, Diff']
Vars = ['OmB_before_BC', 'OmB_after_BC', 'OmB_after_BC', 'OmB_after_BC']

anl_start_time = datetime.datetime(2020, 8, 24,  6, 0, 0)
anl_end_time   = datetime.datetime(2020, 8, 24,  6, 0, 0)
cycling_interval = 6
n_time = 1
domains = ['d01']
lon_limit = {'d01': [-103.424225, -45.91736 ]}
lat_limit = {'d01': [   8.879852,  45.190746]}

var1 = 'temp'
var2 = 'rh'
lb_title = 'T (K)'
colormap = (-0.50, 0.51, 0.10, 'RdBu_r')
levels = {}
levels.update({200: [-0.50, 0.51, 0.10, 'RdBu_r', 0.5, '0.5 m/s']})

for dom in domains:

    for idt in range(0, n_time):

        time_now     = anl_start_time + datetime.timedelta(hours = idt*cycling_interval)
        time_now_str = time_now.strftime('%Y%m%d%H')
        print(time_now)

        pdfname = './Figure_91_Laura_Temperature_Increment.pdf'

        with PdfPages(pdfname) as pdf:

            fig, axs = plt.subplots(n_row, n_col, figsize=(fig_width, fig_height))
            fig.subplots_adjust(left=fig_left, bottom=fig_bottom, right=fig_right, top=fig_top, wspace=fig_wspace, hspace=fig_hspace)

            print('Part One')
            for idc, (case, exp) in enumerate(zip(cases, Exps)):

                extent = [lon_limit[dom][0], lon_limit[dom][1], lat_limit[dom][0], lat_limit[dom][1]]
                (vmin, vmax, vint, cmap) = colormap

                row = idc//n_col
                col = idc%n_col
                print(row, col)

                if col == 0:

                    ax = axs[0, col]
                    m = Basemap(llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], \
                                projection='lcc', lat_1=40.0, lat_2=20.0, lon_0=-80.0, resolution='i', ax=ax)
                    m.drawcoastlines(linewidth=0.2, color='k')
                    m.drawparallels(np.arange(0, 70, 10), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])
                    m.drawmeridians(np.arange(-120, -35, 10), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])

                    filename = dir_main_in + '/ASRC12/' + var1 + '_da_' + dom + '.nc'
                    ncfile = Dataset(filename)
                    level = ncfile.variables['level'][:]
                    lat   = ncfile.variables['lat'][:,:]
                    lon   = ncfile.variables['lon'][:,:]
                    idl = list(level).index(200)
                    (vmin, vmax, vint, cmap, ws, wslb) = levels[200]
                    ASRC12_temp1 = ncfile.variables[var1][idt,idl,1,:,:] - ncfile.variables[var1][idt,idl,0,:,:]
                    avg = np.average(ncfile.variables[var1][idt,idl,1,:,:])
                    print(np.average(ncfile.variables[var1][idt,idl,1,:,:]))
                    ncfile.close()

                    filename = dir_main_in + '/ASRC12/' + var2 + '_da_' + dom + '.nc'
                    ncfile = Dataset(filename)
                    ASRC12_temp2 = ncfile.variables[var2][idt,idl,1,:,:] - ncfile.variables[var2][idt,idl,0,:,:]
                    ncfile.close()

                    lon, lat = m(lon, lat, inverse=False)
                    pcm1 = ax.contourf(lon, lat, ASRC12_temp1, levels=np.arange(-1.2, 1.21, 0.4), cmap='coolwarm', extend='both', zorder=0)
                    #pcm2 = ax.contour( lon, lat, ASRC12_temp2, levels=np.arange(-100.0, -2.9, 3.0), linestyles='dashed', linewidths=1.0, colors='k', zorder=1)
                    #pcm2 = ax.contour( lon, lat, ASRC12_temp2, levels=np.arange(3.0, 100.1, 3.0), linestyles='solid', linewidths=1.0, colors='k', zorder=1)

                    idl = list(level).index(500)
                    filename = dir_main_in + '/ASRC12/ua_da_' + dom + '.nc'
                    ncfile = Dataset(filename)
                    ASRC12_ua_temp = ncfile.variables['ua'][idt,idl,1,:,:] - ncfile.variables['ua'][idt,idl,0,:,:]
                    ncfile.close()

                    filename = dir_main_in + '/ASRC12/va_da_' + dom + '.nc'
                    ncfile = Dataset(filename)
                    ASRC12_va_temp = ncfile.variables['va'][idt,idl,1,:,:] - ncfile.variables['va'][idt,idl,0,:,:]
                    ncfile.close()

                    pcm3 = ax.quiver(lon[::15, ::15], lat[::15, ::15], ASRC12_ua_temp[::15, ::15], ASRC12_va_temp[::15, ::15], \
                                     color='k', scale=5.0*ws, scale_units='inches', zorder=2)

                    if idc == 0:
                        qk = ax.quiverkey(pcm3, 0.200, 0.350, ws, wslb, labelpos='E', coordinates='figure')

                    x_d01, y_d01 = m(-102.5, 44.0, inverse=False)
                    #ax.text(x_d01, y_d01, format(avg, '.2f'), ha='center', va='center', color='black', fontsize=10.0, zorder=4)
                    mtitle = '(' + chr(101+idc) + ') ASR'
                    ax.set_title(mtitle, fontsize=10.0, pad=4.0)

                    lb_ticks = np.array([-1.2, -0.8, -0.4, 0, 0.4, 0.8, 1.2])
                    clb3 = fig.colorbar(pcm1, ax=ax, orientation='horizontal', ticks=lb_ticks, pad=lb_pad, aspect=17.5, shrink=1.00)
                    clb3.set_label(lb_title, fontsize=10.0, labelpad=4.0)
                    clb3.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

                ax = axs[0, col+1]
                m = Basemap(llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], \
                            projection='lcc', lat_1=40.0, lat_2=20.0, lon_0=-80.0, resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.2, color='k')
                m.drawparallels(np.arange(0, 70, 10), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])
                m.drawmeridians(np.arange(-120, -35, 10), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])

                filename = dir_main_in + '/' + case + '/' + var1 + '_da_' + dom + '.nc'
                ncfile   = Dataset(filename)
                idl = list(level).index(200)
                temp1 = ncfile.variables[var1][idt,idl,1,:,:] - ncfile.variables[var1][idt,idl,0,:,:]
                avg = np.average(ncfile.variables[var1][idt,idl,1,:,:])
                print(np.average(ncfile.variables[var1][idt,idl,1,:,:]))
                ncfile.close()

                filename = dir_main_in + '/' + case + '/' + var2 + '_da_' + dom + '.nc'
                ncfile = Dataset(filename)
                temp2 = ncfile.variables[var2][idt,idl,1,:,:] - ncfile.variables[var2][idt,idl,0,:,:]
                ncfile.close()

                #lon, lat = m(lon, lat, inverse=False)
                pcm1 = ax.contourf(lon, lat, temp1-ASRC12_temp1, levels=np.arange(vmin, vmax, vint), cmap=cmap, extend='both', zorder=0)
                #pcm2 = ax.contour( lon, lat, temp2-ASRC12_temp2, levels=np.arange(-18.0, -0.9, 1.0), linestyles='dashed', linewidths=1.0, colors='k', zorder=1)
                #pcm2 = ax.contour( lon, lat, temp2-ASRC12_temp2, levels=np.arange(1.0, 18.1, 1.0), linestyles='solid', linewidths=1.0, colors='k', zorder=1)

                idl = list(level).index(500)
                filename = dir_main_in + '/' + case + '/ua_da_' + dom + '.nc'
                ncfile = Dataset(filename)
                ua_temp = ncfile.variables['ua'][idt,idl,1,:,:] - ncfile.variables['ua'][idt,idl,0,:,:]
                ncfile.close()

                filename = dir_main_in + '/' + case + '/va_da_' + dom + '.nc'
                ncfile = Dataset(filename)
                va_temp = ncfile.variables['va'][idt,idl,1,:,:] - ncfile.variables['va'][idt,idl,0,:,:]
                ncfile.close()

                pcm3 = ax.quiver(lon[::15, ::15], lat[::15, ::15], ua_temp[::15, ::15]-ASRC12_ua_temp[::15, ::15], va_temp[::15, ::15]-ASRC12_va_temp[::15, ::15], \
                                 color='k', scale=5.0*0.2, scale_units='inches', zorder=2)

                if idc == 0:
                    qk = ax.quiverkey(pcm3, 0.900, 0.350, 0.2, '0.2 m/s', labelpos='E', coordinates='figure')

                x_d01, y_d01 = m(-102.5, 44.0, inverse=False)
                mtitle = '(' + chr(102+idc) + ') ' + exp
                ax.set_title(mtitle, fontsize=10.0, pad=4.0)

            lb_ticks = np.array([-0.50, -0.40, -0.30, -0.20, -0.10, 0.0, 0.10, 0.20, 0.30, 0.40, 0.50])
            clb4 = fig.colorbar(pcm1, ax=axs[0, 1:], orientation='horizontal', ticks=lb_ticks, pad=lb_pad, aspect=60.0, shrink=1.00)
            clb4.set_label(lb_title, fontsize=10.0, labelpad=4.0)
            clb4.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

            print('Part Two')
            for idc, (case, exp) in enumerate(zip(cases_CLD, Exps)):

                extent = [lon_limit[dom][0], lon_limit[dom][1], lat_limit[dom][0], lat_limit[dom][1]]
                (vmin, vmax, vint, cmap) = colormap

                row = idc//n_col
                col = idc%n_col
                print(row, col)

                if col == 0:

                    ax = axs[1, col]
                    m = Basemap(llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], \
                                projection='lcc', lat_1=40.0, lat_2=20.0, lon_0=-80.0, resolution='i', ax=ax)
                    m.drawcoastlines(linewidth=0.2, color='k')
                    m.drawparallels(np.arange(0, 70, 10), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])
                    m.drawmeridians(np.arange(-120, -35, 10), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])

                    filename = dir_main_in + '/ASRCLDC12/' + var1 + '_da_' + dom + '.nc'
                    ncfile = Dataset(filename)
                    level = ncfile.variables['level'][:]
                    lat   = ncfile.variables['lat'][:,:]
                    lon   = ncfile.variables['lon'][:,:]
                    idl = list(level).index(200)
                    (vmin, vmax, vint, cmap, ws, wslb) = levels[200]
                    ASRCLDC12_temp1 = ncfile.variables[var1][idt,idl,1,:,:] - ncfile.variables[var1][idt,idl,0,:,:]
                    avg = np.average(ncfile.variables[var1][idt,idl,1,:,:])
                    print(np.average(ncfile.variables[var1][idt,idl,1,:,:]))
                    ncfile.close()

                    filename = dir_main_in + '/ASRCLDC12/' + var2 + '_da_' + dom + '.nc'
                    ncfile = Dataset(filename)
                    ASRCLDC12_temp2 = ncfile.variables[var2][idt,idl,1,:,:] - ncfile.variables[var2][idt,idl,0,:,:]
                    ncfile.close()

                    lon, lat = m(lon, lat, inverse=False)
                    pcm1 = ax.contourf(lon, lat, ASRCLDC12_temp1, levels=np.arange(-1.2, 1.21, 0.4), cmap='coolwarm', extend='both', zorder=0)
                    #pcm2 = ax.contour( lon, lat, ASRCLDC12_temp2, levels=np.arange(-100.0, -2.9, 3.0), linestyles='dashed', linewidths=1.0, colors='k', zorder=1)
                    #pcm2 = ax.contour( lon, lat, ASRCLDC12_temp2, levels=np.arange(3.0, 100.1, 3.0), linestyles='solid', linewidths=1.0, colors='k', zorder=1)

                    idl = list(level).index(500)
                    filename = dir_main_in + '/ASRCLDC12/ua_da_' + dom + '.nc'
                    ncfile = Dataset(filename)
                    ASRCLDC12_ua_temp = ncfile.variables['ua'][idt,idl,1,:,:] - ncfile.variables['ua'][idt,idl,0,:,:]
                    ncfile.close()

                    filename = dir_main_in + '/ASRCLDC12/va_da_' + dom + '.nc'
                    ncfile = Dataset(filename)
                    ASRCLDC12_va_temp = ncfile.variables['va'][idt,idl,1,:,:] - ncfile.variables['va'][idt,idl,0,:,:]
                    ncfile.close()

                    pcm3 = ax.quiver(lon[::15, ::15], lat[::15, ::15], ASRCLDC12_ua_temp[::15, ::15], ASRCLDC12_va_temp[::15, ::15], \
                                     color='k', scale=5.0*ws, scale_units='inches', zorder=2)

                    if idc == 0:
                        qk = ax.quiverkey(pcm3, 0.200, 0.350, ws, wslb, labelpos='E', coordinates='figure')

                    x_d01, y_d01 = m(-102.5, 44.0, inverse=False)
                    #ax.text(x_d01, y_d01, format(avg, '.2f'), ha='center', va='center', color='black', fontsize=10.0, zorder=4)
                    mtitle = '(' + chr(101+idc) + ') ASRCLD'
                    ax.set_title(mtitle, fontsize=10.0, pad=4.0)

                    lb_ticks = np.array([-1.2, -0.8, -0.4, 0, 0.4, 0.8, 1.2])
                    clb3 = fig.colorbar(pcm1, ax=ax, orientation='horizontal', ticks=lb_ticks, pad=lb_pad, aspect=17.5, shrink=1.00)
                    clb3.set_label(lb_title, fontsize=10.0, labelpad=4.0)
                    clb3.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

                ax = axs[1, col+1]
                m = Basemap(llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], \
                            projection='lcc', lat_1=40.0, lat_2=20.0, lon_0=-80.0, resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.2, color='k')
                m.drawparallels(np.arange(0, 70, 10), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])
                m.drawmeridians(np.arange(-120, -35, 10), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])

                filename = dir_main_in + '/' + case + '/' + var1 + '_da_' + dom + '.nc'
                ncfile   = Dataset(filename)
                idl = list(level).index(200)
                temp1 = ncfile.variables[var1][idt,idl,1,:,:] - ncfile.variables[var1][idt,idl,0,:,:]
                avg = np.average(ncfile.variables[var1][idt,idl,1,:,:])
                print(np.average(ncfile.variables[var1][idt,idl,1,:,:]))
                ncfile.close()

                filename = dir_main_in + '/' + case + '/' + var2 + '_da_' + dom + '.nc'
                ncfile = Dataset(filename)
                temp2 = ncfile.variables[var2][idt,idl,1,:,:] - ncfile.variables[var2][idt,idl,0,:,:]
                ncfile.close()

                #lon, lat = m(lon, lat, inverse=False)
                pcm1 = ax.contourf(lon, lat, temp1-ASRCLDC12_temp1, levels=np.arange(vmin, vmax, vint), cmap=cmap, extend='both', zorder=0)
                #pcm2 = ax.contour( lon, lat, temp2-ASRCLDC12_temp2, levels=np.arange(-18.0, -0.9, 1.0), linestyles='dashed', linewidths=1.0, colors='k', zorder=1)
                #pcm2 = ax.contour( lon, lat, temp2-ASRCLDC12_temp2, levels=np.arange(1.0, 18.1, 1.0), linestyles='solid', linewidths=1.0, colors='k', zorder=1)

                idl = list(level).index(500)
                filename = dir_main_in + '/' + case + '/ua_da_' + dom + '.nc'
                ncfile = Dataset(filename)
                ua_temp = ncfile.variables['ua'][idt,idl,1,:,:] - ncfile.variables['ua'][idt,idl,0,:,:]
                ncfile.close()

                filename = dir_main_in + '/' + case + '/va_da_' + dom + '.nc'
                ncfile = Dataset(filename)
                va_temp = ncfile.variables['va'][idt,idl,1,:,:] - ncfile.variables['va'][idt,idl,0,:,:]
                ncfile.close()

                pcm3 = ax.quiver(lon[::15, ::15], lat[::15, ::15], ua_temp[::15, ::15]-ASRCLDC12_ua_temp[::15, ::15], va_temp[::15, ::15]-ASRCLDC12_va_temp[::15, ::15], \
                                 color='k', scale=5.0*0.2, scale_units='inches', zorder=2)

                if idc == 0:
                    qk = ax.quiverkey(pcm3, 0.900, 0.350, 0.2, '0.2 m/s', labelpos='E', coordinates='figure')

                x_d01, y_d01 = m(-102.5, 44.0, inverse=False)
                mtitle = '(' + chr(102+idc) + ') ' + exp
                ax.set_title(mtitle, fontsize=10.0, pad=4.0)

            lb_ticks = np.array([-0.50, -0.40, -0.30, -0.20, -0.10, 0.0, 0.10, 0.20, 0.30, 0.40, 0.50])
            clb4 = fig.colorbar(pcm1, ax=axs[1, 1:], orientation='horizontal', ticks=lb_ticks, pad=lb_pad, aspect=60.0, shrink=1.00)
            clb4.set_label(lb_title, fontsize=10.0, labelpad=4.0)
            clb4.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

            pdf.savefig(fig)
            plt.cla()
            plt.clf()
            plt.close()
