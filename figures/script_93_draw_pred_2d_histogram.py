import os
import datetime
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import entropy
from matplotlib.backends.backend_pdf import PdfPages

dir_GOES  = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'

dir_main  = []
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/13_2017051118_CON0_Ch13_Offline_ExBC1_CP4/02_Post_Process/2017051118_06h')
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/13_2017051118_CON0_Ch13_Offline_ExBC1_CP4/02_Post_Process/2017051118_06h')
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/14_2017051118_CON0_Ch13_Offline_ExBC1_CP4_AR1/02_Post_Process/2017051118_06h')
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/15_2017051118_CON0_Ch13_Offline_ExBC1_CP4_AR2/02_Post_Process/2017051118_06h')
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/13_2017051118_CON0_Ch13_Offline_ExBC1_CP4/02_Post_Process/2017051118_06h')
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/13_2017051118_CON0_Ch13_Offline_ExBC1_CP4/02_Post_Process/2017051118_06h')
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/14_2017051118_CON0_Ch13_Offline_ExBC1_CP4_AR1/02_Post_Process/2017051118_06h')
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/15_2017051118_CON0_Ch13_Offline_ExBC1_CP4_AR2/02_Post_Process/2017051118_06h')
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/13_2017051118_CON0_Ch13_Offline_ExBC1_CP4/02_Post_Process/2017051118_06h')
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/13_2017051118_CON0_Ch13_Offline_ExBC1_CP4/02_Post_Process/2017051118_06h')
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/14_2017051118_CON0_Ch13_Offline_ExBC1_CP4_AR1/02_Post_Process/2017051118_06h')
dir_main.append(dir_GOES + '/24_Revision/BC_coeffs/15_2017051118_CON0_Ch13_Offline_ExBC1_CP4_AR2/02_Post_Process/2017051118_06h')

anl_start_time   = datetime.datetime(2017, 5, 11, 18, 0, 0)
anl_end_time     = datetime.datetime(2017, 6, 24, 18, 0, 0)
cycling_interval = 6
forecast_hours   = [6]
domains          = ['d01']
thingrid         = ['030km']
channel          = 8

Exps = ['Before BC, Clear Sky', 'After BC, Clear Sky', 'After BC, Clear Sky', 'After BC, Clear Sky', \
        'Before BC, Clear Sky', 'After BC, Clear Sky', 'After BC, Clear Sky', 'After BC, Clear Sky', \
        'Before BC, All Sky',   'ASRBC4, All Sky',     'ASRBC4_AR1, All Sky', 'ASRBC4_AR2, All Sky']
fnames = ['_Clear Sky.txt', '_Clear Sky.txt', '_Clear Sky.txt', '_Clear Sky.txt', \
          '_Clear Sky.txt', '_Clear Sky.txt', '_Clear Sky.txt', '_Clear Sky.txt', \
          '_All Sky.txt',   '_All Sky.txt',   '_All Sky.txt',    '_All Sky.txt']
textx = [-3.80, 0.225, 2.5]

schemes = {}
schemes.update({'Tlap (K)':              (['00', '01', '01', '01'],  -4.0,    4.0,  0.2, -60.0, 60.0, 0.2, -4.0,   4.0,  2.00)})
schemes.update({'Scan Angle (rad)':      (['02', '03', '03', '03'], 0.025,  1.225, 0.05, -60.0, 60.0, 0.2,  0.2,  1.20,  0.25)})
schemes.update({'${\overline{C}}$ (K)':  (['04', '05', '05', '05'],  0.50, 100.50,  1.0, -60.0, 60.0, 0.2,  0.0, 100.0, 25.00)})

for datathinning in thingrid:
    for dom in domains:
        for fhours in forecast_hours:

            anl_start_time_str = anl_start_time.strftime('%Y%m%d%H')
            anl_end_time_str   = anl_end_time.strftime('%Y%m%d%H')

            pdfname = './Figure_93_Conditional_Bias.pdf'

            with PdfPages(pdfname) as pdf:

                fig_width    = 10.00
                fig_height   = 8.50
                fig, axs     = plt.subplots(3, 4, figsize=(fig_width, fig_height))
                fig.subplots_adjust(left=0.075, bottom=-0.075, right=0.975, top=0.975, wspace=0.200, hspace=0.200)

                for idsch, xvar in enumerate(schemes.keys()):

                    (scheme, xrange_min, xrange_max, xrange_interval, yrange_min, yrange_max, yrange_interval, ex_min, ex_max, ex_interval) = schemes[xvar]

                    for idx, (dmain, exp, fname, sch) in enumerate(zip(dir_main[idsch*4:(idsch+1)*4], Exps[idsch*4:(idsch+1)*4], fnames[idsch*4:(idsch+1)*4], scheme)):

                        ax = axs[idsch, idx]
                        xbin_center = np.arange(xrange_min, xrange_max + 0.99*xrange_interval, xrange_interval)
                        ybin_center = np.arange(yrange_min, yrange_max + 0.99*yrange_interval, yrange_interval)

                        dir_histo = dmain
                        filename = dir_histo + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                                   str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_pred_histogram2d_' + sch + '_All Sky.txt'
                        print(filename)

                        temp = np.loadtxt(filename)
                        temp_total = np.sum(temp[1:][:])
                        print(temp_total)

                        dir_histo = dmain
                        filename = dir_histo + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                                   str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_pred_histogram2d_' + sch + fname
                        print(filename)

                        temp  = np.loadtxt(filename)
                        index = temp[0][:] != 0
                        xavg  = xbin_center[index]
                        yavg  = temp[0][index]
                        hist  = np.log10(temp[1:][:]/temp_total/xrange_interval/yrange_interval)

                        extent = [xrange_min-xrange_interval/2.0, xrange_max+xrange_interval/2.0, \
                                  yrange_min-yrange_interval/2.0, yrange_max+yrange_interval/2.0]
                        ax.plot([xrange_min, xrange_max], [0, 0], color='k', ls='--', linewidth=0.5)
                        ax.plot(xavg, yavg, color='k', ls='-',  linewidth=1.5)
                        pcm = ax.contourf(xbin_center, ybin_center, hist, levels=np.arange(-4.5, 0.6, 0.25), cmap='RdYlBu_r', zorder=0)
                        if idsch == 2:
                            ax.plot([55, 55], [-10.0, 10.0], color='k', ls='--', linewidth=1.00, zorder=0)

                        ax.set_xticks(np.arange(ex_min, ex_max+0.1, ex_interval))
                        ax.set_yticks(np.arange(-3, 3.1, 1.0))
                        ax.set_xlabel(xvar, fontsize=10.0)
                        if idx == 0:
                            ax.set_ylabel('All-Sky Scaled OmB', fontsize=10.0)
                        ax.tick_params('both', which='both', direction='in', labelsize=10.0, width=0.5, right=True, top=True)
                        ax.axis([ex_min, ex_max, -3, 3])

                        mtitle = '(' + chr(97+idsch*4+idx) + ') ' + exp
                        ax.text(textx[idsch], 2.5, mtitle, ha='left', va='center', color='black', fontsize=10.0, zorder=1)

                clb = fig.colorbar(pcm, ax=axs, ticks=np.arange(-4.5, 0.6, 0.50), orientation='horizontal', pad=0.050, aspect=37.5, shrink=1.00)
                clb.set_label('log(PDF)', fontsize=10.0, labelpad=4.0)
                clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0, width=0.5)

                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()
