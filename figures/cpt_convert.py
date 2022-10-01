import numpy as np                       # Import the Numpy package
import colorsys

def loadCPT(path):

    try:
        f = open(path)
    except:
        print ("File ", path, "not found")
        return None

    lines = f.readlines()

    f.close()

    x = np.array([])
    r = np.array([])
    g = np.array([])
    b = np.array([])

    colorModel = 'RGB'

    for idl, l in enumerate(lines):
        ls = l.split()
        if l[0] == '#':
            if ls[-1] == 'HSV':
                colorModel = 'HSV'
                continue
            else:
                continue
        if ls[0] == 'B' or ls[0] == 'F' or ls[0] == 'N':
            pass
        else:
            x=np.append(x,float(idl))
            r=np.append(r,float(ls[0]))
            g=np.append(g,float(ls[1]))
            b=np.append(b,float(ls[2]))
            #xtemp = float(ls[4])
            #rtemp = float(ls[5])
            #gtemp = float(ls[6])
            #btemp = float(ls[7])

        #x=np.append(x,xtemp)
        #r=np.append(r,rtemp)
        #g=np.append(g,gtemp)
        #b=np.append(b,btemp)

    if colorModel == 'HSV':
        for i in range(r.shape[0]):
            rr, gg, bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
        r[i] = rr ; g[i] = gg ; b[i] = bb

    if colorModel == 'RGB' and (r[0] > 1.0 or g[0] > 1.0 or b[0] > 1.0):
        r = r/255.0
        g = g/255.0
        b = b/255.0

    xNorm = (x - x[0])/(x[-1] - x[0])

    red     = []
    blue    = []
    green   = []
    red_r   = []
    blue_r  = []
    green_r = []

    n = len(x)
    for i in range(n):
        red.append([xNorm[i],r[i],r[i]])
        green.append([xNorm[i],g[i],g[i]])
        blue.append([xNorm[i],b[i],b[i]])
        red_r.append([xNorm[i],r[n-1-i],r[n-1-i]])
        green_r.append([xNorm[i],g[n-1-i],g[n-1-i]])
        blue_r.append([xNorm[i],b[n-1-i],b[n-1-i]])

    colorDict = {'red': red, 'green': green, 'blue': blue}
    colorDict_r = {'red': red_r, 'green': green_r, 'blue': blue_r}

    return colorDict, colorDict_r
