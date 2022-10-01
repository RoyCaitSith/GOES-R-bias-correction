import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import datetime
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap

cases = ['ASRBC0C04', 'ASRBC1C04', 'ASRBC4C04']
dir_main_cs = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/24_Revision/cross_section/Cindy'
dir_main_in = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/24_Revision/increment/Cindy'
(fig_width, fig_height, n_row, n_col) = (12.00, 8.50, 3, 4)
(fig_left, fig_bottom, fig_right, fig_top, fig_wspace, fig_hspace) = (0.050, 0.030, 0.975, 0.975, 0.300, 0.100)
(lb_pad, lb_aspect, lb_shrink) = (0.075, 40, 1.00)

Exps = ['ASRBC0, Diff', 'ASRBC1, Diff', 'ASRBC4, Diff']
Vars = ['OmB_before_BC', 'OmB_after_BC', 'OmB_after_BC', 'OmB_after_BC']
cenlon = [-87.0]

anl_start_time = datetime.datetime(2017, 6, 20,  6, 0, 0)
anl_end_time   = datetime.datetime(2017, 6, 20,  6, 0, 0)
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

        pdfname = './Figure_08_Temperature_Increment.pdf'

        with PdfPages(pdfname) as pdf:

            fig, axs = plt.subplots(n_row, n_col, figsize=(fig_width, fig_height))
            fig.subplots_adjust(left=fig_left, bottom=fig_bottom, right=fig_right, top=fig_top, wspace=fig_wspace, hspace=fig_hspace)

            print('Part One')
            for idc, (case, exp) in enumerate(zip(cases, Exps)):

                (vmin, vmax, vint, cmap) = colormap

                row = idc//n_col
                col = idc%n_col
                print(row, col)

                if col == 0:
                    ax = axs[0, col]

                    filename = dir_main_cs + '/ASRC04/' + var1 + '_da_' + dom + '.nc'
                    ncfile = Dataset(filename)
                    ASRC04_temp1 = ncfile.variables[var1][idt,1,:,:] - ncfile.variables[var1][idt,0,:,:]
                    lon      = ncfile.variables['lon'][:]
                    level    = ncfile.variables['level'][:]
                    n_level  = len(level)
                    n_latlon = len(lon)
                    extent   = [lon.min(), lon.max(), 0, n_level-1]
                    ncfile.close()

                    filename = dir_main_cs + '/ASRC04/' + var2 + '_da_' + dom + '.nc'
                    ncfile = Dataset(filename)
                    ASRC04_temp2 = ncfile.variables[var2][idt,1,:,:] - ncfile.variables[var2][idt,0,:,:]
                    ncfile.close()

                    pcm1 = ax.contourf(lon, level, ASRC04_temp1, levels=np.arange(-1.2, 1.21, 0.4), cmap='coolwarm', extend='both', zorder=0)
                    pcm2 = ax.contour(lon, level, ASRC04_temp2, levels=np.arange(-100.0, -2.9, 3.0), linestyles='dashed', linewidths=1.0, colors='k', zorder=1)
                    pcm2 = ax.contour(lon, level, ASRC04_temp2, levels=np.arange(3.0, 100.1, 3.0), linestyles='solid', linewidths=1.0, colors='k', zorder=1)

                    for idp, clon in enumerate(cenlon):
                        ax.plot([clon, clon], [0.0, 10000.0], color='k', ls='dashdot', linewidth=1.00, zorder=0)
                        #ax.text(clon+0.5, 850.0, chr(65+idp), horizontalalignment='center', verticalalignment='center', fontsize=10.0)

                    ax.set_xticks(np.arange(-92.0, -83.0, 2.0))
                    ax.set_xticklabels(['-92W', '-90W', '-88W', '-86W', '-84W'], fontsize=10.0)
                    ax.set_yticks(np.arange(100, n_level, 200))
                    ax.set_ylabel('Pressure (hPa)', fontsize=10.0)
                    ax.tick_params('both', direction='in', labelsize=10.0)
                    ax.axis(extent)
                    ax.invert_yaxis()

                    mtitle = '(' + chr(97+idc) + ') ASR'
                    ax.set_title(mtitle, fontsize=10.0, pad=4.0)

                    lb_ticks = np.array([-1.2, -0.8, -0.4, 0, 0.4, 0.8, 1.2])
                    clb1 = fig.colorbar(pcm1, ax=ax, orientation='horizontal', ticks=lb_ticks, pad=lb_pad, aspect=17.5, shrink=1.00)
                    clb1.set_label(lb_title, fontsize=10.0, labelpad=4.0)
                    clb1.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

                ax = axs[0, col+1]

                filename = dir_main_cs + '/' + case + '/' + var1 + '_da_' + dom + '.nc'
                ncfile   = Dataset(filename)
                temp1 = ncfile.variables[var1][idt,1,:,:] - ncfile.variables[var1][idt,0,:,:]
                ncfile.close()

                filename = dir_main_cs + '/' + case + '/' + var2 + '_da_' + dom + '.nc'
                ncfile   = Dataset(filename)
                temp2    = ncfile.variables[var2][idt,1,:,:] - ncfile.variables[var2][idt,0,:,:]
                ncfile.close()

                print(np.nanmax(temp2-ASRC04_temp2))
                print(np.nanmin(temp2-ASRC04_temp2))
                pcm1 = ax.contourf(lon, level, temp1-ASRC04_temp1, levels=np.arange(vmin, vmax, vint), cmap=cmap, extend='both', zorder=0)
                pcm2 = ax.contour(lon, level, temp2-ASRC04_temp2, levels=np.arange(-18.0, -0.9, 1.0), linestyles='dashed', linewidths=1.0, colors='k', zorder=1)
                pcm2 = ax.contour(lon, level, temp2-ASRC04_temp2, levels=np.arange(1.0, 18.1, 1.0), linestyles='solid', linewidths=1.0, colors='k', zorder=1)

                for idp, clon in enumerate(cenlon):
                    ax.plot([clon, clon], [0.0, 10000.0], color='k', ls='dashdot', linewidth=1.00, zorder=0)
                    #ax.text(clon+0.5, 850.0, chr(65+idp), horizontalalignment='center', verticalalignment='center', fontsize=10.0)

                ax.set_xticks(np.arange(-92.0, -83.0, 2.0))
                ax.set_xticklabels(['-92W', '-90W', '-88W', '-86W', '-84W'], fontsize=10.0)
                ax.set_yticks(np.arange(100, n_level, 200))
                ax.set_ylabel('Pressure (hPa)', fontsize=10.0)
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.axis(extent)
                ax.invert_yaxis()

                mtitle = '(' + chr(98+idc) + ') ' + exp
                ax.set_title(mtitle, fontsize=10.0, pad=4.0)

            lb_ticks = np.array([-0.50, -0.40, -0.30, -0.20, -0.10, 0.0, 0.10, 0.20, 0.30, 0.40, 0.50])
            clb2 = fig.colorbar(pcm1, ax=axs[0,1:], orientation='horizontal', ticks=lb_ticks, pad=lb_pad, aspect=60.0, shrink=1.00)
            clb2.set_label(lb_title, fontsize=10.0, labelpad=4.0)
            clb2.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

            print('Part Two')
            for idc, (case, exp) in enumerate(zip(cases, Exps)):

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

                    filename = dir_main_in + '/ASRC04/' + var1 + '_da_' + dom + '.nc'
                    ncfile = Dataset(filename)
                    level = ncfile.variables['level'][:]
                    lat   = ncfile.variables['lat'][:,:]
                    lon   = ncfile.variables['lon'][:,:]
                    idl = list(level).index(200)
                    (vmin, vmax, vint, cmap, ws, wslb) = levels[200]
                    ASRC04_temp1 = ncfile.variables[var1][idt,idl,1,:,:] - ncfile.variables[var1][idt,idl,0,:,:]
                    avg = np.average(ncfile.variables[var1][idt,idl,1,:,:])
                    print(np.average(ncfile.variables[var1][idt,idl,0,:,:]))
                    ncfile.close()

                    filename = dir_main_in + '/ASRC04/' + var2 + '_da_' + dom + '.nc'
                    ncfile = Dataset(filename)
                    ASRC04_temp2 = ncfile.variables[var2][idt,idl,1,:,:] - ncfile.variables[var2][idt,idl,0,:,:]
                    ncfile.close()

                    lon, lat = m(lon, lat, inverse=False)
                    pcm1 = ax.contourf(lon, lat, ASRC04_temp1, levels=np.arange(-1.2, 1.21, 0.4), cmap='coolwarm', extend='both', zorder=0)
                    pcm2 = ax.contour( lon, lat, ASRC04_temp2, levels=np.arange(-100.0, -2.9, 3.0), linestyles='dashed', linewidths=1.0, colors='k', zorder=1)
                    pcm2 = ax.contour( lon, lat, ASRC04_temp2, levels=np.arange(3.0, 100.1, 3.0), linestyles='solid', linewidths=1.0, colors='k', zorder=1)

                    idl = list(level).index(500)
                    filename = dir_main_in + '/ASRC04/ua_da_' + dom + '.nc'
                    ncfile = Dataset(filename)
                    ASRC04_ua_temp = ncfile.variables['ua'][idt,idl,1,:,:] - ncfile.variables['ua'][idt,idl,0,:,:]
                    ncfile.close()

                    filename = dir_main_in + '/ASRC04/va_da_' + dom + '.nc'
                    ncfile = Dataset(filename)
                    ASRC04_va_temp = ncfile.variables['va'][idt,idl,1,:,:] - ncfile.variables['va'][idt,idl,0,:,:]
                    ncfile.close()

                    pcm3 = ax.quiver(lon[::15, ::15], lat[::15, ::15], ASRC04_ua_temp[::15, ::15], ASRC04_va_temp[::15, ::15], \
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
                print(np.average(ncfile.variables[var1][idt,idl,0,:,:]))
                ncfile.close()

                filename = dir_main_in + '/' + case + '/' + var2 + '_da_' + dom + '.nc'
                ncfile = Dataset(filename)
                temp2 = ncfile.variables[var2][idt,idl,1,:,:] - ncfile.variables[var2][idt,idl,0,:,:]
                ncfile.close()

                #lon, lat = m(lon, lat, inverse=False)
                pcm1 = ax.contourf(lon, lat, temp1-ASRC04_temp1, levels=np.arange(vmin, vmax, vint), cmap=cmap, extend='both', zorder=0)
                pcm2 = ax.contour( lon, lat, temp2-ASRC04_temp2, levels=np.arange(-18.0, -0.9, 1.0), linestyles='dashed', linewidths=1.0, colors='k', zorder=1)
                pcm2 = ax.contour( lon, lat, temp2-ASRC04_temp2, levels=np.arange(1.0, 18.1, 1.0), linestyles='solid', linewidths=1.0, colors='k', zorder=1)

                idl = list(level).index(500)
                filename = dir_main_in + '/' + case + '/ua_da_' + dom + '.nc'
                ncfile = Dataset(filename)
                ua_temp = ncfile.variables['ua'][idt,idl,1,:,:] - ncfile.variables['ua'][idt,idl,0,:,:]
                ncfile.close()

                filename = dir_main_in + '/' + case + '/va_da_' + dom + '.nc'
                ncfile = Dataset(filename)
                va_temp = ncfile.variables['va'][idt,idl,1,:,:] - ncfile.variables['va'][idt,idl,0,:,:]
                ncfile.close()

                pcm3 = ax.quiver(lon[::15, ::15], lat[::15, ::15], ua_temp[::15, ::15]-ASRC04_ua_temp[::15, ::15], va_temp[::15, ::15]-ASRC04_va_temp[::15, ::15], \
                                 color='k', scale=5.0*0.2, scale_units='inches', zorder=2)

                if idc == 0:
                    qk = ax.quiverkey(pcm3, 0.900, 0.350, 0.2, '0.2 m/s', labelpos='E', coordinates='figure')

                x_d01, y_d01 = m(-102.5, 44.0, inverse=False)
                #ax.text(x_d01, y_d01, format(avg, '.2f'), ha='center', va='center', color='black', fontsize=10.0, zorder=4)
                mtitle = '(' + chr(102+idc) + ') ' + exp
                ax.set_title(mtitle, fontsize=10.0, pad=4.0)

            lb_ticks = np.array([-0.50, -0.40, -0.30, -0.20, -0.10, 0.0, 0.10, 0.20, 0.30, 0.40, 0.50])
            clb4 = fig.colorbar(pcm1, ax=axs[1, 1:], orientation='horizontal', ticks=lb_ticks, pad=lb_pad, aspect=60.0, shrink=1.00)
            clb4.set_label(lb_title, fontsize=10.0, labelpad=4.0)
            clb4.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

            print('Part Three')
            dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
            dir_main = []
            dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/29_2017051118_CON0_Ch13_Offline_ExBC1_CP0/02_Post_Process/2017051118_06h')
            dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/30_2017051118_CON0_Ch13_Offline_ExBC1_CP1/02_Post_Process/2017051118_06h')
            dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/21_2017051118_CON0_Ch13_Offline_ExBC1_CP4_AR1_TC5/02_Post_Process/2017051118_06h')

            anl_start_time = datetime.datetime(2017, 5, 11, 18, 0, 0)
            anl_end_time   = datetime.datetime(2017, 6, 24, 18, 0, 0)
            anl_start_time_str = anl_start_time.strftime('%Y%m%d%H')
            anl_end_time_str   = anl_end_time.strftime('%Y%m%d%H')
            extent = [lon_limit[dom][0], lon_limit[dom][1], lat_limit[dom][0], lat_limit[dom][1]]

            for idc, (var, exp, dmain) in enumerate(zip(Vars[1:], Exps, dir_main)):

                if idc == 0:
                    filename = dmain + '/' + anl_start_time_str + '_' + anl_end_time_str + '_030km_' + dom + '_06h_channel_08.nc'
                    print(filename)

                    ncfile  = Dataset(filename)
                    cenlat  = ncfile.variables['cenlat'][:,:]
                    cenlon  = ncfile.variables['cenlon'][:,:]
                    qc_temp = ncfile.variables['id_qc'][:,:]
                    time    = list(ncfile.variables['time'][:])
                    itime   = int(time.index(float(time_now.strftime('%Y%m%d%H')))-1.0)
                    ASRC04_temp   = ncfile.variables['OmB_before_BC'][itime, :]
                    ASRC04_id_qc  = qc_temp[itime, :]
                    ASRC04_errinv = ncfile.variables['errinv'][itime, :]

                    index  = (ASRC04_temp < 66666) & (ASRC04_id_qc == 0)
                    lat_1d = cenlat[itime, index]
                    lon_1d = cenlon[itime, index]
                    ASRC04_temp_1d = ASRC04_temp[index]*ASRC04_errinv[index]
                    ncfile.close()

                    print('max: ', np.max(ASRC04_temp_1d))
                    print('min: ', np.min(ASRC04_temp_1d))

                    ax = axs[2, 0]
                    m = Basemap(llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], \
                                projection='lcc', lat_1=40.0, lat_2=20.0, lon_0=-80.0, resolution='i', ax=ax)
                    m.drawcoastlines(linewidth=0.2, color='k')
                    m.drawparallels(np.arange(0, 70, 10), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])
                    m.drawmeridians(np.arange(-120, -35, 10), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])

                    lon_1d, lat_1d = m(lon_1d, lat_1d, inverse=False)
                    pcm = ax.scatter(lon_1d, lat_1d, s=1.00, marker='s', linewidths=0.0, c=ASRC04_temp_1d, vmin=-1.8, vmax=1.8, cmap='coolwarm', zorder=0)

                    mtitle = '(' + chr(105) + ') ASR'
                    ax.set_title(mtitle, fontsize=10.0, pad=4.0)

                    lon_line = np.arange(-92.0, -84.0, 0.01)
                    lat_line = np.ones((len(lon_line)))*25.0
                    lon_line, lat_line = m(lon_line, lat_line, inverse=False)
                    ax.plot(lon_line, lat_line, color='k', linewidth=1.5)

                    lb_ticks = np.arange(-1.8, 1.9, 0.6)
                    clb5 = fig.colorbar(pcm, ax=ax, orientation='horizontal', ticks=lb_ticks, pad=lb_pad, aspect=17.5, shrink=1.00)
                    clb5.set_label('All-Sky Scaled OmB', fontsize=10.0, labelpad=4.0)
                    clb5.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

                filename = dmain + '/' + anl_start_time_str + '_' + anl_end_time_str + '_030km_' + dom + '_06h_channel_08.nc'
                print(filename)

                ncfile  = Dataset(filename)
                cenlat  = ncfile.variables['cenlat'][:,:]
                cenlon  = ncfile.variables['cenlon'][:,:]
                temp   = ncfile.variables[var][itime, :]
                id_qc  = ncfile.variables['id_qc'][itime, :]
                errinv = ncfile.variables['errinv'][itime, :]

                index  = (ASRC04_temp < 66666) & (ASRC04_id_qc == 0) & (temp < 66666) & (id_qc == 0)
                lat_1d = cenlat[itime, index]
                lon_1d = cenlon[itime, index]
                temp_1d = temp[index]*errinv[index]-ASRC04_temp[index]*ASRC04_errinv[index]
                ncfile.close()

                #print('max: ', np.max(temp_1d))
                #print('min: ', np.min(temp_1d))

                ax = axs[2, idc+1]
                m = Basemap(llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], \
                            projection='lcc', lat_1=40.0, lat_2=20.0, lon_0=-80.0, resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.2, color='k')
                m.drawparallels(np.arange(0, 70, 10), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])
                m.drawmeridians(np.arange(-120, -35, 10), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])

                lon_1d, lat_1d = m(lon_1d, lat_1d, inverse=False)
                pcm = ax.scatter(lon_1d, lat_1d, s=1.00, marker='s', linewidths=0.0, c=temp_1d, vmin=-0.5, vmax=0.5, cmap='RdBu_r', zorder=0)

                mtitle = '(' + chr(106+idc) + ') ' + exp
                ax.set_title(mtitle, fontsize=10.0, pad=4.0)

                lon_line = np.arange(-92.0, -84.0, 0.01)
                lat_line = np.ones((len(lon_line)))*25.0
                lon_line, lat_line = m(lon_line, lat_line, inverse=False)
                ax.plot(lon_line, lat_line, color='k', linewidth=1.5)

            lb_ticks = np.arange(-0.5, 0.51, 0.1)
            clb6 = fig.colorbar(pcm, ax=axs[2,1:], orientation='horizontal', ticks=lb_ticks, pad=lb_pad, aspect=60.0, shrink=1.00)
            clb6.set_label('All-Sky Scaled OmB', fontsize=10.0, labelpad=4.0)
            clb6.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

            pdf.savefig(fig)
            plt.cla()
            plt.clf()
            plt.close()
