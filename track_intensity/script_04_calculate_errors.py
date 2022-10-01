import datetime
import numpy as np
import pandas as pd
from geopy.distance import great_circle

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
#cases.update({'ASR': 4})
#cases.update({'ASRBC0': 4})
#cases.update({'ASRBC1': 4})
#cases.update({'ASRBC4': 4})
cases.update({'ASR': 12})
cases.update({'ASRBC0': 12})
cases.update({'ASRBC1': 12})
cases.update({'ASRBC4': 12})
cases.update({'ASRFD': 12})
cases.update({'ASRCLD': 12})
cases.update({'ASRBC0CLD': 12})
cases.update({'ASRBC1CLD': 12})
cases.update({'ASRBC4CLD': 12})
#cases.update({'ASR': 6})
#cases.update({'ASRBC0': 6})
#cases.update({'ASRBC1': 6})
#cases.update({'ASRBC4': 6})
#cases.update({'ASRFD': 6})
#cases.update({'ASRCLD': 6})
#cases.update({'ASRBC0CLD': 6})
#cases.update({'ASRBC1CLD': 6})
#cases.update({'ASRBC4CLD': 6})

if 'Cindy' in name:
    forecast_start_time = datetime.datetime(2017, 6, 20,  0, 0, 0)
if 'Laura' in name:
    forecast_start_time = datetime.datetime(2020, 8, 24,  0, 0, 0)

forecast_hours = 48

BT_df = pd.read_csv(file_best_track)
for case in cases.keys():

    n_cycle = cases[case]
    n_lead_time = int(forecast_hours/6 + 1)
    error_df = pd.DataFrame(0.0, index=np.arange(n_cycle*n_lead_time), \
                            columns=['Cycle', 'Forecast_Hour', 'Track_Error (km)', 'MSLP_Error (hPa)', 'MWS_Error (Knot)'])

    for idc in range(0, n_cycle):

        casename = case + 'C' + str(idc+1).zfill(2)
        filename = dir_main + '/' + name + '/' + casename + '/multi/fort.69'
        print(filename)
        df = pd.read_csv(filename, header=None, usecols=[2, 5, 6, 7, 8, 9])
        df.columns = ['Initial_Time', 'Forecast_Hour', 'Latitude', 'Longitude', 'MWS (Knot)', 'MSLP (hPa)']
        df.drop_duplicates(subset=['Forecast_Hour'], keep='last', inplace=True)

        Date_Time = []
        for it, fh in zip(df['Initial_Time'], df['Forecast_Hour']):
            Date_Time = Date_Time + [datetime.datetime.strptime(str(it), '%Y%m%d%H') + datetime.timedelta(hours = fh/100.0)]
        df.insert(loc=0, column='Date_Time', value=Date_Time)
        df.drop(columns=['Initial_Time', 'Forecast_Hour'], inplace=True)
        df.reset_index(drop=True, inplace=True)

        lat = list(df['Latitude'])
        lat = [x.split('N')[0] for x in lat]
        lat = pd.Series(map(float, lat))
        df['Latitude'] = 0.1*lat

        lon = list(df['Longitude'])
        lon = [x.split('W')[0] for x in lon]
        lon = pd.Series(map(float, lon))
        df['Longitude'] = -0.1*lon

        df.to_csv(dir_best_track + '/' + name + '_' + casename + '.csv', index=False)

        anl_end_time = forecast_start_time + datetime.timedelta(hours=6.0*idc)
        for idx, DT in enumerate(BT_df['Date_Time']):
            if datetime.datetime.strptime(DT, '%Y-%m-%d %H:%M:%S') == anl_end_time: BT_str_index = idx
        for idx, DT in enumerate(df['Date_Time']):
            if DT == anl_end_time: str_index = idx

        for idl in range(0, n_lead_time):

            index = idc*n_lead_time + idl
            error_df['Cycle'][index] = idc + 1
            error_df['Forecast_Hour'][index] = 6.0*idl

            loc = (df['Latitude'][str_index+idl], df['Longitude'][str_index+idl])
            BT_loc = (BT_df['Latitude'][BT_str_index+idl], BT_df['Longitude'][BT_str_index+idl])
            error_df['Track_Error (km)'][index] = great_circle(loc, BT_loc).kilometers
            error_df['MSLP_Error (hPa)'][index] = df['MSLP (hPa)'][str_index+idl] - BT_df['MSLP (hPa)'][BT_str_index+idl]
            error_df['MWS_Error (Knot)'][index] = df['MWS (Knot)'][str_index+idl] - BT_df['MWS (Knot)'][BT_str_index+idl]

    error_df.to_csv(dir_best_track + '/Error_' + name + '_' + case + '.csv', index=False)
