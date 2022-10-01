from script_00_common_settings import *

var = 'QICE'
(lb_title, factor, levels) = set_parameters(var)

for dom in domains:

    for idt in range(0, n_time):

        time_now     = anl_start_time + datetime.timedelta(hours = idt*cycling_interval)
        time_now_str = time_now.strftime('%Y%m%d%H')
        print(time_now)

        extent  = [lon_limit[dom][0], lon_limit[dom][1], lat_limit[dom][0], lat_limit[dom][1]]
        pdfname = dir_main + '/' + var + '_da_' + dom + '_' + time_now_str + '.pdf'

        with PdfPages(pdfname) as pdf:

            for lev in levels.keys():

                fig, axs   = plt.subplots(n_row, n_col, figsize=(fig_width, fig_height))
                fig.subplots_adjust(left=fig_left, bottom=fig_bottom, right=fig_right, top=fig_top, wspace=fig_wspace, hspace=fig_hspace)

                suptitle_str = time_now_str + ', ' + dom + ', ' + str(lev) + ' hPa'
                fig.suptitle(suptitle_str, fontsize=7.5)

                print(name + '_' + exp + ': ' + str(lev) + ' hPa')

                filename = dir_main + '/' + var + '_da_' + dom + '.nc'
                ncfile   = Dataset(filename)
                lat_temp = ncfile.variables['lat'][:,:]
                lon_temp = ncfile.variables['lon'][:,:]
                level    = ncfile.variables['level'][:]

                idl = list(level).index(lev)
                (vmin1, vmax1, vint1, cmap1, vmin2, vmax2, vint2, cmap2) = levels[lev]

                for ids, sta in enumerate(status):

                    if n_row == 1:
                        ax = axs[ids]
                    else:
                        ax = axs[idc, ids]

                    m = Basemap(llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], \
                                projection='lcc', lat_1=40.0, lat_2=20.0, lon_0=-80.0, resolution='i', ax=ax)
                    m.drawcoastlines(linewidth=0.2, color='k')
                    #m.fillcontinents(color=sns_deep[8])
                    m.drawparallels(np.arange(0, 70, 10), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])
                    m.drawmeridians(np.arange(-120, -35, 10), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])

                    lon, lat = m(lon_temp, lat_temp, inverse=False)
                    if ids == 2:
                        temp = factor*(ncfile.variables[var][idt,idl,1,:,:] - ncfile.variables[var][idt,idl,0,:,:])
                        pcm2 = ax.contourf(lon, lat, temp, levels=np.arange(vmin2, vmax2, vint2), cmap=cmap2, extend='both', zorder=0)
                    else:
                        temp = factor*(ncfile.variables[var][idt,idl,ids,:,:])
                        pcm1 = ax.contourf(lon, lat, temp, levels=np.arange(vmin1, vmax1+0.5*vint1, vint1), cmap=cmap1, extend='both', zorder=0)

                    mtitle = '(' + chr(97+ids) + ') ' + exp + ', ' + sta
                    ax.set_title(mtitle, fontsize=7.5, pad=4.0)

                if n_row == 1:
                    clb1 = fig.colorbar(pcm1, ax=axs[:2], orientation='horizontal', pad=lb_pad, aspect=75, shrink=1.00)
                else:
                    clb1 = fig.colorbar(pcm1, ax=axs[:,:2], orientation='horizontal', pad=lb_pad, aspect=75, shrink=1.00)
                clb1.set_label(lb_title, fontsize=7.5, labelpad=4.0)
                clb1.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=7.5)

                if n_row == 1:
                    clb2 = fig.colorbar(pcm2, ax=axs[2], orientation='horizontal', pad=lb_pad, aspect=37.5, shrink=1.00)
                else:
                    clb2 = fig.colorbar(pcm2, ax=axs[:, 2], orientation='horizontal', pad=lb_pad, aspect=37.5, shrink=1.00)
                clb2.set_label('increment of ' + lb_title, fontsize=7.5, labelpad=4.0)
                clb2.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=7.5)

                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()

    ncfile.close()
