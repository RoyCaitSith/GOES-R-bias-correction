import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/24_Revision/track_intensity'
dir_best_track = dir_main + '/best_track'

forecast_hours = 48
sns_cmap = sns.color_palette('bright')

variables = {}
variables.update({'Track_Error (km)': ['Reduction in RMSE of Track Forecasts (km)', -40, 20, 10]})
variables.update({'MSLP_Error (hPa)': ['Reduction in RMSE of MSLP (hPa)', -4.0, 6.0, 2.0]})
variables.update({'MWS_Error (Knot)': ['Reduction in RMSE of MWS (Knot)', -4.0, 6.0, 2.0]})

pdfname = './Figure_11_Laura_errors.pdf'

with PdfPages(pdfname) as pdf:

    fig, axs = plt.subplots(3, 2, figsize=(12.0, 12.0))
    fig.subplots_adjust(left=0.075, bottom=0.050, right=0.980, top=0.975, wspace=0.150, hspace=0.200)
    width = 0.20

    for ids in range(0, 2):

        cases = {}
        if ids == 0:
            cases.update({'ASR':    [12, 'ASR',    sns_cmap[0]]})
            cases.update({'ASRBC0': [12, 'ASRBC0', sns_cmap[1]]})
            cases.update({'ASRBC1': [12, 'ASRBC1', sns_cmap[2]]})
            cases.update({'ASRBC4': [12, 'ASRBC4', sns_cmap[3]]})
        elif ids == 1:
            cases.update({'ASRCLD':    [12, 'ASRCLD',    sns_cmap[0]]})
            cases.update({'ASRBC0CLD': [12, 'ASRBC0CLD', sns_cmap[1]]})
            cases.update({'ASRBC1CLD': [12, 'ASRBC1CLD', sns_cmap[2]]})
            cases.update({'ASRBC4CLD': [12, 'ASRBC4CLD', sns_cmap[3]]})

        for idv, var in enumerate(variables.keys()):

            ax = axs[idv, ids]
            (ylabel, ymin, ymax, yint) = variables[var]

            for idc, case in enumerate(cases.keys()):

                if idc == 0:

                    (n_cycle, exp, color) = cases[case]
                    n_lead_time = int(forecast_hours/6.0 + 1.0)

                    filename = dir_best_track + '/Error_Laura_' + case + '.csv'
                    df = pd.read_csv(filename)

                    RMSE_0 = np.zeros((n_lead_time))
                    for idl in range(0, n_lead_time):
                        err = np.array(df[var][df['Forecast_Hour'] == idl*6.0])
                        RMSE_0[idl] = np.sqrt(np.average(np.square(err)))

                else:

                    (n_cycle, exp, color) = cases[case]
                    n_lead_time = int(forecast_hours/6.0 + 1.0)

                    filename = dir_best_track + '/Error_Laura_' + case + '.csv'
                    df = pd.read_csv(filename)

                    for idl in range(0, n_lead_time):

                        err = np.array(df[var][df['Forecast_Hour'] == idl*6.0])
                        RMSE_diff = RMSE_0[idl] - np.sqrt(np.average(np.square(err)))

                        if idl == 0 and idv == 1:
                            ax.bar(idl + (idc-1)*width-0.2, RMSE_diff, width, color=color, label=exp, zorder=3)
                            ax.text(idl, 0.0, str(np.around(RMSE_0[idl], 1)), ha='center', va='center', color='black', fontsize=10.0)
                        else:
                            ax.bar(idl + (idc-1)*width-0.2, RMSE_diff, width, color=color, zorder=3)
                            ax.text(idl, 0.0, str(np.around(RMSE_0[idl], 1)), ha='center', va='center', color='black', fontsize=10.0)

            extent = [-0.5, n_lead_time - 0.5, ymin, ymax]
            mtitle = '(' + chr(97+idv+ids*3) + ')'

            ax.set_xticks(np.arange(0, n_lead_time, 1))
            ax.set_yticks(np.arange(ymin, ymax+yint, yint))
            ax.set_xticklabels(['0', '6', '12', '18', '24', '30', '36', '42', '48'])
            ax.set_xlabel('Forecast Hours', fontsize=10.0)
            ax.set_ylabel(ylabel, fontsize=10.0)
            ax.tick_params('both', direction='in', labelsize=10.0)
            ax.grid(linewidth=0.5, color=sns_cmap[7], axis='y')
            ax.axis(extent)
            ax.text( 8.1, extent[2]+0.950*(extent[3]-extent[2]), mtitle, ha='left', va='center', color='black', fontsize=10.0)
            ax.text(-0.4, extent[2]+0.950*(extent[3]-extent[2]), 'Improvement', ha='left', va='center', color='black', fontsize=15.0)
            ax.text(-0.4, extent[2]+0.050*(extent[3]-extent[2]), 'Degradation', ha='left', va='center', color='black', fontsize=15.0)

            if idv == 1:
                ax.legend(loc='lower right', fontsize=10.0, handlelength=1.0)

    pdf.savefig(fig)
    plt.cla()
    plt.clf()
    plt.close()
