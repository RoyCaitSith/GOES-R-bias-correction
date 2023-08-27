import numpy as np

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/17_2020Laura_Experiments/berror'

f0 = open(dir_main + '/berror_stats', 'rb')
f1 = open(dir_main + '/berror_stats_SF3', 'w')

reclen = np.fromfile(f0, dtype='>i4', count=1)
reclen.tofile(f1)
reclen = int(reclen/4)

dims = np.fromfile(f0, dtype='>i4', count=reclen)
dims.tofile(f1)
nsig = int(dims[0])
mlat = int(dims[1])
del dims

reclen = np.fromfile(f0, dtype='>i4', count=1)
reclen.tofile(f1)
reclen = int(reclen/4)

reclen = np.fromfile(f0, dtype='>i4', count=1)
reclen.tofile(f1)
reclen = int(reclen/4)

temp = np.fromfile(f0, dtype='>f4', count=reclen)
temp.tofile(f1)
lat = temp[0:mlat]
sig = temp[mlat:mlat+nsig]
del temp

reclen = np.fromfile(f0, dtype='>i4', count=1)
reclen.tofile(f1)
reclen = int(reclen/4)

reclen = np.fromfile(f0, dtype='>i4', count=1)
reclen.tofile(f1)
reclen = int(reclen/4)

temp = np.fromfile(f0, dtype='>f4', count=reclen)
temp.tofile(f1)
del temp

reclen = np.fromfile(f0, dtype='>i4', count=1)
reclen.tofile(f1)
reclen = int(reclen/4)

c3d  = []
c2d  = []
nc3d = 4
nc2d = 1

for nc in range(0, nc3d):

    reclen = np.fromfile(f0, dtype='>i4', count=1)
    reclen.tofile(f1)
    reclen = int(reclen/4)

    c3d.append(str(f0.read(9), encoding='utf-8'))
    f1.write(c3d[nc])
    c3d[nc] = c3d[nc][0:5].strip()
    print(c3d[nc])

    reclen = np.fromfile(f0, dtype='>i4', count=1)
    reclen.tofile(f1)
    reclen = int(reclen/4)

    reclen = np.fromfile(f0, dtype='>i4', count=1)
    reclen.tofile(f1)
    reclen = int(reclen/4)

    temp = np.fromfile(f0, dtype='>f4', count=reclen)
    temp.tofile(f1)
    del temp

    reclen = np.fromfile(f0, dtype='>i4', count=1)
    reclen.tofile(f1)
    reclen = int(reclen/4)

    reclen = np.fromfile(f0, dtype='>i4', count=1)
    reclen.tofile(f1)
    reclen = int(reclen/4)

    temp = np.fromfile(f0, dtype='>f4', count=reclen)
    print(temp[(mlat+2)*26:(mlat+2)*nsig])
    if c3d[nc] == 'sf':
        #temp[0:(mlat+2)*nsig] = np.where(temp[0:(mlat+2)*nsig] < 500000, temp[0:(mlat+2)*nsig], 500000)
        temp[(mlat+2)*26:(mlat+2)*nsig] = np.where(temp[(mlat+2)*26:(mlat+2)*nsig] < 300000, temp[(mlat+2)*26:(mlat+2)*nsig], 300000)
    temp.tofile(f1)
    del temp

    reclen = np.fromfile(f0, dtype='>i4', count=1)
    reclen.tofile(f1)
    reclen = int(reclen/4)

    reclen = np.fromfile(f0, dtype='>i4', count=1)
    reclen.tofile(f1)
    reclen = int(reclen/4)

    temp = np.fromfile(f0, dtype='>f4', count=reclen)
    temp.tofile(f1)
    del temp

    reclen = np.fromfile(f0, dtype='>i4', count=1)
    reclen.tofile(f1)
    reclen = int(reclen/4)

for nc in range(0, nc2d):

    reclen = np.fromfile(f0, dtype='>i4', count=1)
    reclen.tofile(f1)
    reclen = int(reclen/4)

    c2d.append(str(f0.read(9), encoding='utf-8'))
    f1.write(c2d[nc])
    c2d[nc] = c2d[nc][0:5].strip()
    print(c2d[nc])

    reclen = np.fromfile(f0, dtype='>i4', count=1)
    reclen.tofile(f1)
    reclen = int(reclen/4)

    reclen = np.fromfile(f0, dtype='>i4', count=1)
    reclen.tofile(f1)
    reclen = int(reclen/4)

    temp = np.fromfile(f0, dtype='>f4', count=reclen)
    temp.tofile(f1)
    del temp

    reclen = np.fromfile(f0, dtype='>i4', count=1)
    reclen.tofile(f1)
    reclen = int(reclen/4)

    reclen = np.fromfile(f0, dtype='>i4', count=1)
    reclen.tofile(f1)
    reclen = int(reclen/4)

    temp = np.fromfile(f0, dtype='>f4', count=reclen)
    temp.tofile(f1)
    del temp

    reclen = np.fromfile(f0, dtype='>i4', count=1)
    reclen.tofile(f1)
    reclen = int(reclen/4)

f0.close()
f1.close()
