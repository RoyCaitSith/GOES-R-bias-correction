import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.interpolate import griddata

dir_main = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/17_2020Laura_Experiments/berror'

variables = {'sf': [0, 15],
             'vp': [0, 15],
             't':  [0, 40],
             'q':  [0, 40]}

qoption = 2
lat = np.loadtxt(dir_main + '/Results/lat.txt')
sig = np.loadtxt(dir_main + '/Results/sig.txt')
print(sig[:])
#print(sig[26:])
extent = [-90.0, 90.0, 1.0, 0.0]
pdfname = dir_main + '/Figures/vz.pdf'

with PdfPages(pdfname) as pdf:

    mlat = len(lat)
    nsig = len(sig)

    lat_2d, sig_2d = np.meshgrid(np.arange(extent[0], extent[1] +    0.1,     0.1), \
                                 np.arange(extent[2], extent[3] - 0.0005, -0.0005), \
                                 sparse=False, indexing='xy')
    lat_1d, sig_1d = np.meshgrid(lat, sig, sparse=False, indexing='xy')

    lat_1d = lat_1d.ravel()
    sig_1d = sig_1d.ravel()

    fig_width  = 6.00
    fig_height = 6.00
    fig, axs   = plt.subplots(2, 2, figsize=(fig_width, fig_height))
    fig.subplots_adjust(left=0.075, bottom=0.000, right=0.975, top=0.950, wspace=0.250, hspace=0.050)

    for idv, var in enumerate(variables.keys()):

        (vmin, vmax) = variables[var]

        temp    = np.loadtxt(dir_main + '/Results/vz_' + var + '.txt').reshape(mlat+2, nsig)
        temp_1d = np.transpose(temp[1:mlat+1,:]).ravel()
        temp_2d = griddata((lat_1d, sig_1d), temp_1d, (lat_2d, sig_2d), method='linear')

        row = idv//2
        col = idv%2
        print(row, col)
        print(np.nanmin(temp_2d))
        print(np.nanmax(temp_2d))

        ax = axs[row, col]
        pcm1 = ax.imshow(temp_2d, cmap='jet', interpolation='none', origin='lower', \
                         vmin=vmin, vmax=vmax, extent=extent, aspect='auto', zorder=0)

        ax.set_xticks(np.arange(-90, 91, 30))
        ax.set_xticklabels(['90S', '60S', '30S', 'Eq', '30N', '60N', '90N'])
        ax.set_yticks(np.arange(0, 1.1, 0.2))
        ax.set_ylabel('Sigma', fontsize=7.5)
        ax.tick_params('both', direction='in', labelsize=7.5)
        ax.invert_yaxis()
        ax.axis(extent)

        mtitle = '(' + chr(97+idv) + ') ' + var
        ax.set_title(mtitle, fontsize=7.5, pad=4.0)

        clb = fig.colorbar(pcm1, ax=ax, orientation='horizontal', pad=0.100, aspect=25, shrink=0.95)
        clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=7.5)
        clb.set_label('grid units', fontsize=7.5, labelpad=4.0)

    pdf.savefig(fig)
    plt.cla()
    plt.clf()
    plt.close()
