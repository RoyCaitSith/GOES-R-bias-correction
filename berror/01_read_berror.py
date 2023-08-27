import numpy as np

dir_main = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/17_2020Laura_Experiments/berror'

f = open('berror_stats_SF6', 'rb')
reclen = int(np.fromfile(f, dtype='>i4', count=1)/4)
dims   = np.fromfile(f, dtype='>i4', count=reclen)
nsig   = int(dims[0])
mlat   = int(dims[1])
reclen = int(np.fromfile(f, dtype='>i4', count=1)/4)
del dims

reclen = int(np.fromfile(f, dtype='>i4', count=1)/4)
temp   = np.fromfile(f, dtype='>f4', count=reclen)
lat    = temp[0:mlat]
sig    = temp[mlat:mlat+nsig]
reclen = int(np.fromfile(f, dtype='>i4', count=1)/4)
del temp
np.savetxt(dir_main + '/Results/lat.txt', lat.reshape(-1), delimiter=',')
np.savetxt(dir_main + '/Results/sig.txt', sig.reshape(-1), delimiter=',')

reclen = int(np.fromfile(f, dtype='>i4', count=1)/4)
temp   = np.fromfile(f, dtype='>f4', count=reclen)

istart = 0
iend   = (mlat+2)*nsig*nsig
agvi   = temp[istart:iend].reshape(nsig, nsig, mlat+2)
np.savetxt(dir_main + '/Results/agvi.txt', agvi.reshape(-1), delimiter=',')

istart = (mlat+2)*nsig*nsig
iend   = (mlat+2)*nsig*nsig + (mlat+2)*nsig
bvi    = temp[istart:iend].reshape(nsig, mlat+2)
np.savetxt(dir_main + '/Results/bvi.txt', bvi.reshape(-1), delimiter=',')

istart = (mlat+2)*nsig*nsig + (mlat+2)*nsig
iend   = (mlat+2)*nsig*nsig + (mlat+2)*nsig + (mlat+2)*nsig
wgvi   = temp[istart:iend].reshape(nsig, mlat+2)
np.savetxt(dir_main + '/Results/wgvi.txt', wgvi.reshape(-1), delimiter=',')

reclen = int(np.fromfile(f, dtype='>i4', count=1)/4)
del temp

c3d   = []
c2d   = []
nc3d  = 4
nc2d  = 1
corz  = np.zeros((nc3d, nsig, mlat))
corqq = np.zeros((nsig, mlat))
corp  = np.zeros((nc2d, mlat))
hwll  = np.zeros((nc3d, nsig, mlat+2))
hwllp = np.zeros((nc2d, mlat+2))
vz    = np.zeros((nc3d, mlat+2, nsig))

for nc in range(0, nc3d):

    reclen = int(np.fromfile(f, dtype='>i4', count=1))
    c3d.append(str(f.read(9)[0:5].strip(), encoding='utf-8'))
    reclen = int(np.fromfile(f, dtype='>i4', count=1))
    print(c3d[nc])

    reclen = int(np.fromfile(f, dtype='>i4', count=1)/4)
    temp = np.fromfile(f, dtype='>f4', count=reclen)
    corz[nc,:,:] = temp[0:mlat*nsig].reshape(nsig, mlat)
    np.savetxt(dir_main + '/Results/corz_' + c3d[nc] + '.txt', corz[nc,:,:].reshape(-1), delimiter=',')

    if 'q' in c3d[nc]:
        corqq = temp[mlat*nsig:2*mlat*nsig].reshape(nsig, mlat)
    reclen = int(np.fromfile(f, dtype='>i4', count=1)/4)
    del temp
    np.savetxt(dir_main + '/Results/corqq.txt', corqq.reshape(-1), delimiter=',')

    reclen = int(np.fromfile(f, dtype='>i4', count=1)/4)
    temp = np.fromfile(f, dtype='>f4', count=reclen)
    hwll[nc,:,:] = temp[0:(mlat+2)*nsig].reshape(nsig, mlat+2)
    reclen = int(np.fromfile(f, dtype='>i4', count=1)/4)
    del temp
    np.savetxt(dir_main + '/Results/hwll_' + c3d[nc] + '.txt', hwll[nc,:,:].reshape(-1), delimiter=',')

    reclen = int(np.fromfile(f, dtype='>i4', count=1)/4)
    temp = np.fromfile(f, dtype='>f4', count=reclen)
    vz[nc,:,:] = temp[0:nsig*(mlat+2)].reshape(mlat+2, nsig)
    reclen = int(np.fromfile(f, dtype='>i4', count=1)/4)
    del temp
    np.savetxt(dir_main + '/Results/vz_' + c3d[nc] + '.txt', vz[nc,:,:].reshape(-1), delimiter=',')

for nc in range(0, nc2d):

    reclen = int(np.fromfile(f, dtype='>i4', count=1))
    c2d.append(str(f.read(9)[0:5].strip(), encoding='utf-8'))
    reclen = int(np.fromfile(f, dtype='>i4', count=1))
    print(c2d[nc])

    reclen = int(np.fromfile(f, dtype='>i4', count=1)/4)
    temp = np.fromfile(f, dtype='>f4', count=reclen)
    corp[nc,:] = temp[0:mlat].reshape(mlat)
    reclen = int(np.fromfile(f, dtype='>i4', count=1)/4)
    del temp
    np.savetxt(dir_main + '/Results/corp_' + c3d[nc] + '.txt', corp[nc,:].reshape(-1), delimiter=',')

    reclen = int(np.fromfile(f, dtype='>i4', count=1)/4)
    temp = np.fromfile(f, dtype='>f4', count=reclen)
    hwllp[nc,:] = temp[0:mlat+2].reshape(mlat+2)
    reclen = int(np.fromfile(f, dtype='>i4', count=1)/4)
    del temp
    np.savetxt(dir_main + '/Results/hwllp_' + c3d[nc] + '.txt', hwllp[nc,:].reshape(-1), delimiter=',')
