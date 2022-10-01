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
dir_main_1 = dir_GOES + '/24_Revision/BC_coeffs/04_estimate_SOEM_sea/02_Post_Process/2017051118_06h'

anl_start_time_1 = datetime.datetime(2017, 5, 11, 18, 0, 0)
anl_end_time_1   = datetime.datetime(2017, 6, 24, 18, 0, 0)
cycling_interval = 6
forecast_hours   = [6]
domains          = ['d01']
thingrid         = ['030km']
channel          = 8

sns_cmap  = sns.color_palette('bright')
Exps      = ['Before BC', 'Before BC']
colors    = [sns_cmap[3], sns_cmap[0]]
variables = {'OmB_before_BC': [-74.75, 75.25, 0.5, 'C_before_BC']}
schemes   = {'before_BC': [('Normalized', 0, 1.5, sns_cmap[0]), ('All-Sky Scaled',  3, 1.5, sns_cmap[3])]}

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

            n_thingrid = len(thingrid)
            pdfname = './Figure_92_SOEM_and_Normalized_OmB.pdf'

            with PdfPages(pdfname) as pdf:

                fig_width  = 7.50
                fig_height = 3.00
                fig, axs   = plt.subplots(1, 2, figsize=(fig_width, fig_height))
                fig.subplots_adjust(left=0.075, bottom=0.150, right=0.975, top=0.950, wspace=0.375, hspace=0.200)

                ax   = axs[0]
                par  = ax.twinx()
                data = []

                ax.set_zorder(2)
                par.set_zorder(1)
                ax.patch.set_visible(False)

                anl_start_time_str_1 = anl_start_time_1.strftime('%Y%m%d%H')
                anl_end_time_str_1   = anl_end_time_1.strftime('%Y%m%d%H')
                (exp, color) = (Exps[0], colors[0])
                dir_SOEM = dir_main_1

                for idv, var in enumerate(variables.keys()):

                    (range_min, range_max, range_interval, C_name) = variables[var]

                    filename = dir_SOEM + '/' + anl_start_time_str_1 + '_' + anl_end_time_str_1 + '_' + datathinning + '_' + dom + '_' + \
                               str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_' + var + '_SOEM.txt'
                    print(filename)

                    C           = []
                    std         = []
                    data_amount = []
                    a           = open(filename)

                    for line in a:
                        item = line.replace('\n', '').split()
                        if int(item[2]) > 10:
                            C.append(float(item[0]))
                            std.append(float(item[1]))
                            data_amount.append(int(item[2]))
                    a.close()

                    C = np.array(C)
                    std = np.array(std)
                    data_amount = np.log10(np.array(data_amount))

                    ax.plot(C, std, color=color, ls='-', linewidth=1.5, label='SD of OmBs')
                    ax.plot(C, data_amount+1000.0, color=color, ls='--', linewidth=1.5, label='Number of OmBs')
                    par.plot(C, data_amount, color=color, ls='--', linewidth=1.5, label=exp)
                    print(C[0], C[1], (std[0] + std[1])/2.0)
                    print(C[1], C[2], (std[1] + std[2])/2.0)
                    print(C[2], C[3], (std[2] + std[3])/2.0)
                    print(C[3], C[4], (std[3] + std[4])/2.0)
                    print(C[4], C[5], (std[4] + std[5])/2.0)
                    print(C[5], C[6], (std[5] + std[6])/2.0)

                ax.set_xticks(np.arange(0, 91, 10))
                ax.set_yticks(np.arange(0, 18.1, 3))
                ax.set_xlabel('${\overline{C}}$ (K)', fontsize=10.0)
                ax.set_ylabel('Standard Deviation of OmBs (K)', fontsize=10.0)
                ax.xaxis.set_minor_locator(ticker.FixedLocator(np.arange(0, 91, 1)))
                ax.yaxis.set_minor_locator(ticker.FixedLocator(np.arange(0, 18.1, 0.5)))
                ax.tick_params('both', which='both', direction='in', labelsize=10.0, top=True)
                ax.axis([0, 90, 0, 18])

                par.set_yticks(np.arange(1, 8.1, 1.0))
                par.set_ylabel('log(Number of OmBs in Bin)', fontsize=10.0)
                par.yaxis.set_minor_locator(ticker.FixedLocator(np.arange(1, 8.1, 0.1)))
                par.tick_params('both', which='both', direction='in', labelsize=10.0, top=True)
                par.axis([0, 90, 1, 8])

                cclr = 3.000
                ccld = 25.00
                eclr = 1.750
                ecld = 10.55

                a_Cy = (eclr-ecld)/(cclr-ccld)
                b_Cy = cclr-eclr/a_Cy
                min_Cy = eclr
                max_Cy = ecld

                Cx = np.arange(-10.0, 90.1, 0.001)
                Cy = np.arange(-10.0, 90.1, 0.001)
                for icx, cx in enumerate(Cx):
                    Cy[icx] = np.min([np.max([a_Cy*(cx-b_Cy), min_Cy]), max_Cy])

                ax.plot(Cx, Cy, color='k', ls='-', linewidth=1.5, label='SOEM')

                print('cclr: ', cclr)
                print('ccld: ', ccld)
                print('eclr: ', eclr)
                print('ecld: ', ecld)

                ax.legend(loc='upper right', fontsize=10.0, handlelength=1.50)
                ax.text(4.0, 17.0, '(a)', ha='center', va='center', color='black', fontsize=10.0)

                ax = axs[1]

                (range_min, range_max, range_interval) = (-60.0, 60.0, 0.2)
                bin_center    = np.arange(range_min, range_max + range_interval, range_interval)
                dist          = getattr(stats, 'norm')
                data_gaussian = dist.rvs(size=5000000)
                pdf_gaussian  = dist.pdf(bin_center)

                for idsch, idsch_str in enumerate(schemes.keys()):

                    ax.plot([ 0,  0], [0, 1000], color='k', ls='--', linewidth=1.0)
                    ax.plot(bin_center, pdf_gaussian, color='k', ls='--', linewidth=1.5, label='Gaussian')

                    for (lb, idscheme, lw, color) in schemes[idsch_str]:

                        dmain     = dir_main_1
                        dir_histo = dmain
                        filename  = dir_histo + '/' + anl_start_time_str_1 + '_' + anl_end_time_str_1 + '_' + datathinning + '_' + dom + '_' + \
                                    str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_' + idsch_str + '_histogram_' + \
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

                        ax.plot(bin_center[index], pdf_data[index], color=color, linewidth=lw, label=lb + ': ' + format(kld, '.4f'))

                    ax.set_xticks(np.arange(-10.0, 15.0, 5.0))
                    ax.set_xlabel('All-Sky Scaled OmB', fontsize=10.0)
                    ax.set_ylabel('PDF', fontsize=10.0)
                    ax.set_yscale('log')
                    ax.xaxis.set_minor_locator(ticker.FixedLocator(np.arange(-10, 11, 1)))
                    ax.tick_params('both', which='both', direction='in', labelsize=10.0, right=True, top=True)
                    ax.axis([-10.0, 10.0, 0.0001, 1000.0])
                    ax.legend(loc='upper right', fontsize=10.0, handlelength=1.50)
                    ax.text(-10+20*0.05, 400.0, '(b)', ha='center', va='center', color='black', fontsize=10.0)

                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()
