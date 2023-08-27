import numpy as np

dir_GOES = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction'
dir_main = dir_GOES + '/17_2020Laura_Experiments/berror'

f0 = open(dir_main + '/berror_stats', 'rb')
f1 = open(dir_main + '/berror_stats_SF4', 'w')

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

#Change agvi to 0
#istart = 0
#iend = (mlat+2)*nsig*nsig
#print(temp[istart:iend])

#agvi = temp[istart:iend].reshape(nsig, nsig, mlat+2)
#agvi[26:nsig, :, :] = 0
#agvi[26:nsig, 26:nsig, :] = 0
#temp[istart:iend] = agvi.reshape(-1)
#print(temp[istart:iend])
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
    if 't' in c3d[nc]:
        temp[mlat*26:mlat*nsig] = 0.5*temp[mlat*26:mlat*nsig]
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
