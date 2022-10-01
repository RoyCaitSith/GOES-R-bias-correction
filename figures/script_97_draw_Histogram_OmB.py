import os
import datetime
import numpy as np
import seaborn as sns
import scipy.stats as stats
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import entropy
from matplotlib.backends.backend_pdf import PdfPages

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main_1 = dir_GOES + '/24_Revision/BC_coeffs/03_2017051118_CON0_Ch13_Offline_ExBC1_CP0/02_Post_Process/2017051118_06h'
dir_main_2 = dir_GOES + '/24_Revision/BC_coeffs/04_2017051118_CON0_Ch13_Offline_ExBC1_CP1/02_Post_Process/2017051118_06h'
dir_main_3 = dir_GOES + '/24_Revision/BC_coeffs/05_2017051118_CON0_Ch13_Offline_ExBC1_CP4/02_Post_Process/2017051118_06h'

anl_start_time_1 = datetime.datetime(2017, 5, 11, 18, 0, 0)
anl_end_time_1   = datetime.datetime(2017, 6, 24, 18, 0, 0)
cycling_interval = 6
forecast_hours   = [6]
domains          = ['d01']
thingrid         = ['030km']
channel          = 8

sns_cmap = sns.color_palette('bright')

schemes = {}
schemes.update({'Clear Sky':  [('Before BC', 'before_BC', 4, 1.5, sns_cmap[7]), ('After BC', 'after_BC', 4, 1.5, sns_cmap[3])]})
schemes.update({'Cloudy Sky': [('Before BC', 'before_BC', 5, 1.5, sns_cmap[7]), ('After BC', 'after_BC', 5, 1.5, sns_cmap[3])]})

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

            n_thingrid = len(thingrid)
            pdfname = './Figure_97_Histogram_OmB.pdf'

            with PdfPages(pdfname) as pdf:

                fig_width  = 10.0
                fig_height = 6.00
                fig, axs   = plt.subplots(2, 3, figsize=(fig_width, fig_height))
                fig.subplots_adjust(left=0.075, bottom=0.100, right=0.975, top=0.950, wspace=0.300, hspace=0.325)

                anl_start_time_str_1 = anl_start_time_1.strftime('%Y%m%d%H')
                anl_end_time_str_1   = anl_end_time_1.strftime('%Y%m%d%H')

                (range_min, range_max, range_interval) = (-60.0, 60.0, 0.2)
                bin_center    = np.arange(range_min, range_max + range_interval, range_interval)
                dist          = getattr(stats, 'norm')
                data_gaussian = dist.rvs(size=5000000)
                pdf_gaussian  = dist.pdf(bin_center)

                for idsch, idsch_str in enumerate(schemes.keys()):

                    ax = axs[idsch, 0]
                    ax.plot([ 0,  0], [0, 1000], color='k', ls='--', linewidth=1.0)
                    ax.plot(bin_center, pdf_gaussian, color='k', ls='--', linewidth=1.5)

                    for (lb, status, idscheme, lw, color) in schemes[idsch_str]:

                        dmain     = dir_main_1
                        dir_histo = dmain
                        filename  = dir_histo + '/' + anl_start_time_str_1 + '_' + anl_end_time_str_1 + '_' + datathinning + '_' + dom + '_' + \
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
                                avg = float(item)
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

                        ax.plot(bin_center[index], pdf_data[index], color=color, linewidth=lw, label=lb + ': ' + format(avg, '.4f'))

                    ax.set_xticks(np.arange(-10.0, 11.0, 5.0))
                    ax.set_xlabel('All-Sky Scaled OmB', fontsize=10.0)
                    ax.set_ylabel('PDF', fontsize=10.0)
                    ax.set_yscale('log')
                    ax.xaxis.set_minor_locator(ticker.FixedLocator(np.arange(-10, 11, 1)))
                    ax.tick_params('both', which='both', direction='in', labelsize=10.0, right=True, top=True)
                    ax.axis([-10.0, 10.0, 0.0001, 100.0])
                    ax.legend(loc='upper right', fontsize=10.0, handlelength=1.50)

                    mtitle = '(' + chr(97+idsch) + str(1) + ') ASRBC0, ' + idsch_str
                    ax.set_title(mtitle, fontsize=10.0, pad=4.0)

                for idsch, idsch_str in enumerate(schemes.keys()):

                    ax = axs[idsch, 1]
                    ax.plot([ 0,  0], [0, 1000], color='k', ls='--', linewidth=1.0)
                    ax.plot(bin_center, pdf_gaussian, color='k', ls='--', linewidth=1.5)

                    for (lb, status, idscheme, lw, color) in schemes[idsch_str]:

                        dmain     = dir_main_2
                        dir_histo = dmain
                        filename  = dir_histo + '/' + anl_start_time_str_1 + '_' + anl_end_time_str_1 + '_' + datathinning + '_' + dom + '_' + \
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
                                avg = float(item)
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

                        ax.plot(bin_center[index], pdf_data[index], color=color, linewidth=lw, label=lb + ': ' + format(avg, '.4f'))

                    ax.set_xticks(np.arange(-10.0, 11.0, 5.0))
                    ax.set_xlabel('All-Sky Scaled OmB', fontsize=10.0)
                    ax.set_ylabel('PDF', fontsize=10.0)
                    ax.set_yscale('log')
                    ax.xaxis.set_minor_locator(ticker.FixedLocator(np.arange(-10, 11, 1)))
                    ax.tick_params('both', which='both', direction='in', labelsize=10.0, right=True, top=True)
                    ax.axis([-10.0, 10.0, 0.0001, 100.0])
                    ax.legend(loc='upper right', fontsize=10.0, handlelength=1.50)

                    mtitle = '(' + chr(97+idsch) + str(2) + ') ASRBC1, ' + idsch_str
                    ax.set_title(mtitle, fontsize=10.0, pad=4.0)

                for idsch, idsch_str in enumerate(schemes.keys()):

                    ax = axs[idsch, 2]
                    ax.plot([ 0,  0], [0, 1000], color='k', ls='--', linewidth=1.0)
                    ax.plot(bin_center, pdf_gaussian, color='k', ls='--', linewidth=1.5)

                    for (lb, status, idscheme, lw, color) in schemes[idsch_str]:

                        dmain     = dir_main_3
                        dir_histo = dmain
                        filename  = dir_histo + '/' + anl_start_time_str_1 + '_' + anl_end_time_str_1 + '_' + datathinning + '_' + dom + '_' + \
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
                                avg = float(item)
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

                        ax.plot(bin_center[index], pdf_data[index], color=color, linewidth=lw, label=lb + ': ' + format(avg, '.4f'))

                    ax.set_xticks(np.arange(-10.0, 11.0, 5.0))
                    ax.set_xlabel('All-Sky Scaled OmB', fontsize=10.0)
                    ax.set_ylabel('PDF', fontsize=10.0)
                    ax.set_yscale('log')
                    ax.xaxis.set_minor_locator(ticker.FixedLocator(np.arange(-10, 11, 1)))
                    ax.tick_params('both', which='both', direction='in', labelsize=10.0, right=True, top=True)
                    ax.axis([-10.0, 10.0, 0.0001, 100.0])
                    ax.legend(loc='upper right', fontsize=10.0, handlelength=1.50)

                    mtitle = '(' + chr(97+idsch) + str(3) + ') ASRBC4, ' + idsch_str
                    ax.set_title(mtitle, fontsize=10.0, pad=4.0)

                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()
