from script_00_common_settings import *

var = 'qi'
(lb_title, factor, levels) = set_parameters(var)

for dom in domains:
    for idt in range(0, n_time):

        time_now = anl_start_time + datetime.timedelta(hours = idt*cycling_interval)
        time_now_str = time_now.strftime('%Y%m%d%H')
        print(time_now)

        extent = [lon_limit[dom][0], lon_limit[dom][1], lat_limit[dom][0], lat_limit[dom][1]]
        pdfname = dir_pdf + '/' + var + '_da_' + dom + '_' + time_now_str + '.pdf'

        filename = dir_main + '/' + case + '/' + var + '_' + dom + '.nc'
        print(filename)

        ncfile   = Dataset(filename)
        lat_temp = ncfile.variables['lat'][:,:]
        lon_temp = ncfile.variables['lon'][:,:]
        level    = ncfile.variables['level'][:]

        with PdfPages(pdfname) as pdf:
            for lev in levels.keys():

                print(case + ': ' + str(lev) + ' hPa')

                fig, axs = plt.subplots(n_row, n_col, figsize=(fig_width, fig_height))
                fig.subplots_adjust(left=fig_left, bottom=fig_bottom, right=fig_right, top=fig_top, wspace=fig_wspace, hspace=fig_hspace)

                suptitle_str = time_now_str + ', ' + dom + ', ' + str(lev) + ' hPa'
                fig.suptitle(suptitle_str, fontsize=7.5)

                idl = list(level).index(lev)
                (vmin1, vmax1, vint1, cmap1, vmin2, vmax2, vint2, cmap2) = levels[lev]

                ax = axs[0]
                m = Basemap(llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], \
                            projection='lcc', lat_1=40.0, lat_2=20.0, lon_0=-80.0, resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.2, color='k')
                #m.fillcontinents(color=[0.9375, 0.9375, 0.859375])
                m.drawparallels(np.arange(0, 70, 10), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5)
                m.drawmeridians(np.arange(-120, -35, 10), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5)
                lon, lat = m(lon_temp, lat_temp, inverse=False)

                temp = factor*ncfile.variables[var][0,idt,idl,:,:]
                pcm1 = ax.contourf(lon, lat, temp, levels=np.arange(vmin1, vmax1+0.5*vint1, vint1), cmap=cmap1, extend='both', zorder=0)
                mtitle = '(a) ' + case + ', ' + status[0]
                ax.set_title(mtitle, fontsize=7.5, pad=4.0)
                print(np.nanmax(temp))

                ax = axs[1]
                m = Basemap(llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], \
                            projection='lcc', lat_1=40.0, lat_2=20.0, lon_0=-80.0, resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.2, color='k')
                #m.fillcontinents(color=[0.9375, 0.9375, 0.859375])
                m.drawparallels(np.arange(0, 70, 10), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5)
                m.drawmeridians(np.arange(-120, -35, 10), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5)
                lon, lat = m(lon_temp, lat_temp, inverse=False)

                temp = factor*ncfile.variables[var][1,idt,idl,:,:]
                pcm2 = ax.contourf(lon, lat, temp, levels=np.arange(vmin2, vmax2+0.5*vint2, vint2), cmap=cmap2, extend='both', zorder=0)
                mtitle = '(b) ' + case + ', ' + status[1]
                ax.set_title(mtitle, fontsize=7.5, pad=4.0)
                print(np.nanmax(temp))

                clb1 = fig.colorbar(pcm1, ax=axs[0], orientation='horizontal', pad=lb_pad, aspect=37.5, shrink=0.95)
                clb1.set_label(lb_title, fontsize=7.5, labelpad=4.0)
                clb1.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=7.5)

                clb2 = fig.colorbar(pcm2, ax=axs[1], orientation='horizontal', pad=lb_pad, aspect=37.5, shrink=0.95)
                clb2.set_label(lb_title, fontsize=7.5, labelpad=4.0)
                clb2.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=7.5)

                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()

        ncfile.close()
