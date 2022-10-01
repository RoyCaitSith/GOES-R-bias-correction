#!/usr/bin/python

import os
os.environ['PROJ_LIB'] = r'/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/pkgs/proj4-4.9.3-h470a237_8/share/proj'

import re
import datetime
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from wrf import getvar
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/24_Revision/track_intensity'
dir_best_track = dir_main + '/best_track'
file_d01 = dir_main + '/sample/wrfout_d01_2017-06-20_00:00:00'
file_d02 = dir_main + '/sample/wrfout_d02_2017-06-20_00:00:00'

filenames = ['2017_03L_Cindy.csv', '2020_13L_Laura.csv']
start_idx = [1, 16]
end_idx = [12, 37]
zero_idx = [0, 0]
labels = ['Cindy (2017)', 'Laura (2020)']
markers = ['o', 'o']
print(start_idx)
print(end_idx)

sns_bright = sns.color_palette('bright')
sns_deep = sns.color_palette('deep')

fig, axs = plt.subplots(1, 2, figsize=(8.00, 3.50))
fig.subplots_adjust(left=0.075, bottom=0.025, right=0.975, top=0.975, wspace=0.175, hspace=0.150)

data_d01 = Dataset(file_d01)
lat_d01 = data_d01.variables['XLAT'][0,:,:]
lon_d01 = data_d01.variables['XLONG'][0,:,:]
extent = [lon_d01[0,0], lon_d01[-1,-1], lat_d01[0,0], lat_d01[-1,-1]]
data_d01.close()

print(extent)
print(np.max(lat_d01))
print(np.min(lat_d01))
print(np.max(lon_d01))
print(np.min(lon_d01))

lat_d02  = []
lon_d02  = []
data_d02 = Dataset(file_d02)
lat_temp = data_d02.variables['XLAT'][0,:,:]
lon_temp = data_d02.variables['XLONG'][0,:,:]
n_we     = len(lat_temp[0, :])
n_sn     = len(lat_temp[:, 0])
lat_d02  = lat_d02 + list(lat_temp[0, 0:n_we-1:1])
lat_d02  = lat_d02 + list(lat_temp[0:n_sn-1, n_we-1])
lat_d02  = lat_d02 + list(lat_temp[n_sn-1, n_we-1:0:-1])
lat_d02  = lat_d02 + list(lat_temp[n_sn-1:0:-1, 0])
lon_d02  = lon_d02 + list(lon_temp[0, 0:n_we-1:1])
lon_d02  = lon_d02 + list(lon_temp[0:n_sn-1, n_we-1])
lon_d02  = lon_d02 + list(lon_temp[n_sn-1, n_we-1:0:-1])
lon_d02  = lon_d02 + list(lon_temp[n_sn-1:0:-1, 0])
lat_d02.append(lat_temp[0, 0])
lon_d02.append(lon_temp[0, 0])
data_d02.close()

for idx, (filename, sidx, eidx, zidx, marker, label) in enumerate(zip(filenames, start_idx, end_idx, zero_idx, markers, labels)):

    ax = axs[idx]
    m = Basemap(llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], \
                projection='lcc', lat_1=40.0, lat_2=20.0, lon_0=-80.0, resolution='i', ax=ax)
    m.drawcoastlines(linewidth=0.2, color='k')
    m.fillcontinents(color=sns_deep[8])
    m.drawparallels(np.arange(0, 70, 10), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])
    m.drawmeridians(np.arange(-120, -35, 10), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=[0.749, 0.749, 0.749])

    x_lon_d02, y_lat_d02 = m(lon_d02, lat_d02, inverse=False)
    x_d01, y_d01 = m( -52.0, 43.5, inverse=False)
    x_d02, y_d02 = m( -70.0, 41.0, inverse=False)
    x_d03, y_d03 = m( -90.0, 21.5, inverse=False)
    x_d04, y_d04 = m( -92.5, 33.0, inverse=False)
    x_d05, y_d05 = m( -76.0, 17.8, inverse=False)
    x_d06, y_d06 = m( -87.0, 40.0, inverse=False)
    x_d07, y_d07 = m(-110.0, 44.0, inverse=False)
    ax.plot(x_lon_d02, y_lat_d02, color='k', linewidth=0.75, zorder=3)
    ax.text(x_d01, y_d01, '12 km', ha='center', va='center', color='black', fontsize=10.0, zorder=4)
    ax.text(x_d02, y_d02, '4 km', ha='center', va='center', color='black', fontsize=10.0, zorder=4)
    if idx == 0:
        ax.text(x_d03, y_d03, '00 UTC\n20 June', ha='center', va='center', color='black', fontsize=7.5, zorder=4)
        ax.text(x_d04, y_d04, '12 UTC\n22 June', ha='center', va='center', color='black', fontsize=7.5, zorder=4)
        ax.text(x_d07, y_d07, '(a)', ha='center', va='center', color='black', fontsize=7.5, zorder=4)
    else:
        ax.text(x_d05, y_d05, '00 UTC\n24 Aug',  ha='center', va='center', color='black', fontsize=7.5, zorder=4)
        ax.text(x_d06, y_d06, '00 UTC\n29 Aug',  ha='center', va='center', color='black', fontsize=7.5, zorder=4)
        ax.text(x_d07, y_d07, '(b)', ha='center', va='center', color='black', fontsize=7.5, zorder=4)

    file_best_track = dir_best_track + '/' + filename

    df = pd.read_csv(file_best_track)
    Latitude = list(df['Latitude'][sidx:eidx])
    Longitude = list(df['Longitude'][sidx:eidx])
    MWS = df['MWS (Knot)'][sidx:eidx]
    hh = df['Date_Time'][sidx:eidx]
    hh = [float(x[11:13]) for x in hh]
    print(df)

    x_Longitude, y_Latitude = m(Longitude, Latitude, inverse=False)
    sc2 = ax.scatter(x_Longitude, y_Latitude, c=MWS, marker=marker, edgecolor='none', vmin=20, vmax=125, s=25, cmap='jet', zorder=5+3*idx)
    ax.plot(x_Longitude[zidx::4], y_Latitude[zidx::4], marker, color='w', ms=1.50, zorder=6+3*idx)

    (x_legend, y_legend) = (-150.0, -50.0)
    (x_legend, y_legend) = m(x_legend, y_legend, inverse=False)
    ax.plot(x_legend, y_legend, marker, color=sns_bright[0], ms=2.50, label=label, zorder=4+3*idx)
    ax.legend(loc='lower right', fontsize=10.0, scatterpoints=1, handlelength=1.0)

grade = [20, 33, 63, 82, 95, 112, 125]
cat = ['TD', 'TS', 'Cat1', 'Cat2', 'Cat3', 'Cat4']
clb = fig.colorbar(sc2, ax=axs, ticks=grade, orientation='horizontal', pad=0.075, aspect=50.0, shrink=1.00)
clb.set_ticklabels(grade)
clb.set_label('MWS (Knot)', rotation=0, fontsize=10.0)
clb.ax.tick_params(axis='both', direction='in', labelsize=10.0)
for idx, lab in enumerate(cat):
    clb.ax.text(0.5*(grade[idx+1]+grade[idx]), -65.0, lab, ha='center', va='center', color='black', fontsize=10.0)

plt.savefig('./Figure_01_WRF_domain.pdf')
