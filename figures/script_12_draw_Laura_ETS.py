import os
import re
import datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from matplotlib import ticker
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/24_Revision/rainfall'

sns_cmap = sns.color_palette('bright')
cases    = ['ASR',    'ASRBC0',    'ASRBC1',    'ASRBC4', \
            'ASRCLD', 'ASRBC0CLD', 'ASRBC1CLD', 'ASRBC4CLD']
Exps     = ['ASR', 'ASRBC0', 'ASRBC1', 'ASRBC4', 'ASRCLD', 'ASRBC0CLD', 'ASRBC1CLD', 'ASRBC4CLD']
colors   = [sns_cmap[0], sns_cmap[1], sns_cmap[2], sns_cmap[3], sns_cmap[0], sns_cmap[1], sns_cmap[2], sns_cmap[3]]

threshold = [1.0, 5.0, 10.0, 15.0]
extents   = [[0.0, 7.0, 0.04, 0.14], [0.0, 7.0, 0.02, 0.08], [0.0, 7.0, 0.00, 0.06], [0.0, 7.0, 0.00, 0.04]]

domains = ['d02']
n_dom   = len(domains)
n_cases = len(cases)
n_thres = len(threshold)
n_time  = 8
n_cycle = 12

ETS   = np.zeros((n_dom, n_cycle, n_cases, n_thres, n_time))
FAR   = np.zeros((n_dom, n_cycle, n_cases, n_thres, n_time))
FBIAS = np.zeros((n_dom, n_cycle, n_cases, n_thres, n_time))

for idd, dom in enumerate(domains):
    for icycle in range(0, n_cycle):
        for idc, case in enumerate(cases):

            IMERGname = 'IMERGC' + str(icycle+1).zfill(2)
            casename  = case + 'C' + str(icycle+1).zfill(2)
            IMERG     = dir_main + '/Laura/' + IMERGname + '/rainfall_interpolation_6h_' + dom + '.nc'
            filename  = dir_main + '/Laura/' + casename + '/rainfall_6h_' + dom + '.nc'
            print(IMERG)
            print(filename)

            for idt in range(0, n_time):

                var        = 'rainfall'
                ncfile     = Dataset(IMERG)
                IMERG_rain = ncfile.variables[var][idt,:,:]
                ncfile.close()

                ncfile   = Dataset(filename)
                rain     = ncfile.variables[var][idt,:,:]
                rain_lat = ncfile.variables['lat'][:,:]
                rain_lon = ncfile.variables['lon'][:,:]
                ncfile.close()

                for idth, thres in enumerate(threshold):

                    Hit         = (IMERG_rain >= thres) & (rain >= thres)
                    False_Alarm = (IMERG_rain  < thres) & (rain >= thres)
                    Miss        = (IMERG_rain >= thres) & (rain  < thres)
                    Correct_Neg = (IMERG_rain  < thres) & (rain  < thres)

                    N_H   = len(rain[Hit])
                    N_FA  = len(rain[False_Alarm])
                    N_M   = len(rain[Miss])
                    N_CN  = len(rain[Correct_Neg])
                    Total = N_H + N_FA + N_M + N_CN

                    ref = (N_H + N_FA)*(N_H + N_M)/Total
                    ETS[idd, icycle, idc, idth, idt] = (N_H - ref)/(N_H + N_FA + N_M - ref)

ETS_avg = np.average(ETS, axis=1)
pdfname = './Figure_12_Laura_ETS.pdf'

with PdfPages(pdfname) as pdf:

    for idd, dom in enumerate(domains):

        fig, axs = plt.subplots(2, 4, figsize=(12.0, 6.0))
        fig.subplots_adjust(left=0.050, bottom=0.100, right=0.975, top=0.975, wspace=0.300, hspace=0.225)

        for idth, thres in enumerate(threshold):

            for idc, (case, color) in enumerate(zip(cases, colors)):

                row = idth
                col = idc//4
                ax  = axs[col, row]

                ax.plot(np.arange(n_time), ETS_avg[idd, idc, idth, :], color=color, ls='-', linewidth=1.50, label=Exps[idc], zorder=3)

                if idc%4 == 3:

                    ax.set_xticks(np.arange(0, n_time, 1))
                    ax.set_xticklabels(['6', '12', '18', '24', '30', '36', '42', '48'])
                    ax.set_xlabel('Forecast Hours (h)', fontsize=10.0)
                    ax.set_ylabel('ETS', fontsize=10.0)
                    ax.tick_params('both', direction='in', labelsize=10.0)
                    ax.axis(extents[idth])
                    ax.grid(True, linewidth=0.5, color=sns_cmap[7])

                    mtitle = '(' + chr(97+idth+4*col) + ') ' + str(thres) + ' mm/hr'
                    ax.text(0.25, extents[idth][2]+0.950*(extents[idth][3]-extents[idth][2]), mtitle, ha='left', va='center', color='black', fontsize=10.0)

                    if idth==0: ax.legend(loc='lower left', fontsize=10.0)

        pdf.savefig(fig)
        plt.cla()
        plt.clf()
        plt.close()
