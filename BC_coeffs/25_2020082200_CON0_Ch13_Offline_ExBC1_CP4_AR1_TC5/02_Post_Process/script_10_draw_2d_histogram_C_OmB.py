import os
import datetime
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import entropy
from matplotlib.backends.backend_pdf import PdfPages

dir_GOES  = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main  = dir_GOES + '/24_Revision/BC_coeffs/25_2020082200_CON0_Ch13_Offline_ExBC1_CP4_AR1_TC5'
dir_histo = dir_main + '/02_Post_Process/2020082200_06h'
dir_save  = dir_main + '/02_Post_Process/2020082200_06h'

anl_start_time   = datetime.datetime(2020, 8, 22,  0, 0, 0)
anl_end_time     = datetime.datetime(2020, 8, 23, 18, 0, 0)
cycling_interval = 6
forecast_hours   = [6]
domains          = ['d01']
thingrid         = ['030km']
channel          = 8

schemes = {'00': ['C', 'all_sky_scaled_OmB', -74.75, 75.25, 0.5, -40.0, 40.0, 0.2]}
#schemes = {'00': ['C', 'normalized_OmB', -74.75, 75.25, 0.5, -40.0, 40.0, 0.2]}

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

            anl_start_time_str = anl_start_time.strftime('%Y%m%d%H')
            anl_end_time_str   = anl_end_time.strftime('%Y%m%d%H')

            for idsch, idsch_str in enumerate(schemes.keys()):

                pdfname = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                          str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_histogram2d_' + idsch_str + '_C_OmB.pdf'

                with PdfPages(pdfname) as pdf:

                    fig_width    = 6.00
                    fig_height   = 6.00
                    fig, axs     = plt.subplots(1, 1, figsize=(fig_width, fig_height))
                    suptitle_str = 'from ' +  anl_start_time_str + ' to ' + anl_end_time_str + ', datathinning: ' + datathinning + ', domain: ' + dom + ', ' + \
                                   str(fhours).zfill(2) + ' hours forecast, channel ' + str(channel).zfill(2)
                    fig.subplots_adjust(left=0.100, bottom=-0.050, right=0.975, top=0.925, wspace=0.250, hspace=0.450)
                    fig.suptitle(suptitle_str, fontsize=7.5)

                    ax = axs

                    (xvar, yvar, xrange_min, xrange_max, xrange_interval, yrange_min, yrange_max, yrange_interval) = schemes[idsch_str]
                    xbin_center = np.arange(xrange_min, xrange_max + xrange_interval, xrange_interval)
                    ybin_center = np.arange(yrange_min, yrange_max + yrange_interval, yrange_interval)

                    filename = dir_histo + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                               str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_histogram2d_' + idsch_str + '_C_OmB.txt'
                    print(filename)

                    temp  = np.loadtxt(filename)
                    index = temp[0][:] != 0
                    xavg  = xbin_center[index]
                    yavg  = temp[0][index]
                    hist  = np.log10(temp[1:][:]/np.sum(temp[1:][:])/xrange_interval/yrange_interval)
                    print('max: ', np.max(hist))
                    print('min: ', np.min(hist))

                    extent = [xrange_min, xrange_max, yrange_min, yrange_max]
                    ax.plot([xrange_min, xrange_max], [0, 0], color='k', ls='--', linewidth=0.5)
                    ax.plot(xavg, yavg, color='k', ls='-', linewidth=0.5)

                    pcm = ax.imshow(hist, cmap='RdYlBu_r', interpolation='none', origin='lower', vmin=-5.5, vmax=-1.5, \
                                    aspect='auto', extent=extent, zorder=0)
                    #ax.set_xticks(np.arange(170.0, 400.0, 5.0))
                    #ax.set_yticks(np.arange(-40.0, 45.0, 5.0))
                    ax.set_xlabel(xvar, fontsize=7.5)
                    ax.set_ylabel(yvar, fontsize=7.5)
                    ax.tick_params('both', which='both', direction='in', labelsize=7.5, right=True, top=True)
                    #ax.set_title(title_str, fontsize=7.5, pad=4.0)
                    ax.axis([-0, 75, -4, 4])

                    clb = fig.colorbar(pcm, ax=axs, ticks=np.arange(-5.5, -1.0, 0.5), orientation='horizontal', pad=0.075, aspect=50, shrink=0.95)
                    clb.set_label('log(PDF)', fontsize=7.5, labelpad=4.0)
                    clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=7.5)

                    pdf.savefig(fig)
                    plt.cla()
                    plt.clf()
                    plt.close()
