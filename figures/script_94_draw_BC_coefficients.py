import os
import datetime
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = []
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/13_2017051118_CON0_Ch13_Offline_ExBC1_CP4/02_Post_Process/2017051118_06h')
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/14_2017051118_CON0_Ch13_Offline_ExBC1_CP4_AR1/02_Post_Process/2017051118_06h')
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/15_2017051118_CON0_Ch13_Offline_ExBC1_CP4_AR2/02_Post_Process/2017051118_06h')

extent_1 = [[-1, 2.5, 1.0], [-1, 2.5, 1.0], [-1, 2.5, 1.0]]
extent_2 = [[0.0000001, 0.1], [0.0000001, 0.1], [0.0000001, 0.1]]
sns_cmap = sns.color_palette('bright')

anl_start_time    = datetime.datetime(2017, 5, 11, 18, 0, 0)
anl_end_time      = datetime.datetime(2017, 6, 24, 18, 0, 0)
forecast_hours    = [6]
domains           = ['d01']
thingrid          = ['030km']
channel           = 8
variable_name     = ['C', '$\mathregular{Tlap^2}$', 'Tlap', r'$\theta^4$', r'$\theta^3$', r'$\theta^2$', r'$\theta$', \
                     r'$\left(\frac{\overline{C}}{20}\right)^4$', r'$\left(\frac{\overline{C}}{20}\right)^3$', \
                     r'$\left(\frac{\overline{C}}{20}\right)^2$', r'$\frac{\overline{C}}{20}$']
variable_position = [3, 6, 7, 11, 12, 13, 14, 9, 8, 5, 4]
variable_use      = [[1, 1, 1,  1,  1,  1,  1, 1, 1, 1, 1], [1, 1, 1,  1,  1,  1,  1, 1, 1, 1, 1], [1, 1, 1,  1,  1,  1,  1, 1, 1, 1, 1]]
Exps              = ['Zhu_2014', 'Cameron_2016', 'Dee_2004']

colors = [sns_cmap[1], sns_cmap[0], sns_cmap[0], \
          sns_cmap[2], sns_cmap[2], sns_cmap[2], sns_cmap[2], \
          sns_cmap[3], sns_cmap[3], sns_cmap[3], sns_cmap[3]]
