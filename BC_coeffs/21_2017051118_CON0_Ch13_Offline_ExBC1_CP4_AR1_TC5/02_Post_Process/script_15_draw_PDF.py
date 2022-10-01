import os
import math
import datetime
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import entropy
from scipy.interpolate import interp1d
from matplotlib.backends.backend_pdf import PdfPages

dir_GOES  = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main  = dir_GOES + '/24_Revision/BC_coeffs/21_2017051118_CON0_Ch13_Offline_ExBC1_CP4_AR1_TC5'
dir_histo = dir_main + '/02_Post_Process/2017051118_06h'
dir_save  = dir_main + '/02_Post_Process/2017051118_06h'

anl_start_time    = datetime.datetime(2017, 5, 11, 18, 0, 0)
anl_end_time      = datetime.datetime(2017, 6, 24, 18, 0, 0)
cycling_interval = 6
forecast_hours   = [6]
domains          = ['d01']
thingrid         = ['030km']
channel          = 8
schemes          = {'00': [('BT_bkg', 2, 100, 300, 1, '#000000'), \
                           ('BT_obs_before_BC', 0, 100, 300, 1, '#1f77b4'), \
                           ('BT_obs_after_BC', 1, 100, 300, 1, '#d62728')],
                    '01': [('cldeff_obs', 3, -100, 40, 1, '#1f77b4'), \
                           ('cldeff_bkg', 4, -100, 40, 1, '#000000')]}

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

            anl_start_time_str = anl_start_time.strftime('%Y%m%d%H')
            anl_end_time_str   = anl_end_time.strftime('%Y%m%d%H')

            for idsch, idsch_str in enumerate(schemes.keys()):

                #pdfname = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                          #str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_PDF_' + idsch_str + '_All Sky.pdf'
                #pdfname = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                          #str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_PDF_' + idsch_str + '_Clear Sky.pdf'
                pdfname = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                          str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_PDF_' + idsch_str + '_Cloudy Sky.pdf'

                with PdfPages(pdfname) as pdf:

                    fig_width    = 6.00
                    fig_height   = 3.00
                    fig, axs     = plt.subplots(1, 1, figsize=(fig_width, fig_height))
                    suptitle_str = 'from ' +  anl_start_time_str + ' to ' + anl_end_time_str + ', datathinning: ' + datathinning + ', domain: ' + dom + \
                                   ', '+ str(fhours).zfill(2) + ' hours forecast, channel ' + str(channel).zfill(2)
                    fig.subplots_adjust(left=0.100, bottom=0.120, right=0.980, top=0.925, wspace=0.250, hspace=0.450)
                    fig.suptitle(suptitle_str, fontsize=7.5)

                    ax = axs

                    for (lb, scheme, range_min, range_max, range_interval, color) in schemes[idsch_str]:

                        bin_center = np.arange(range_min, range_max + range_interval, range_interval)
                        #filename   = dir_histo + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                                     #str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_PDF_' + str(scheme).zfill(2) + '_All Sky.txt'
                        #filename   = dir_histo + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                                     #str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_PDF_' + str(scheme).zfill(2) + '_Clear Sky.txt'
                        filename   = dir_histo + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                                     str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_PDF_' + str(scheme).zfill(2) + '_Cloudy Sky.txt'
                        print(filename)

                        temp  = []
                        a     = open(filename)
                        iline = 0
                        for line in a:
                            item  = line.replace('\n', '')
                            temp.append(float(item))
                        a.close()

                        pdf_temp = np.asarray(temp)/np.sum(temp)
                        ax.plot(bin_center, pdf_temp, color=color, linewidth=1.0, linestyle='-',  label=lb)

                    ax.set_xticks(np.arange(range_min, range_max, 25.0))
                    ax.set_xlabel(lb, fontsize=7.5)
                    ax.set_ylabel('PDF', fontsize=7.5)
                    ax.set_yscale('log')
                    ax.xaxis.set_minor_locator(ticker.FixedLocator(np.arange(range_min, range_max, 5.0)))
                    ax.tick_params('both', which='both', direction='in', labelsize=7.5, right=True, top=True)
                    #ax.set_title(mtitle, fontsize=7.5)
                    #ax.axis([-10.0, 10.0, 0.0001, 100.0])
                    ax.legend(loc='upper left', fontsize=7.5)

                    pdf.savefig(fig)
                    plt.cla()
                    plt.clf()
                    plt.close()
