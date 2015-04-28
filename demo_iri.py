#!/usr/bin/env python3
"""
Demo of using IRI reference ionosphere in Python
michael Hirsch
MIT license
"""
from dateutil.parser import parse
from datetime import datetime
#import iri

def demoiri(dtime):
    jmag=0 #0:geographic 1: magnetic
    glat = 65
    glon = -148
    altmin = 80
    altmax =1000
    altstep = 10
    JF = (1,1,1) + (0,0,0) +(1,)*14 + (0,1,0,1,1,1,1,0,0,0,1,1,0,1,0,1,1,1)
    #%%
    outf = iri.iri_sub(JF,jmag,glat,glon % 360.,
                       dtime.year, dtime.strftime('%m%d'),
                       dtime.hour+dtime.minute/60+dtime.seconds/3600,
                       altmin,altmax,altstep)

if __name__ == '__main__':
    dtime = parse('2013-04-14T08:54:00')
    demoiri(dtime)