linestyles = [  'solid', 'dotted',  'solid', \
              'dashdot', 'dashed', 'dotted', 'solid', \
              'dashdot', 'dashed', 'dotted', 'solid']

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

                anl_start_time_str = anl_start_time.strftime('%Y%m%d%H')
                anl_end_time_str   = anl_end_time.strftime('%Y%m%d%H')

                pdfname = './Figure_94_BC_Coefficients.pdf'

                with PdfPages(pdfname) as pdf:

                    fig_width  = 9.00
                    fig_height = 6.50
                    fig, axs   = plt.subplots(3, 2, figsize=(fig_width, fig_height))
                    maintitle  = 'from ' +  anl_start_time_str + ' to ' + anl_end_time_str + ', ' + dom + ', ' + \
                                 str(int(fhours)).zfill(2) + ' hours forecast, channel ' + str(channel).zfill(2)
                    fig.subplots_adjust(left=0.075, bottom=0.125, right=0.975, top=0.950, wspace=0.200, hspace=0.150)
                    print(maintitle)

                    for idd, dmain in enumerate(dir_main):

                        ax       = axs[idd, 0]
                        dir_in   = dmain
                        filename = dir_in + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                                   str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_BC_coefficients.txt'

                        (ymin, ymax, yint) = extent_1[idd]
                        ytxt = ymin + 0.90*(ymax-ymin)

                        for idv, (varn, varp, varuse, color, ls) in enumerate(zip(variable_name, variable_position, variable_use[idd], colors, linestyles)):
                            if varuse == 1:

                                time  = []
                                data  = []
                                a     = open(filename)
                                iline = 0
                                for line in a:
                                    item  = line.replace('\n', '').split()
                                    time.append(float(item[0]))
                                    data.append(float(item[varp]))
                                    iline = iline + 1
                                a.close()

                                time  = np.array(time)
                                data  = np.array(data)
                                label = varn

                                ax.plot(data, color=color, ls=ls, linewidth=1.5, label=label, zorder=1)

                                ax.set_xticks([0, 41, 81, 121, 161, 201, 241])
                                if idd == 2:
                                    ax.set_xticklabels(['00 UTC\n12 May',  '00 UTC\n13 May',  '00 UTC\n14 May', '00 UTC\n24 May', \
                                                        '00 UTC\n03 June', '00 UTC\n13 June', '00 UTC\n23 June'], fontsize=10.0)
                                else:
                                    ax.set_xticklabels(['', '', '', '', '', '', ''], fontsize=10.0)

                                ax.set_yticks(np.arange(ymin, ymax+0.1, yint))
                                ax.set_ylabel('BC Coefficient', fontsize=10.0)
                                ax.yaxis.set_minor_locator(ticker.FixedLocator(np.arange(ymin, ymax+0.1, 0.2)))
                                ax.tick_params('both', which='both', direction='in', labelsize=10.0, top=True, right=True)
                                ax.axis([0, len(data)-1, ymin, ymax])

                        ax.plot([81, 81], [-10.0, 10.0], color='k', ls='--', linewidth=1.00, zorder=0)
                        ax.text( 30, ytxt, 'Spin-up', fontsize=10.0)
                        ax.text(210, ytxt, 'Monitor', fontsize=10.0)
                        ax.axvspan( 84,  89, facecolor=sns_cmap[7], alpha=0.5)
                        ax.axvspan( 84,  89, facecolor=sns_cmap[7], alpha=0.5)
                        ax.axvspan(111, 113, facecolor=sns_cmap[7], alpha=0.5)
                        ax.axvspan(116, 117, facecolor=sns_cmap[7], alpha=0.5)
                        ax.axvspan(127, 128, facecolor=sns_cmap[7], alpha=0.5)
                        ax.axvspan(170, 171, facecolor=sns_cmap[7], alpha=0.5)
                        ax.axvspan(179, 180, facecolor=sns_cmap[7], alpha=0.5)
                        ax.axvspan(200, 205, facecolor=sns_cmap[7], alpha=0.5)

                        mtitle = '(' + chr(97+idd) + ') ' + Exps[idd]
                        ax.set_title(mtitle, fontsize=10.0, pad=4.0)

                    for idd, dmain in enumerate(dir_main):

                        ax       = axs[idd, 1]
                        dir_in   = dmain
                        filename = dir_in + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                                   str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_BC_covariances.txt'

                        (ymin, ymax) = extent_2[idd]
                        ytxt = np.power(10, np.log10(ymin) + 0.90*(np.log10(ymax)-np.log10(ymin)))
                        print(ytxt)

                        for idv, (varn, varp, varuse, color, ls) in enumerate(zip(variable_name, variable_position, variable_use[idd], colors, linestyles)):
                            if varuse == 1:

                                time  = []
                                data  = []
                                a     = open(filename)
                                iline = 0
                                for line in a:
                                    item  = line.replace('\n', '').split()
                                    time.append(float(item[0]))
                                    data.append(float(item[varp]))
                                    iline = iline + 1
                                a.close()

                                time  = np.array(time)
                                data  = np.array(data)
                                label = varn

                                ax.plot(data, color=color, ls=ls, linewidth=1.5, label=label, zorder=1)

                                ax.set_xticks([0, 41, 81, 121, 161, 201, 241])
                                if idd == 2:
                                    ax.set_xticklabels(['00 UTC\n12 May',  '00 UTC\n13 May',  '00 UTC\n14 May', '00 UTC\n24 May', \
                                                        '00 UTC\n03 June', '00 UTC\n13 June', '00 UTC\n23 June'], fontsize=10.0)
                                else:
                                    ax.set_xticklabels(['', '', '', '', '', '', ''], fontsize=10.0)

                                ax.set_ylabel('Error Variance', fontsize=10.0)
                                ax.set_yscale('log')
                                ax.tick_params('both', which='both', direction='in', labelsize=10.0, top=True, right=True)
                                ax.axis([0, len(data)-1, ymin, ymax])

                        ax.plot([81, 81], [-10.0, 10.0], color='k', ls='--', linewidth=1.00, zorder=0)
                        ax.text( 30, ytxt, 'Spin-up', fontsize=10.0)
                        ax.text(210, ytxt, 'Monitor', fontsize=10.0)
                        ax.axvspan( 84,  89, facecolor=sns_cmap[7], alpha=0.5)
                        ax.axvspan( 84,  89, facecolor=sns_cmap[7], alpha=0.5)
                        ax.axvspan(111, 113, facecolor=sns_cmap[7], alpha=0.5)
                        ax.axvspan(116, 117, facecolor=sns_cmap[7], alpha=0.5)
                        ax.axvspan(127, 128, facecolor=sns_cmap[7], alpha=0.5)
                        ax.axvspan(170, 171, facecolor=sns_cmap[7], alpha=0.5)
                        ax.axvspan(179, 180, facecolor=sns_cmap[7], alpha=0.5)
                        ax.axvspan(200, 205, facecolor=sns_cmap[7], alpha=0.5)

                        mtitle = '(' + chr(100+idd) + ') ' + Exps[idd]
                        ax.set_title(mtitle, fontsize=10.0, pad=4.0)

                    ax.legend(loc='upper left', bbox_to_anchor=(-1.250, -0.225), fontsize=10.0, ncol=11, handlelength=1.5, columnspacing=1.50)

                    pdf.savefig(fig)
                    plt.cla()
                    plt.clf()
                    plt.close()
