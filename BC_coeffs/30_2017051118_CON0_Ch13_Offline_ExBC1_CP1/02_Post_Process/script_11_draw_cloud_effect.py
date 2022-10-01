import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import os
import datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap

dir_GOES   = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main   = dir_GOES + '/24_Revision/BC_coeffs/30_2017051118_CON0_Ch13_Offline_ExBC1_CP1'
file_d01   = dir_GOES + '/24_Revision/track_intensity/sample/wrfout_d01_2017-06-20_00:00:00'
dir_netcdf = dir_main + '/02_Post_Process/2017051118_06h'
dir_save   = dir_main + '/02_Post_Process/2017051118_06h'

anl_start_time   = datetime.datetime(2017, 5, 11, 18, 0, 0)
anl_end_time     = datetime.datetime(2017, 6, 24, 18, 0, 0)
draw_time        = datetime.datetime(2017, 6, 22,  0, 0, 0)
cycling_interval = 6
forecast_hours   = [6]
domains          = ['d01']
thingrid         = ['030km']
channel          = 8

variables = {'error0':     [0, 0, '(a) error0'], \
             'cldeff_obs': [0, 1, '(b) observed C'], \
             'cldeff_bkg': [1, 0, '(c) simulated C'], \
             'C':          [1, 1, '(d) cloud proxy variable C']}

sns_bright = sns.color_palette('bright')
sns_deep = sns.color_palette('deep')

data_d01 = Dataset(file_d01)
lat_d01 = data_d01.variables['XLAT'][0,:,:]
lon_d01 = data_d01.variables['XLONG'][0,:,:]
extent = [lon_d01[0,0], lon_d01[-1,-1], lat_d01[0,0], lat_d01[-1,-1]]
data_d01.close()

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

            anl_start_time_str = anl_start_time.strftime('%Y%m%d%H')
            anl_end_time_str   = anl_end_time.strftime('%Y%m%d%H')
            draw_time_str      = draw_time.strftime('%Y%m%d%H')

            pdfname = dir_save + '/' + draw_time_str + '_' + datathinning + '_' + dom + '_' + \
                      str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_CE.pdf'

            with PdfPages(pdfname) as pdf:

                fig_width  = 6.00
                fig_height = 5.30
                fig, axs   = plt.subplots(2, 2, figsize=(fig_width, fig_height))
                fig.subplots_adjust(left=0.075, bottom=0.050, right=0.980, top=0.975, wspace=0.200, hspace=0.050)

                ftime        = draw_time + datetime.timedelta(hours = fhours)
                suptitle_str = draw_time_str + ', datathinning: ' + datathinning + ', domain: ' + dom + ', ' + \
                               str(int(fhours)).zfill(2) + ' hours forecast, channel ' + str(channel).zfill(2)
                fig.suptitle(suptitle_str, fontsize=7.5)

                filename = dir_netcdf + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                           str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '.nc'
                print(filename)

                ncfile        = Dataset(filename)
                time          = list(ncfile.variables['time'][:])
                draw_time_str = draw_time.strftime('%Y%m%d%H')
                itime         = time.index(float(draw_time_str))
                temp          = ncfile.variables['BT_bkg'][itime, :]
                index         = temp < 66666
                cenlat        = ncfile.variables['cenlat'][itime, :]
                cenlon        = ncfile.variables['cenlon'][itime, :]
                lat_1d        = cenlat[index]
                lon_1d        = cenlon[index]

                for var in variables:

                    (idx, jdx, title) = variables[var]
                    temp_1d = abs(ncfile.variables[var][itime, index])
                    print(title)
                    print('max: ', np.max(temp_1d))
                    print('min: ', np.min(temp_1d))

                    ax = axs[idx, jdx]
                    m = Basemap(llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], \
                                projection='lcc', lat_1=40.0, lat_2=20.0, lon_0=-80.0, resolution='i', ax=ax)
                    m.drawcoastlines(linewidth=0.2, color='k')
                    m.fillcontinents(color=sns_deep[8])
                    m.drawparallels(np.arange(0, 70, 10), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])
                    m.drawmeridians(np.arange(-120, -35, 10), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])

                    x_lon_1d, y_lat_1d = m(lon_1d, lat_1d, inverse=False)
                    pcm = ax.tricontourf(x_lon_1d, y_lat_1d, temp_1d, levels=np.arange(0, 101, 10), cmap='RdBu', extend='both', zorder=0)
                    ax.tick_params('both', direction='in', labelsize=7.5)
                    ax.set_title(title, fontsize=7.5, pad=4.0)

                clb = fig.colorbar(pcm, ax=axs[1,:], ticks=np.arange(0, 101, 10), orientation='horizontal', pad=0.150, aspect=50, shrink=0.95)
                clb.set_label('Cloud Effect (K)', fontsize=7.5, labelpad=4.0)
                clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=7.5)

                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()
                ncfile.close()
