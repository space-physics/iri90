#!/usr/bin/env python
from dateutil.parser import parse
from numpy import arange
import matplotlib
from matplotlib.pyplot import show,gcf
import seaborn as sns
#
from pyiri90 import runiri
from pyiri90.plots import summary

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('--alt',help='START STOP STEP altitude [km]',type=float,nargs=3,default=(60,1000,5))
    p.add_argument('-t','--time',help='datetime of simulation',default='1999-12-21T00:00:00Z')
    p.add_argument('-c','--latlon',help='geodetic coordinates of simulation',default=(70,0),type=float)
    p.add_argument('--f107',type=float,default=100.)
    p.add_argument('--f107a',type=float,default=100.)
    p.add_argument('--ap',type=float,default=4)
    p = p.parse_args()

    altkm = arange(p.alt[0],p.alt[1],p.alt[2])
    dtime = parse(p.time)

    iono = runiri(dtime,altkm,p.latlon,p.f107,p.f107a,ap=p.ap)
#%% plots
    summary(iono,p.latlon,dtime)

    show()

    if matplotlib.get_backend().lower() == 'agg':
        gcf().savefig('summary.svg',bbox_inches='tight')