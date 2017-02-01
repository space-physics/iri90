#!/usr/bin/env python
import logging
from dateutil.parser import parse
from numpy import arange,pi,zeros,sqrt,cos,isfinite
import matplotlib
from matplotlib.pyplot import show,gcf
import seaborn as sns
#
from pyiri90 import runiri,plasmaprop
from pyiri90.plots import summary,sweep

f0 = 3.5e6 # radar frequency, Hz
B0 = 60e-6 # Geomagnetic field strength [Tesla] #TODO verify at altitude
theta = 0.01 # radians off parallal from B

fs = arange(1e6,8e6,0.05e6) # [hz] radar frequency sweep

def appleton(iono):
    #%% Appleton-Hartree dispersion formula
    """
    Assumptions:
    aligned with geomagnetic field B
    cold, collisionless plasma

    first order approximation: reflection occurs where w0 = wp  (radar frequency = plasma frequency)
    """
    wp,wH,reflectionheight = plasmaprop(iono,f0,B0)

#    assert isfinite(wp).all() # else whole calculation breaks down due to low altitude nan
#    X = wp**2/w0
#    Y = wH/w0

 #   print('electron gyrofreq {} rad/sec'.format(wH))
#    print(wp)
#    print('X {}  Y {}'.format(X,Y))
#    print(Y)
#    print(X[:10])
#    n2 = 1-( X / (1-Y*cos(theta)))
#    #nr2 = 1-( X / (1 - 0.5*Y**2*sin(theta)**2/(1-X) + Y*cos(theta)))
#
#    print(n2[:10])
#    n = sqrt(n2)
    #nr  = sqrt(1 - X / (1 - 0.5*Y**2*sin(theta)**2/(1-X) - Y*cos(theta)))
#    print(n[:10])
#    R = zeros(n.size)
#    for i in range(n.size-1):
#        R[i] = (n[i]-n[i+1])**2 / (n[i] + n[i+1])**2
    #print(R)
    R=None

    return R,reflectionheight

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('--alt',help='START STOP STEP altitude [km]',type=float,nargs=3,default=(85,500,1.))
    p.add_argument('-t','--time',help='datetime of simulation',default='2012-07-21T12:00:00Z')
    p.add_argument('-c','--latlon',help='geodetic coordinates of simulation',default=(30,0),type=float)
    p.add_argument('--f107',type=float,default=200.)
    p.add_argument('--f107a',type=float,default=200.)
    p.add_argument('--ap',type=int,default=4)
    p = p.parse_args()

    altkm = arange(p.alt[0],p.alt[1],p.alt[2])
    dtime = parse(p.time)

    iono = runiri(dtime,altkm,p.latlon,p.f107,p.f107a,ap=p.ap)
#%%
    R,reflectionheight = appleton(iono)
#%% plots
    summary(iono,R,reflectionheight,f0,p.latlon,dtime)

    sweep(iono,fs,B0,p.latlon,dtime)

    show()

    if matplotlib.get_backend().lower() == 'agg':
        gcf().savefig('summary.svg',bbox_inches='tight')