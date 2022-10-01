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

statuses         = {'before_BC': [-60.0, 60.0, 0.2],
                    'after_BC':  [-60.0, 60.0, 0.2]}

maintitle        = ['before bias correction', 'after bias correction']
channel          = 8
schemes          = {'All Sky':    [('normalized OmB', 0, 0.5, '#000000'), ('all-sky scaled OmB',  5, 1.0, '#d62728')],
                    'Clear Sky':  [('normalized OmB', 1, 0.5, '#000000'), ('all-sky scaled OmB',  6, 1.0, '#d62728')],
                    'Cloudy Sky': [('normalized OmB', 2, 0.5, '#000000'), ('all-sky scaled OmB',  7, 1.0, '#d62728')]}

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

            anl_start_time_str = anl_start_time.strftime('%Y%m%d%H')
            anl_end_time_str   = anl_end_time.strftime('%Y%m%d%H')

            for idsch, sch_str in enumerate(schemes.keys()):

                pdfname = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                          str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_normalized_OmB_histogram_' + \
                          sch_str + '.pdf'

                with PdfPages(pdfname) as pdf:

                    fig_width    = 6.00
                    fig_height   = 3.00
                    fig, axs     = plt.subplots(1, 2, figsize=(fig_width, fig_height))
                    suptitle_str = 'from ' +  anl_start_time_str + ' to ' + anl_end_time_str
                    fig.subplots_adjust(left=0.100, bottom=0.120, right=0.950, top=0.850, wspace=0.250, hspace=0.450)
                    fig.suptitle(suptitle_str, fontsize=7.5)

                    for ids, (status, mtitle) in enumerate(zip(statuses.keys(), maintitle)):

                        (range_min, range_max, range_interval) = statuses[status]
                        bin_center    = np.arange(range_min, range_max + range_interval, range_interval)
                        dist          = getattr(stats, 'norm')
                        data_gaussian = dist.rvs(size=5000000)
                        pdf_gaussian  = dist.pdf(bin_center)

                        ax = axs[ids]
                        ax.plot([ 0,  0], [0, 1000], color='k', ls='--', linewidth=0.5)
                        ax.plot([ 3,  3], [0, 1000], color='k', ls='--', linewidth=0.5)
                        ax.plot([-3, -3], [0, 1000], color='k', ls='--', linewidth=0.5)
                        ax.plot(bin_center, pdf_gaussian, color='k', ls='--', linewidth=0.5, label='Gaussian')

                        for (lb, idscheme, lw, color) in schemes[sch_str]:

                            filename = dir_histo + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                                       str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_' + status + '_histogram_' + \
                                       str(idscheme).zfill(2) + '.txt'
                            print(filename)

                            temp  = []
                            a     = open(filename)
                            iline = 0
                            for line in a:
                                item  = line.replace('\n', '')
                                if iline == 0:
                                    print('Amount of Data: ', item)
                                elif iline == 1:
                                    print('Average: ', item)
                                elif iline == 2:
                                    print('Standard Deviation: ', item)
                                elif iline == 3:
                                    print('RMS: ', item)
                                elif iline == 4:
                                    print('Skewness: ', item)
                                elif iline == 5:
                                    print('Kurtosis: ', item)
                                else:
                                    temp.append(float(item))
                                iline = iline + 1
                            a.close()

                            temp     = np.asarray(temp)
                            index    = np.where(temp)
                            pdf_data = temp/sum(temp)/range_interval
                            kld      = entropy(pdf_data, pdf_gaussian)
                            print('KLD: ', kld)

                            ax.plot(bin_center[index], pdf_data[index], color=color, linewidth=lw, label=lb)

                        ax.set_xticks(np.arange(-10.0, 15.0, 5.0))
                        ax.set_xlabel('Normalized OmB (K)', fontsize=7.5)
                        ax.set_ylabel('PDF', fontsize=7.5)
                        ax.set_yscale('log')
                        ax.xaxis.set_minor_locator(ticker.FixedLocator(np.arange(-10, 11, 1)))
                        ax.tick_params('both', which='both', direction='in', labelsize=7.5, right=True, top=True)
                        ax.set_title(sch_str + '_' + mtitle, fontsize=7.5)
                        ax.axis([-10.0, 10.0, 0.0001, 100.0])
                        ax.legend(loc='upper left', fontsize=7.5)

                    pdf.savefig(fig)
                    plt.cla()
                    plt.clf()
                    plt.close()
