import os
import datetime
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import entropy
from matplotlib.backends.backend_pdf import PdfPages

dir_GOES  = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main  = dir_GOES + '/24_Revision/BC_coeffs/30_2017051118_CON0_Ch13_Offline_ExBC1_CP1'
dir_histo = dir_main + '/02_Post_Process/2017051118_06h'
dir_save  = dir_main + '/02_Post_Process/2017051118_06h'

anl_start_time   = datetime.datetime(2017, 5, 11, 18, 0, 0)
anl_end_time     = datetime.datetime(2017, 6, 24, 18, 0, 0)
cycling_interval = 6
forecast_hours   = [6]
domains          = ['d01']
thingrid         = ['030km']
channel          = 8

schemes = {}
schemes.update({'00': [('00',   -4.0,    4.0,  0.2, -60.0, 60.0, 0.2), ('01',   -4.0,    4.0,  0.2, -60.0, 60.0, 0.2)]})
schemes.update({'01': [('02',  0.025,  1.225, 0.05, -60.0, 60.0, 0.2), ('03',  0.025,  1.225, 0.05, -60.0, 60.0, 0.2)]})
schemes.update({'02': [('04',   0.50, 100.50,  1.0, -60.0, 60.0, 0.2), ('05',   0.50, 100.50,  1.0, -60.0, 60.0, 0.2)]})

configurations = {}
configurations.update({'00': [('Tlap',          'All-sky Scaled OmB', '(a) before BC'), ('Tlap',          'All-sky Scaled OmB', '(b) after BC')]})
configurations.update({'01': [('Scan Position', 'All-sky Scaled OmB', '(a) before BC'), ('Scan Position', 'All-sky Scaled OmB', '(b) after BC')]})
configurations.update({'02': [('Normalized C',  'All-sky Scaled OmB', '(a) before BC'), ('Normalized C',  'All-sky Scaled OmB', '(b) after BC')]})

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

            anl_start_time_str = anl_start_time.strftime('%Y%m%d%H')
            anl_end_time_str   = anl_end_time.strftime('%Y%m%d%H')

            for idsch, idsch_str in enumerate(schemes.keys()):

                #pdfname = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                          #str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_pred_histogram2d_' + idsch_str + '_All Sky.pdf'
                #pdfname = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                          #str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_pred_histogram2d_' + idsch_str + '_Clear Sky.pdf'
                pdfname = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                          str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_pred_histogram2d_' + idsch_str + '_Cloudy Sky.pdf'

                with PdfPages(pdfname) as pdf:

                    fig_width    = 6.00
                    fig_height   = 4.50
                    fig, axs     = plt.subplots(1, 2, figsize=(fig_width, fig_height))
                    suptitle_str = 'from ' +  anl_start_time_str + ' to ' + anl_end_time_str + ', datathinning: ' + datathinning + ', domain: ' + dom + ', ' + \
                                   str(fhours).zfill(2) + ' hours forecast, channel ' + str(channel).zfill(2)
                    fig.subplots_adjust(left=0.075, bottom=0.000, right=0.975, top=0.925, wspace=0.200, hspace=0.450)
                    fig.suptitle(suptitle_str, fontsize=7.5)

                    for idx, (scheme, configuration) in enumerate(zip(schemes[idsch_str], configurations[idsch_str])):

                        ax = axs[idx]
                        (ids_str, xrange_min, xrange_max, xrange_interval, yrange_min, yrange_max, yrange_interval) = scheme
                        xbin_center = np.arange(xrange_min, xrange_max + 0.99*xrange_interval, xrange_interval)
                        ybin_center = np.arange(yrange_min, yrange_max + 0.99*yrange_interval, yrange_interval)

                        #filename = dir_histo + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                                   #str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_pred_histogram2d_' + ids_str + '_All Sky.txt'
                        #filename = dir_histo + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                                   #str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_pred_histogram2d_' + ids_str + '_Clear Sky.txt'
                        filename = dir_histo + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                                   str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_pred_histogram2d_' + ids_str + '_Cloudy Sky.txt'
                        print(filename)

                        temp  = np.loadtxt(filename)
                        index = temp[0][:] != 0
                        xavg  = xbin_center[index]
                        yavg  = temp[0][index]
                        hist  = np.log10(temp[1:][:]/np.sum(temp[1:][:])/xrange_interval/yrange_interval)
                        print('max: ', np.max(hist))
                        print('min: ', np.min(hist))

                        (xvar, yvar, mtitle) = configuration
                        extent = [xrange_min, xrange_max, -5, 5]
                        index  = (ybin_center >= -5) & (ybin_center <= 5)

                        ax.plot([xrange_min, xrange_max], [0, 0], color='k', ls='--', linewidth=0.5)
                        ax.plot(xavg, yavg, color='k', ls='-',  linewidth=0.5)
                        pcm = ax.imshow(hist[index][:], cmap='RdYlBu_r', interpolation='none', origin='lower', \
                                        vmin=-5.0, vmax=0.5, extent=extent, aspect='auto', zorder=0)
                        #ax.set_xticks(np.arange(170.0, 400.0, 5.0))
                        #ax.set_yticks(np.arange(-40.0, 45.0, 5.0))
                        ax.set_xlabel(xvar, fontsize=7.5)
                        ax.set_ylabel(yvar, fontsize=7.5)
                        ax.tick_params('both', which='both', direction='in', labelsize=7.5, right=True, top=True)
                        #ax.set_title(title_str, fontsize=7.5, pad=4.0)
                        #ax.axis([180, 270, -40, 40])

                    clb = fig.colorbar(pcm, ax=axs, ticks=np.arange(-5.0, 1.0, 0.5), orientation='horizontal', pad=0.100, aspect=50, shrink=0.95)
                    clb.set_label('log(PDF)', fontsize=7.5, labelpad=4.0)
                    clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=7.5)

                    pdf.savefig(fig)
                    plt.cla()
                    plt.clf()
                    plt.close()
