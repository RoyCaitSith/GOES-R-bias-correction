import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap

dir_GOES   = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main   = dir_GOES + '/24_Revision/BC_coeffs/27_2020082200_CON0_Ch13_Offline_ExBC1_CP0'
dir_netcdf = dir_main + '/02_Post_Process/2020082200_06h'
dir_save   = dir_main + '/02_Post_Process/2020082200_06h'

anl_start_time   = datetime.datetime(2020, 8, 22,  0, 0, 0)
anl_end_time     = datetime.datetime(2020, 8, 23, 18, 0, 0)
draw_time        = datetime.datetime(2020, 8, 23, 18, 0, 0)
cycling_interval = 6
forecast_hours   = [6]
domains          = ['d01']
thingrid         = ['030km']
channel          = 8

variables = {'Tlap': [4, -2.0, 2.0, 0.5, '(a) Tlap', 'Tlap (K)'], \
             'Scan Position': [11, 0.2, 1.0, 0.1, '(b) Scan Position', 'Scan Position'], \
             'Normalized C': [1, 0.0, 5.0, 1.0, '(c) Normalized C', 'Normalized C']}

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

            anl_start_time_str = anl_start_time.strftime('%Y%m%d%H')
            anl_end_time_str   = anl_end_time.strftime('%Y%m%d%H')
            draw_time_str      = draw_time.strftime('%Y%m%d%H')

            filename = dir_netcdf + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                       str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '.nc'
            print(filename)

            ncfile = Dataset(filename)
            time   = list(ncfile.variables['time'][:])
            itime  = time.index(float(draw_time_str))
            cenlat = ncfile.variables['cenlat'][itime,:]
            cenlon = ncfile.variables['cenlon'][itime,:]
            ncfile.close()

            filename = dir_netcdf + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                       str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_pred.nc'
            print(filename)

            ncfile = Dataset(filename)
            pred   = ncfile.variables['pred'][:, itime, :]
            ncfile.close()

            pdfname = dir_save + '/' + draw_time_str + '_' + datathinning + '_' + dom + '_' + \
                      str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_pred.pdf'

            with PdfPages(pdfname) as pdf:

                fig_width  = 9.00
                fig_height = 2.25
                fig, axs   = plt.subplots(1, 3, figsize=(fig_width, fig_height))
                fig.subplots_adjust(left=0.035, bottom=0.050, right=0.990, top=0.950, wspace=0.125, hspace=0.050)

                suptitle_str = draw_time_str + ', datathinning: ' + datathinning + ', domain: ' + dom + ', ' + \
                               str(fhours).zfill(2) + ' hours forecast, channel ' + str(channel).zfill(2)
                fig.suptitle(suptitle_str, fontsize=7.5)

                index  = cenlat < 66666
                lat_1d = cenlat[index]
                lon_1d = cenlon[index]

                for idv, var in enumerate(variables.keys()):

                    (xid, xmin, xmax, xint, mtitle, lb) = variables[var]
                    temp_1d = pred[xid, index]

                    print(var)
                    print(max(temp_1d))
                    print(min(temp_1d))

                    ax = axs[idv]
                    extent = [-109.420, -50.590, 10.040, 36.620]
                    m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], \
                        urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                    m.drawcoastlines(linewidth=0.2, color='k')
                    #m.fillcontinents(color=[0.9375, 0.9375, 0.859375])
                    pcm = ax.scatter(lon_1d, lat_1d, s=0.75, marker='s', linewidths=0.0, c=temp_1d, vmin=xmin, vmax=xmax, cmap='RdYlBu_r', zorder=0)
                    ax.set_xticks(np.arange(-105, -45, 10))
                    ax.set_xticklabels(['105W', '95W', '85W', '75W', '65W', '55W'])
                    ax.set_yticks(np.arange(5, 45, 10))
                    ax.set_yticklabels(['5N', '15N', '25N', '35N'])
                    ax.tick_params('both', direction='in', labelsize=7.5)
                    ax.set_title(mtitle, fontsize=7.5, pad=4.0)
                    ax.axis(extent)

                    clb = fig.colorbar(pcm, ax=ax, ticks=np.arange(xmin, xmax + xint, xint), orientation='horizontal', pad=0.100, aspect=50, shrink=0.95)
                    clb.set_label(lb, fontsize=7.5, labelpad=4.0)
                    clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=7.5)

                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()
