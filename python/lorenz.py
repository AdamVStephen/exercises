
# Example references https://stackoverflow.com/questions/34571749/how-do-i-create-a-3d-line-plot-in-matplotlib-from-the-data-in-arrays

import numpy as np
import pdb

import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection


def lorenz(x,y,z,t,rho=28.0, sigma=10.0, beta = 8./3.):
    xdot = sigma * (y-x)
    ydot = x * (rho - z) - y
    zdot = x*y - beta*z
    return np.array([xdot, ydot, zdot])

def rkstep(x,y,z,t,dt,f = lorenz):
    f1 = dt * f(x,y,z,t)
    f2 = dt * f(x+0.5*f1[0], y+ 0.5*f1[1], z+0.5*f1[2],t+0.5*dt)
    f3 = dt * f(x+0.5*f2[0], y+ 0.5*f2[1], z+0.5*f2[2],t+0.5*dt)
    f4 = dt * f(x+f3[0], y+f3[1], z+f3[2], t+dt)
    dx = (f1[0] + 2*f2[0] + 2*f3[0] + f4[0])/6.0
    dy = (f1[1] + 2*f2[1] + 2*f3[1] + f4[1])/6.0
    dz = (f1[2] + 2*f2[2] + 2*f3[2] + f4[2])/6.0
    return (dx, dy, dz)

def rkint(x=1.,y=1.,z=1.,t=1,dt = 0.01, f=lorenz):
    tnow = 0
    npoints = 1+ int(t/dt)
    data = np.zeros((npoints,3))
    ix = 0
    while tnow < t:
        dD = rkstep(x,y,z,tnow,dt)
        x = x + dD[0]
        y = y + dD[1]
        z = z + dD[2]
        data[ix] = (x,y,z)
        ix+=1
        if ix%1000 == 0: print(ix)
        tnow = tnow + dt
    return data

 def plotit(ldata):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(ldata[:,0], ldata[:,1],ldata[:,2], lw=0.5)
    plt.show()

from matplotlib.collections import LineCollection

def cplotit(ldata, t):
    '''With color as time'''
    fig = plt.figure()
    tvec = np.linspace(0,t,ldata.shape[0])
    #segments = np.concatenate(([ldata[:,0], ldata[:,1], ldata[:,2]]),axis=0)
    #lc = Line3DCollection(segments, cmap=plt.get_cmap('copper'), norm=plt.Normalize(0,t))
    points = np.array([ldata[:,0], ldata[:,1], ldata[:,2]]).transpose().reshape(-1,1,3)
    print(points.shape)
    # set up a list of segments
    segs = np.concatenate([points[:-1],points[1:]],axis=1)
    print(segs.shape)  # Out: ( len(x)-1, 2, 2 )
                  # see what we've done here -- we've mapped our (x,y)
                  # points to an array of segment start/end coordinates.
                  # segs[i,0,:] == segs[i-1,1,:]
    lc = Line3DCollection(segs, cmap=plt.get_cmap('jet'))

    lc.set_array(tvec)
    pdb.set_trace()
    ax = fig.gca(projection = '3d')
    #ax.add_collection3d(lc)
    ax.add_collection3d(lc)
    #ax = fig.gca(projection='3d')
    #ax.plot(ldata[:,0], ldata[:,1],ldata[:,2], lw=0.5)
    plt.xlim(ldata[:,0].min(), ldata[:,0].max())
    plt.ylim(ldata[:,1].min(), ldata[:,1].max())
    ax.set_zlim(ldata[:,2].min(), ldata[:,2].max())
    
    plt.show()

def demoplot():
    x = np.linspace(0,1,10)
    y = np.random.random((10,))
    z = np.linspace(0,1,10)
    t = np.linspace(0,1,10)

    # generate a list of (x,y,z) points
    points = np.array([x,y,z]).transpose().reshape(-1,1,3)
    print(points.shape)  # Out: (len(x),1,2)

    # set up a list of segments
    segs = np.concatenate([points[:-1],points[1:]],axis=1)
    print(segs.shape)  # Out: ( len(x)-1, 2, 2 )
                  # see what we've done here -- we've mapped our (x,y)
                  # points to an array of segment start/end coordinates.
                  # segs[i,0,:] == segs[i-1,1,:]

    # make the collection of segments
    lc = Line3DCollection(segs, cmap=plt.get_cmap('jet'))
    lc.set_array(t) # color the segments by our parameter
    pdb.set_trace()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.add_collection3d(lc)
    plt.show()



if __name__ == '__main__':
    tmax = 500
    ldata = rkint(1.,1.,1.,tmax)
    #demoplot()
    cplotit(ldata,tmax)
    plotit(ldata)
    pdb.set_trace()



    