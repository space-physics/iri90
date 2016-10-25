#!/usr/bin/env python
from warnings import warn
from dateutil.parser import parse
from numpy import arange,pi,zeros,sqrt,sin,cos,isfinite
import matplotlib
from matplotlib.pyplot import show,gcf
import seaborn as sns
#
from pyiri90 import runiri
from pyiri90.plots import summary

e = 1.6021766208e-19 # electron charge, coulomb
me = 9.10938356e-31 # electron mass, kg
eps0 = 8.85418782e-12 # permittivity of free space m^-3 kg^-1 s^4 A^2
f0 = 1e6 # radar frequency, Hz
B0 = 60e-6 # Geomagnetic field strength [Tesla] #TODO verify at altitude
theta = 0.01 # radians off parallal from B

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('--alt',help='START STOP STEP altitude [km]',type=float,nargs=3,default=(85,500,1.))
    p.add_argument('-t','--time',help='datetime of simulation',default='2012-12-21T00:00:00Z')
    p.add_argument('-c','--latlon',help='geodetic coordinates of simulation',default=(40,-80),type=float)
    p.add_argument('--f107',type=float,default=100.)
    p.add_argument('--f107a',type=float,default=100.)
    p.add_argument('--ap',type=int,default=4)
    p = p.parse_args()

    altkm = arange(p.alt[0],p.alt[1],p.alt[2])
    dtime = parse(p.time)

    iono = runiri(dtime,altkm,p.latlon,p.f107,p.f107a,ap=p.ap)
    Ne = iono['ne'].values.astype(float)
#%% Appleton-Hartree dispersion formula
    """
    Assumptions:
    aligned with geomagnetic field B
    cold, collisionless plasma
    """
    w0 = 2*pi*f0
    wp = sqrt(Ne*e**2/(eps0*me)) # electron plasma frequency [rad/sec]
    assert (w0<wp).any()

    assert isfinite(wp).all() # else whole calculation breaks down due to low altitude nan
    wH = B0*e/me               # electron gyrofrequency [rad/sec]
    X = wp**2/w0
    Y = wH/w0

    print('electron gyrofreq {} rad/sec'.format(wH))
#    print(wp)
#    print('X {}  Y {}'.format(X,Y))
    print(Y)
    print(X[:10])
    nr2 = 1-( X / (1-Y*cos(theta)))
    #nr2 = 1-( X / (1 - 0.5*Y**2*sin(theta)**2/(1-X) + Y*cos(theta)))

    print(nr2[:10])
    nr = sqrt(nr2)
    #nr  = sqrt(1 - X / (1 - 0.5*Y**2*sin(theta)**2/(1-X) - Y*cos(theta)))
    print(nr[:10])
    R = zeros(nr.size)
    for i in range(nr.size-1):
        R[i] = (nr[i]-nr[i+1])**2 / (nr[i]+nr[i+1])**2
    #print(R)
#%% plots
    summary(iono,R,p.latlon,dtime)

    show()

    if matplotlib.get_backend().lower() == 'agg':
        gcf().savefig('summary.svg',bbox_inches='tight')