import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/24_Revision/BC_coeffs/30_2017051118_CON0_Ch13_Offline_ExBC1_CP1'
dir_SOEM = dir_main + '/02_Post_Process/2017051118_06h'
dir_save = dir_main + '/02_Post_Process/2017051118_06h'

anl_start_time   = datetime.datetime(2017, 5, 11, 18, 0, 0)
anl_end_time     = datetime.datetime(2017, 6, 24, 18, 0, 0)

#2017051118_06h
cclr = 3.000
ccld = 25.00
eclr = 1.750
ecld = 10.55

cycling_interval = 6
forecast_hours   = [6]
domains          = ['d01']
thingrid         = ['030km']
channel          = 8

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

            anl_start_time_str = anl_start_time.strftime('%Y%m%d%H')
            anl_end_time_str   = anl_end_time.strftime('%Y%m%d%H')
            n_thingrid         = len(thingrid)

            pdfname  = dir_save + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + \
                       dom + '_' + str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_SOEM.pdf'
            filesave = dir_SOEM + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + \
                       dom + '_' + str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_SOEM_parameters.txt'
            fsave    = open(filesave, 'w')

            with PdfPages(pdfname) as pdf:

                suptitle_str = 'from ' +  anl_start_time_str + ' to ' + anl_end_time_str + ', domain: ' + dom + ', ' + \
                               str(int(fhours)).zfill(2) + ' hours forecast, channel ' + str(channel).zfill(2)
                fig_width  =  6.00
                fig_height =  4.50
                fig, axs   = plt.subplots(1, 1, figsize=(fig_width, fig_height))
                fig.subplots_adjust(left=0.075, bottom=0.100, right=0.920, top=0.925, wspace=0.100, hspace=0.200)
                fig.suptitle(suptitle_str, fontsize=7.5)
                print(suptitle_str)

                ax   = axs
                par  = ax.twinx()
                data = []

                (var, range_min, range_max, range_interval, var_color, lb) = ('OmB_after_BC', -74.75, 150.25, 0.5, '#1f77b4', 'after BC')
                filename = dir_SOEM + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
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

                data_amount = np.array(data_amount)/10000.0
                ax.plot(C, std, color=var_color, ls='-', linewidth=0.5, label='STD')
                par.plot(C, data_amount, color=var_color, ls='--', linewidth=0.5, label='Number')

                ymax1 = 90
                Cx = np.arange(-10.0, ymax1+0.1, 0.1)
                Cy = np.arange(-10.0, ymax1+0.1, 0.1)

                a_Cy = (eclr-ecld)/(cclr-ccld)
                b_Cy = cclr-eclr/a_Cy
                min_Cy = eclr
                max_Cy = ecld

                for icx, cx in enumerate(Cx):
                    Cy[icx] = np.min([np.max([a_Cy*(cx-b_Cy), min_Cy]), max_Cy])

                ax.plot(Cx, Cy, color='k', ls='-', linewidth=1.0, label='SOEM')

                print('cclr: ', cclr)
                fsave.write(str(cclr) + '\n')
                print('ccld: ', ccld)
                fsave.write(str(ccld) + '\n')
                print('eclr: ', eclr)
                fsave.write(str(eclr) + '\n')
                print('ecld: ', ecld)
                fsave.write(str(ecld) + '\n')

                ax.set_xticks(np.arange(-10, ymax1+1, 10))
                ax.set_yticks(np.arange(0, 15.1, 3.0))
                ax.set_xlabel('Symmetric Cloud Proxy Variable (K)', fontsize=7.5)
                ax.set_ylabel('Standard Deviation of Normalized OmB', fontsize=7.5)
                ax.xaxis.set_minor_locator(ticker.FixedLocator(np.arange(-10, ymax1+1, 1)))
                ax.yaxis.set_minor_locator(ticker.FixedLocator(np.arange(0, 15.1, 0.25)))
                ax.tick_params('both', which='both', direction='in', labelsize=7.5, top=True)
                ax.axis([-10, ymax1, 0, 15.0])
                ax.grid(axis='both')

                ymax2 = 2.5
                par.set_yticks(np.arange(0, ymax2+0.1, 0.5))
                par.set_ylabel('Number of OmB in Bin ($\mathregular{10^4}$)', fontsize=7.5)
                par.yaxis.set_minor_locator(ticker.FixedLocator(np.arange(0, ymax2+0.05, 0.1)))
                par.tick_params('both', which='both', direction='in', labelsize=7.5, top=True)
                par.axis([-10, ymax1, 0, ymax2])

                ax.legend(loc='lower right', fontsize=7.5)

                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()
