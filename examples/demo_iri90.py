#!/usr/bin/env python3
from dateutil.parser import parse
from numpy import arange
#
from pyiri90.runiri90 import runiri

if __name__ == '__main__':
    altkm=arange(100,1000,5)
    dtime = parse('2013-04-14T08:54:00')
    outf,oarr= runiri(dtime,altkm,70,0,100,100,ap=4)