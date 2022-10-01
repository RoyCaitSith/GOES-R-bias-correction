import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/24_Revision/BC_coeffs/28_2020082200_CON0_Ch13_Offline_ExBC1_CP1'
dir_in   = dir_main + '/02_Post_Process/2020082200_06h'
dir_save = dir_main + '/02_Post_Process/2020082200_06h'

anl_start_time    = datetime.datetime(2020, 8, 22,  0, 0, 0)
anl_end_time      = datetime.datetime(2020, 8, 23, 18, 0, 0)
forecast_hours    = [6]
domains           = ['d01']
thingrid          = ['030km']
channel           = 8
variable_name     = ['Constant', '$\mathregular{tlap^2}$', 'tlap', r'$\theta^4$', r'$\theta^3$', r'$\theta^2$', r'$\theta$', r'$C^4$', r'$C^3$', r'$C^2$', r'$C$']
variable_position = [3, 6, 7, 11, 12, 13, 14, 9, 8, 5, 4]
variable_use      = [1, 1, 1,  1,  1,  1,  1, 1, 1, 1, 1]
colors            = ['#7f7f7f', '#9edae5', '#1f77b4', '#f7b6d2', '#ffbb78', '#ff7f0e', '#d62728', '#a0bf7c', '#65934a', '#407434', '#03230e']

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

                anl_start_time_str = anl_start_time.strftime('%Y%m%d%H')
                anl_end_time_str   = anl_end_time.strftime('%Y%m%d%H')

                pdfname = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + \
                          dom + '_' + str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_BC_coefficients.pdf'

                with PdfPages(pdfname) as pdf:

                    fig_width  = 6.00
                    fig_height = 4.00
                    fig, axs   = plt.subplots(1, 1, figsize=(fig_width, fig_height))
                    maintitle  = 'from ' +  anl_start_time_str + ' to ' + anl_end_time_str + ', ' + dom + ', ' + \
                                 str(int(fhours)).zfill(2) + ' hours forecast, channel ' + str(channel).zfill(2)
                    fig.subplots_adjust(left=0.100, bottom=0.100, right=0.975, top=0.925, wspace=0.100, hspace=0.200)
                    print(maintitle)

                    ax         = axs
                    filename   = dir_in + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                                 str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_BC_coefficients.txt'

                    for idv, (varn, varp, varuse, color) in enumerate(zip(variable_name, variable_position, variable_use, colors)):
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

                            ax.plot(data, color=color, ls='-', linewidth=1.0, label=label)
                            ax.set_xticks([0, 41, 81, 101, 121, 141, 161, 181, 201, 221, 241])
                            ax.set_xticklabels(['12 May',  '13 May',  '14 May',  '19 May',  '24 May',  '29 May', \
                                                '03 June', '08 June', '13 June', '18 June', '23 June'], fontsize=7.5)
                            ax.set_yticks(np.arange(-2.0, 9.5, 1.0))
                            ax.set_xlabel('Time', fontsize=7.5)
                            ax.set_ylabel('Normalized Bias Correction Coefficient', fontsize=7.5)
                            ax.yaxis.set_minor_locator(ticker.FixedLocator(np.arange(-2.0, 9.1, 0.1)))
                            ax.tick_params('both', which='both', direction='in', labelsize=7.5, top=True, right=True)
                            ax.set_title(maintitle, fontsize=7.5)
                            ax.axis([0, len(data)-1, -2.0, 9.0])
                            #ax.grid(axis='y')

                    ax.plot([81, 81], [-10.0, 10.0], color='k', ls='--', linewidth=0.75)
                    ax.text( 56, 8.5, 'Spin-up', fontsize=7.5)
                    ax.text(224, 8.5, 'Monitor', fontsize=7.5)
                    ax.axvspan( 84,  89, facecolor='#c7c7c7', alpha=0.5)
                    ax.axvspan( 84,  89, facecolor='#c7c7c7', alpha=0.5)
                    ax.axvspan(111, 113, facecolor='#c7c7c7', alpha=0.5)
                    ax.axvspan(116, 117, facecolor='#c7c7c7', alpha=0.5)
                    ax.axvspan(127, 128, facecolor='#c7c7c7', alpha=0.5)
                    ax.axvspan(170, 171, facecolor='#c7c7c7', alpha=0.5)
                    ax.axvspan(179, 180, facecolor='#c7c7c7', alpha=0.5)
                    ax.axvspan(200, 205, facecolor='#c7c7c7', alpha=0.5)
                    ax.legend(loc='upper left', fontsize=7.5)

                    pdf.savefig(fig)
                    plt.cla()
                    plt.clf()
                    plt.close()
