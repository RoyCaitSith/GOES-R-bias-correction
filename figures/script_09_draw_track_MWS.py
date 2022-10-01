import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import re
import numpy as np
import seaborn as sns
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from decimal import Decimal
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.gridspec import GridSpec
from mpl_toolkits.basemap import Basemap
from geopy.distance import great_circle

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/24_Revision/track_intensity'

name = 'Cindy'
sns_cmap = sns.color_palette('bright')
cases  = ['ASRC02', 'ASRBC0C02', 'ASRBC1C02', 'ASRBC4C02']
Exps   = ['ASR       ', 'ASRBC0 ', 'ASRBC1 ', 'ASRBC4 ']
colors = [sns_cmap[0], sns_cmap[1], sns_cmap[2], sns_cmap[3]]

forecast_start_time = datetime.datetime(2017, 6, 20, 12, 0, 0)
forecast_end_time   = datetime.datetime(2017, 6, 22, 12, 0, 0)
n_time = 9

pdfname = './Figure_09_Track_MWS.pdf'

file_best_track = dir_main + '/best_track/2017_03L_Cindy.csv'
df = pd.read_csv(file_best_track)
i_bt = 3
lat  = list(df['Latitude'][i_bt:i_bt+n_time])
lon  = list(df['Longitude'][i_bt:i_bt+n_time])
MWS  = list(df['MWS (Knot)'][i_bt:i_bt+n_time])
MSLP = list(df['MSLP (hPa)'][i_bt:i_bt+n_time])
print(lat)
print(lon)
print(MWS)

fig = plt.figure(1, [6.0, 6.0])
fig.subplots_adjust(left=0.075, bottom=0.025, right=0.950, top=1.000, wspace=0.250, hspace=0.000)
extent = [-97.0, -89.0, 24.0, 32.0]

# Draw best track
gs  = GridSpec(2, 1, figure=fig)
ax1 = fig.add_subplot(gs[0:])
m   = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='h', ax=ax1)
m.drawcoastlines(linewidth=0.2, color='k')
m.drawparallels(np.arange(24, 36, 2), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5)
m.drawmeridians(np.arange(-97, -87, 2), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5)

lon_bt = np.array(lon)
lat_bt = np.array(lat)
ax1.plot(lon, lat, 'o', color='k', ls='-', ms=2.50, linewidth=1.50, label='NHC', zorder=3)
ax1.plot(lon[2::4], lat[2::4], 'o', color='w', ms=1.00, zorder=3)

MWS_bt = np.array(MWS)
MSLP_bt = np.array(MSLP)

for idc, (case, exp, color) in enumerate(zip(cases, Exps, colors)):

    filename = dir_main + '/best_track/' + name + '_' + case + '.csv'
    df_track = pd.read_csv(filename)

    i    = i_bt-1
    lat  = list(df_track['Latitude'][i:i+n_time])
    lon  = list(df_track['Longitude'][i:i+n_time])
    MWS  = list(df_track['MWS (Knot)'][i:i+n_time])
    MSLP = list(df_track['MSLP (hPa)'][i:i+n_time])
    print(MWS)

    lat  = np.array(lat)
    lon  = np.array(lon)
    MWS  = np.array(list(map(float,  MWS)))
    MSLP = np.array(list(map(float, MSLP)))

    Err = []
    for idbt in range(n_time):
        loc_bt = (lat_bt[idbt], lon_bt[idbt])
        loc    = (lat[idbt],    lon[idbt])
        Err.append(great_circle(loc, loc_bt).kilometers)
    Err  = np.array(Err)
    RMSE = round(Decimal(str(np.sqrt(np.average(np.square(Err))))), 2)
    label = exp + str(RMSE) + ' km, '
    print(case + ', track: ' + str(RMSE))

    MWS = np.array(list(map(float, MWS)))
    Err  = MWS_bt - MWS
    RMSE = round(Decimal(str(np.sqrt(np.average(np.square(Err))))), 2)
    label = label + str(RMSE) + ' Knot'
    print(case + ', MWS: ' + str(RMSE))

    MSLP = np.array(list(map(float, MSLP)))
    Err  = MSLP_bt - MSLP
    RMSE = round(Decimal(str(np.sqrt(np.average(np.square(Err))))), 2)

    ax1.plot(lon, lat, 'o', color=color, ls='-', ms=2.50, linewidth=1.50, label=label, zorder=3)
    ax1.plot(lon[2::4], lat[2::4], 'o', color='w', ms=1.00, zorder=3)

ax1.text(-91.0, 25.0, '12 UTC 20 June', fontsize=10.0)
ax1.text(-96.0, 31.0, '12 UTC 22 June', fontsize=10.0)
ax1.legend(loc='lower left', fontsize=10.0, handlelength=1.0)

plt.savefig(pdfname)
