import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from matplotlib import ticker
from matplotlib.gridspec import GridSpec
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap

dir_main = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/24_Revision/rainfall/Cindy'

sns_cmap = sns.color_palette('bright')
cases    = ['ASRC02', 'ASRBC0C02', 'ASRBC1C02', 'ASRBC4C02']
Exps     = ['ASR', 'ASRBC0', 'ASRBC1', 'ASRBC4']
colors   = [sns_cmap[0], sns_cmap[1], sns_cmap[2], sns_cmap[3]]

threshold = [1.0, 5.0, 10.0, 15.0]
rain_levels = [1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0]
rain_labels = ['1.0', '1.5', '2', '3', '4', '5', '6', '8', '10', '15', '20', '25', '30', '35', '40']

domains = ['d02']
n_dom   = len(domains)
n_cases = len(cases)
n_thres = len(threshold)
n_time  = 8

ETS   = np.zeros((n_dom, n_cases, n_thres, n_time))
FAR   = np.zeros((n_dom, n_cases, n_thres, n_time))
FBIAS = np.zeros((n_dom, n_cases, n_thres, n_time))

for idd, dom in enumerate(domains):
    for idc, case in enumerate(cases):

        IMERG    = dir_main + '/IMERGC02/rainfall_interpolation_6h_' + dom + '.nc'
        filename = dir_main + '/' + case + '/rainfall_6h_' + dom + '.nc'
        print(IMERG)
        print(filename)

        for idt in range(0, n_time):

            print('Time: ', idt+1)

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
                ETS[idd, idc, idth, idt] = (N_H - ref)/(N_H + N_FA + N_M - ref)
                print(ETS[idd, idc, idth, idt])

pdfname = './Figure_10_ETS_Score_Rainfall.pdf'

with PdfPages(pdfname) as pdf:

    fig = plt.figure(1, [8.5, 12.0])
    fig.subplots_adjust(left=0.100, bottom=0.000, right=0.950, top=0.975, wspace=0.200, hspace=0.200)
    gs = GridSpec(4, 3, figure=fig)
    ax = fig.add_subplot(gs[0:2, 0:3])

    for idd, dom in enumerate(domains):
        for idth, thres in enumerate(threshold):
            for idc, (case, exp, color) in enumerate(zip(cases, Exps, colors)):

                width = 0.20
                ax.bar(idth+idc*0.20-0.3, np.average(ETS[idd, idc, idth, :]), width, color=color, label=exp, zorder=3)

            if idth == 0:
                ax.legend(loc='upper right', fontsize=10.0, handlelength=1.0)

        extent = [-0.5, 3.5, 0, 0.2]
        ax.set_xticks(np.arange(0, n_thres, 1))
        ax.set_xticklabels(['1.0 mm/hr', '5.0 mm/hr', '10.0 mm/hr', '15.0 mm/hr'])
        ax.set_yticks(np.arange(extent[2], extent[3]+0.02, 0.02))
        ax.set_ylabel('ETS', fontsize=10.0)
        ax.tick_params('both', direction='in', labelsize=10.0)
        ax.grid(linewidth=0.5, color=sns_cmap[7], axis='y')
        ax.axis(extent)

        ax.text(-0.25, 0.19, '(a)', ha='center', va='center', color='black', fontsize=10.0)

        axs = []
        cases.insert(0, 'IMERGC02')
        Exps.insert(0, 'IMERG')
        for idc, case in enumerate(cases):

            var = 'rainfall'
            filename = dir_main + '/' + case + '/rainfall_6h_' + dom + '.nc'
            ncfile   = Dataset(filename)
            #rain     = ncfile.variables[var][6,:,:]
            rain     = ncfile.variables[var][5,:,:]
            rain_lat = ncfile.variables['lat'][:,:]
            rain_lon = ncfile.variables['lon'][:,:]
            ncfile.close()

            row = idc//3
            col = idc%3

            ax = fig.add_subplot(gs[row+2, col])
            axs.append(ax)
            extent = [-95.0, -91.0, 27, 31]
            m  = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
            m.drawcoastlines(linewidth=0.2, color='k')
            m.drawparallels(np.arange(27, 32, 1), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5)
            m.drawmeridians(np.arange(-95, -90, 1), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5)

            rain[rain<=0] = 0
            pcm1 = ax.contourf(rain_lon, rain_lat, rain, locator=ticker.LogLocator(), levels=rain_levels, cmap='RdYlBu_r', extend='max', zorder=0)

            mtitle = '(' + chr(98+idc) + ') ' + Exps[idc]
            ax.set_title(mtitle, fontsize=10.0, pad=4.0)

        clb = fig.colorbar(pcm1, ax=axs, orientation='horizontal', pad=0.075, aspect=30, shrink=1.00)
        clb.set_label('6-hr Averaged Precipitation (mm/hr)', fontsize=10.0, labelpad=4.0)
        clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
        clb.ax.minorticks_off()
        clb.set_ticks(rain_levels)
        clb.set_ticklabels(rain_labels)

        pdf.savefig(fig)
        plt.cla()
        plt.clf()
