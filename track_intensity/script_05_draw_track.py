import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import re
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap

#name = 'Cindy'
name = 'Laura'

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/24_Revision/track_intensity'
dir_best_track = dir_main + '/best_track'

if 'Cindy' in name:
    file_best_track = dir_best_track + '/2017_03L_Cindy.csv'
if 'Laura' in name:
    file_best_track = dir_best_track + '/2020_13L_Laura.csv'

cases = {}
#cases.update({'ASR': [4, 'ASR']})
#cases.update({'ASRBC0': [4, 'ASRBC0']})
#cases.update({'ASRBC1': [4, 'ASRBC1']})
#cases.update({'ASRBC4': [4, 'ASRBC4']})
cases.update({'ASR': [6, 'ASR']})
cases.update({'ASRBC0': [6, 'ASRBC0']})
cases.update({'ASRBC1': [6, 'ASRBC1']})
cases.update({'ASRBC4': [6, 'ASRBC4']})
cases.update({'ASRFD': [6, 'ASRFD']})
cases.update({'ASRCLD': [6, 'ASRCLD']})
cases.update({'ASRBC0CLD': [6, 'ASRBC0CLD']})
cases.update({'ASRBC1CLD': [6, 'ASRBC1CLD']})
cases.update({'ASRBC4CLD': [6, 'ASRBC4CLD']})

if 'Cindy' in name:
    anl_start_time      = datetime.datetime(2017, 6, 20,  0, 0, 0)
    forecast_start_time = datetime.datetime(2017, 6, 20,  6, 0, 0)
    forecast_end_time   = datetime.datetime(2017, 6, 23,  0, 0, 0)
if 'Laura' in name:
    anl_start_time      = datetime.datetime(2020, 8, 24,  0, 0, 0)
    forecast_start_time = datetime.datetime(2020, 8, 24,  6, 0, 0)
    forecast_end_time   = datetime.datetime(2020, 8, 29,  0, 0, 0)

extent = [-100.0, -70.0, 15.0, 35.0]
pdfname = dir_main + '/' + name + '/figures/01_Track.pdf'

colors = [[0.620, 0.604, 0.784], [0.459, 0.420, 0.694], [0.329, 0.153, 0.561], \
          [0.984, 0.416, 0.290], [0.851, 0.176, 0.149], [0.647, 0.059, 0.082], \
          [0.647, 0.059, 0.082], [0.647, 0.059, 0.082], [0.647, 0.059, 0.082], \
          [0.647, 0.059, 0.082], [0.647, 0.059, 0.082], [0.647, 0.059, 0.082]]

with PdfPages(pdfname) as pdf:
    for idc, case in enumerate(cases.keys()):

        (n_cycle, exp) = cases[case]

        fig = plt.figure(1, [6.0, 4.0])
        fig.subplots_adjust(left=0.075, bottom=0.050, right=0.950, top=0.980, wspace=0.000, hspace=0.000)

        #Read Best Track
        df = pd.read_csv(file_best_track)
        #print(df)

        index = []
        for idx, Date_Time in enumerate(df['Date_Time']):
            time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
            if time_now >= anl_start_time and time_now <= forecast_end_time: index = index + [idx]

        lat = list(df['Latitude'][index])
        lon = list(df['Longitude'][index])
        idx_anl_start_time = int((24-float(anl_start_time.strftime('%H')))%24/6)

        # Draw best track
        ax = fig.add_subplot(111)
        m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='h', ax=ax)
        m.drawcoastlines(linewidth=0.2, color='k')
        ax.plot(lon, lat, 'o', color='k', ls='-', ms=2.50, linewidth=1.50, label='NHC', zorder=3)
        ax.plot(lon[idx_anl_start_time::4], lat[idx_anl_start_time::4], 'o', color='w', ms=1.00, zorder=3)

        for icycle in range(0, n_cycle):

            casename = name + '_' + case + 'C' + str(icycle+1).zfill(2)
            filename = dir_main + '/best_track/' + casename + '.csv'

            df = pd.read_csv(filename)
            #print(df)

            index = []
            anl_end_time = forecast_start_time + datetime.timedelta(hours=6.0*icycle)
            for idx, Date_Time in enumerate(df['Date_Time']):
                time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                if time_now >= anl_end_time and time_now <= forecast_end_time: index = index + [idx]

            lat = list(df['Latitude'][index])
            lon = list(df['Longitude'][index])
            idx_anl_end_time = int((24-float(anl_end_time.strftime('%H')))%24/6)

            mtitle = exp + ': ' + anl_end_time.strftime('%H UTC %d Aug')
            ax.plot(lon, lat, 'o', color=colors[icycle], ls='-', ms=1.00, linewidth=0.60, label=mtitle, zorder=3)
            ax.plot(lon[idx_anl_end_time::4], lat[idx_anl_end_time::4], 'o', color='w', ms=0.40, zorder=3)

        ax.set_xticks(np.arange(-100, -65, 5))
        ax.set_xticklabels(['100W', '95W', '90W', '85W', '80W', '75W', '70W'])
        ax.set_yticks(np.arange(15, 40, 5))
        ax.set_yticklabels(['15N', '20N', '25N', '30N', '35N'])
        ax.tick_params('both', direction='in', labelsize=10.0)
        ax.axis(extent)
        ax.grid(True, linewidth=0.5)
        ax.text(-78.0, 19.0, '00 UTC 24 Aug', fontsize=10.0)
        ax.text(-91.5, 32.0, '12 UTC 27 Aug', fontsize=10.0)
        ax.legend(loc='lower left', fontsize=10.0, handlelength=1.0)

        pdf.savefig(fig)
        plt.cla()
        plt.clf()
        plt.close()
