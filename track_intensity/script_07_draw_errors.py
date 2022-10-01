import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#name = 'Cindy'
name = 'Laura'

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/24_Revision/track_intensity'
dir_best_track = dir_main + '/best_track'

cases = {}
variables = {}

#cases.update({'ASR':       [4, 'ASR',       [0.502, 0.502, 0.502]]})
#cases.update({'ASRBC0':    [4, 'ASRBC0',    [0.988, 0.682, 0.569]]})
#cases.update({'ASRBC1':    [4, 'ASRBC1',    [0.984, 0.416, 0.290]]})
#cases.update({'ASRBC4':    [4, 'ASRBC4',    [0.871, 0.176, 0.149]]})
cases.update({'ASR':       [12, 'ASR',       [0.502, 0.502, 0.502]]})
cases.update({'ASRBC0':    [12, 'ASRBC0',    [0.988, 0.682, 0.569]]})
cases.update({'ASRBC1':    [12, 'ASRBC1',    [0.984, 0.416, 0.290]]})
cases.update({'ASRBC4':    [12, 'ASRBC4',    [0.871, 0.176, 0.149]]})
cases.update({'ASRFD':     [12, 'ASRFD',     [0.871, 0.176, 0.149]]})
cases.update({'ASRCLD':    [12, 'ASRCLD',    [0.871, 0.176, 0.149]]})
cases.update({'ASRBC0CLD': [12, 'ASRBC0CLD', [0.871, 0.176, 0.149]]})
cases.update({'ASRBC1CLD': [12, 'ASRBC1CLD', [0.871, 0.176, 0.149]]})
cases.update({'ASRBC4CLD': [12, 'ASRBC4CLD', [0.871, 0.176, 0.149]]})

variables.update({'Track_Error (km)': ['RMSE of Track (km)', 0, 500, 50]})
variables.update({'MSLP_Error (hPa)': ['RMSE of MSLP (hPa)', 0, 40,  5]})
variables.update({'MWS_Error (Knot)': ['RMSE of MWS (Knot)', 0, 70,  10]})

pdfname = dir_main + '/' + name + '/figures/03_Error.pdf'

forecast_hours = 48

with PdfPages(pdfname) as pdf:

    for var in variables.keys():

        fig, axs = plt.subplots(1, 1, figsize=(9.0, 6.0))
        fig.subplots_adjust(left=0.075, bottom=0.075, right=0.975, top=0.975, wspace=0.250, hspace=0.225)
        (ylabel, ymin, ymax, yint) = variables[var]

        ax = axs
        width = 0.15

        for idc, case in enumerate(cases.keys()):

            (n_cycle, exp, color) = cases[case]
            n_lead_time = int(forecast_hours/6.0 + 1.0)
            extent = [-0.5, n_lead_time - 0.5, ymin, ymax]

            filename = dir_best_track + '/Error_' + name + '_' + case + '.csv'
            print(filename)
            df = pd.read_csv(filename)

            for idl in range(0, n_lead_time):

                err = np.array(df[var][df['Forecast_Hour'] == idl*6.0])
                RMSE = np.sqrt(np.average(np.square(err)))

                if idl == 0:
                    ax.bar(idl + idc*0.15-0.3, RMSE, width, color=color, label=exp, zorder=3)
                else:
                    ax.bar(idl + idc*0.15-0.3, RMSE, width, color=color, zorder=3)

        ax.set_xticks(np.arange(0, n_lead_time, 1))
        ax.set_yticks(np.arange(ymin, ymax+yint, yint))
        ax.set_xticklabels(['0', '6', '12', '18', '24', '30', '36', '42', '48'])
        ax.set_xlabel('Forecast Hours', fontsize=10.0)
        ax.set_ylabel(ylabel, fontsize=10.0)
        ax.tick_params('both', direction='in', labelsize=10.0)
        ax.axis(extent)
        ax.legend(loc='upper left', fontsize=10.0, handlelength=1.0)

        pdf.savefig(fig)
        plt.cla()
        plt.clf()
        plt.close()
