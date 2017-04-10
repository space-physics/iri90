#!/usr/bin/env python
from dateutil.parser import parse
import numpy as np
from matplotlib.pyplot import show
import seaborn as sns
#
from pyiri90 import runiri
from pyiri90.plots import plotiono

f0 = 3.5e6 # radar frequency [Hz]
B0 = 60e-6 # Geomagnetic field strength [Tesla] #TODO verify at altitude
theta = 0.01 # radians off parallel from B

fs = np.arange(1e6,8e6,0.05e6) # [Hz] radar frequency sweep

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('--alt',help='START STOP STEP altitude [km]',type=float,nargs=3,default=(85,500,1.))
    p.add_argument('-t','--time',help='datetime of simulation',default='2012-07-21T12')
    p.add_argument('-c','--latlon',help='geodetic coordinates of simulation',default=(65,-147.5),type=float)
    p.add_argument('--f107',type=float,default=200.)
    p.add_argument('--f107a',type=float,default=200.)
    p.add_argument('--ap',type=int,default=4)
    p = p.parse_args()

    altkm = np.arange(p.alt[0], p.alt[1], p.alt[2])
    dtime = parse(p.time)
#%%
    iono = runiri(dtime,altkm,p.latlon,p.f107, p.f107a, ap=p.ap)

    plotiono(iono,dtime,p.latlon,p.f107,p.f107a,p.ap)
    show()
