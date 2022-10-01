import os
import math
import datetime
import numpy as np
import seaborn as sns
import scipy.stats as stats
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import entropy
from scipy.interpolate import interp1d
from matplotlib.backends.backend_pdf import PdfPages

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'

dir_main = []
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/29_2017051118_CON0_Ch13_Offline_ExBC1_CP0/02_Post_Process/2017051118_06h')
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/29_2017051118_CON0_Ch13_Offline_ExBC1_CP0/02_Post_Process/2017051118_06h')
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/29_2017051118_CON0_Ch13_Offline_ExBC1_CP0/02_Post_Process/2017051118_06h')
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/30_2017051118_CON0_Ch13_Offline_ExBC1_CP1/02_Post_Process/2017051118_06h')
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/21_2017051118_CON0_Ch13_Offline_ExBC1_CP4_AR1_TC5/02_Post_Process/2017051118_06h')

anl_start_time   = datetime.datetime(2017, 5, 11, 18, 0, 0)
anl_end_time     = datetime.datetime(2017, 6, 24, 18, 0, 0)
cycling_interval = 6
forecast_hours   = [6]
domains          = ['d01']
thingrid         = ['030km']
channel          = 8

sns_cmap = sns.color_palette('bright')
Exps     = ['BT_bkg', 'BT_obs Before BC', 'BT_obs in ASRBC0', 'BT_obs in ASRBC1', 'BT_obs in ASRBC4']
colors   = [sns_cmap[6], sns_cmap[0], sns_cmap[1], sns_cmap[2], sns_cmap[3]]
schemes  = [2, 0, 1, 1, 1]
(range_min, range_max, range_interval) = (100, 300, 1)

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

            anl_start_time_str = anl_start_time.strftime('%Y%m%d%H')
            anl_end_time_str   = anl_end_time.strftime('%Y%m%d%H')

            pdfname = './Figure_07_PDF_BT.pdf'
            with PdfPages(pdfname) as pdf:

                fig_width  = 6.00
                fig_height = 5.00
                fig, axs   = plt.subplots(2, 1, figsize=(fig_width, fig_height))
                fig.subplots_adjust(left=0.125, bottom=0.100, right=0.975, top=0.950, wspace=0.250, hspace=0.350)

                ax = axs[0]
                ax.plot([ 238,  238], [0, 1000], color='k', ls='--', linewidth=1.0, zorder=2)

                for (dmain, exp, color, scheme) in zip(dir_main, Exps, colors, schemes):

                    bin_center = np.arange(range_min, range_max + range_interval, range_interval)
                    dir_histo  = dmain
                    filename   = dir_histo + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                                 str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_PDF_' + str(scheme).zfill(2) + '_All Sky.txt'
                    print(filename)

                    temp  = []
                    a     = open(filename)
                    iline = 0
                    for line in a:
                        item  = line.replace('\n', '')
                        temp.append(float(item))
                    a.close()
                    temp_total = np.sum(temp)

                    filename   = dir_histo + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                                 str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_PDF_' + str(scheme).zfill(2) + '_Clear Sky.txt'
                    print(filename)

                    temp  = []
                    a     = open(filename)
                    iline = 0
                    for line in a:
                        item  = line.replace('\n', '')
                        temp.append(float(item))
                    a.close()

                    pdf_temp = np.asarray(temp)/temp_total
                    if exp == 'BT_bkg':
                        pdf_bkg = pdf_temp
                        index   = pdf_temp > 0

                    kld = entropy(pdf_temp[index], pdf_bkg[index])
                    if exp == 'BT_bkg':
                        ax.plot(bin_center, pdf_temp, color=color, linewidth=1.5, linestyle='-', label=exp, zorder=2)
                    else:
                        ax.plot(bin_center, pdf_temp, color=color, linewidth=1.5, linestyle='-', label=exp + ': ' + format(kld, '.4f'), zorder=2)
                    print('KLD: ', kld)

                ax.set_xticks(np.arange(range_min, range_max, 5.0))
                ax.set_xlabel('BT (K)', fontsize=10.0)
                ax.set_ylabel('PDF of BTs', fontsize=10.0)
                ax.xaxis.set_minor_locator(ticker.FixedLocator(np.arange(range_min, range_max, 5.0)))
                ax.tick_params('both', which='both', direction='in', labelsize=10.0, right=True, top=True)
                ax.axis([195, 260, 0, 0.06])
                ax.grid(linewidth=0.5, color=sns_cmap[7], zorder=0)
                ax.legend(loc='upper left', fontsize=10.0, handlelength=1.0)

                mtitle = '(a) Clear Sky'
                ax.set_title(mtitle, fontsize=10.0, pad=4.0)

                ax = axs[1]
                ax.plot([ 240,  240], [0, 1000], color='k', ls='--', linewidth=1.0, zorder=2)
                ax.plot([ 228,  228], [0, 1000], color='k', ls='--', linewidth=1.0, zorder=2)

                for (dmain, exp, color, scheme) in zip(dir_main, Exps, colors, schemes):

                    bin_center = np.arange(range_min, range_max + range_interval, range_interval)
                    dir_histo  = dmain
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

                    pdf_temp = np.asarray(temp)/temp_total
                    if exp == 'BT_bkg':
                        pdf_bkg = pdf_temp
                        index   = pdf_temp > 0

                    kld = entropy(pdf_temp[index], pdf_bkg[index])
                    if exp == 'BT_bkg':
                        ax.plot(bin_center, pdf_temp, color=color, linewidth=1.5, linestyle='-', label=exp, zorder=2)
                    else:
                        ax.plot(bin_center, pdf_temp, color=color, linewidth=1.5, linestyle='-', label=exp + ': ' + format(kld, '.4f'), zorder=2)
                    print('KLD: ', kld)

                ax.set_xticks(np.arange(range_min, range_max, 5.0))
                ax.set_xlabel('BT (K)', fontsize=10.0)
                ax.set_ylabel('PDF of BTs', fontsize=10.0)
                ax.xaxis.set_minor_locator(ticker.FixedLocator(np.arange(range_min, range_max, 5.0)))
                ax.tick_params('both', which='both', direction='in', labelsize=10.0, right=True, top=True)
                ax.axis([195, 260, 0, 0.06])
                ax.grid(linewidth=0.5, color=sns_cmap[7], zorder=0)
                ax.legend(loc='upper left', fontsize=10.0, handlelength=1.0)

                mtitle = '(b) Cloudy Sky'
                ax.set_title(mtitle, fontsize=10.0, pad=4.0)

                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()
