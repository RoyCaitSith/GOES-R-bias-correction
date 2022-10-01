import os
import re
import datetime

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/24_Revision/BC_coeffs/27_2020082200_CON0_Ch13_Offline_ExBC1_CP0'
dir_save = dir_main + '/01_Var_BC/save_files'
dir_out  = dir_main + '/02_Post_Process/2020082200_06h'

anl_start_time   = [datetime.datetime(2020, 8, 22,  0, 0, 0)]
anl_end_time     = [datetime.datetime(2020, 8, 23, 18, 0, 0)]
cycling_interval = 6
forecast_hours   = [6]
domains          = ['d01']
thingrid         = ['030km']
channel          = 8
periods          = {'Spin-up': (10, 0.025)}
n_period         = len(periods.keys())

for dom in domains:
    for fhours in forecast_hours:
        for datathinning in thingrid:

            anl_start_time_str = anl_start_time[0].strftime('%Y%m%d%H')
            anl_end_time_str   = anl_end_time[n_period-1].strftime('%Y%m%d%H')

            filename    = dir_out + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                          str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_BC_coefficients.txt'
            filename_pc = dir_out + '/' + anl_start_time_str + '_' + anl_end_time_str + '_' + datathinning + '_' + dom + '_' + \
                          str(fhours).zfill(2) + 'h_channel_' + str(channel).zfill(2) + '_BC_covariances.txt'
            print(filename)
            print(filename_pc)

            fsave    = open(filename, 'w')
            fsave_pc = open(filename_pc, 'w')
            n_time   = -1

            for idp, period in enumerate(periods.keys()):

                (ct, dc) = periods[period]
                time_now = anl_start_time[idp]

                while time_now <= anl_end_time[idp]:

                    if time_now == anl_start_time[0]:
                        cts = 0
                    else:
                        cts = 1

                    for ict in range(cts, ct+1):

                        delta_time   = time_now-anl_start_time[0]
                        delt         = delta_time.days + delta_time.seconds/3600.0/24
                        time_ict     = round(delt+(ict-1)*dc, 3)
                        n_time       = n_time + 1

                        ftime        = time_now + datetime.timedelta(hours = fhours)
                        time_str     = time_now.strftime('%Y%m%d%H')
                        ftime_str    = ftime.strftime('%Y%m%d%H')
                        dir_satbias  = dir_save + '/' + time_str + '_' + str(ict).zfill(2)

                        file_satbias = dir_satbias + "/satbias_out." + ftime_str + "." + dom
                        a            = open(file_satbias)
                        iline        = 0
                        for line in a:
                            iline = iline + 1
                            if iline == 9653 + (channel-8)*3 + 0:
                                temp = line.replace('\n', '')
                            if iline == 9653 + (channel-8)*3 + 1:
                                temp = '%3d' % n_time + '%8.3f ' % time_ict + ' ' + ftime_str + ' ' + temp + ' ' + line
                                fsave.write(temp)
                        a.close()

                        file_satbias = dir_satbias + "/satbias_pc.out." + ftime_str + "." + dom
                        a            = open(file_satbias)
                        iline        = 0
                        for line in a:
                            iline = iline + 1
                            if iline == 9653 + (channel-8)*3 + 0:
                                temp = line.replace('\n', '')
                            if iline == 9653 + (channel-8)*3 + 1:
                                temp = '%3d' % n_time + '%8.3f ' % time_ict + ' ' + ftime_str + ' ' + temp + ' ' + line
                                fsave_pc.write(temp)
                        a.close()

                    time_now = time_now + datetime.timedelta(hours = cycling_interval)

            fsave.close()
            fsave_pc.close()
