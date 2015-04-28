#!/usr/bin/env python3
"""
Demo of using IRI reference ionosphere in Python
michael Hirsch
MIT license
"""
from numpy import array,arange
from dateutil.parser import parse
from pandas import DataFrame

import iri90
import sys
sys.path.append('../msise-00')
from demo_msis import rungtd1d

def demoiri(dtime,glat=65,glon=-148,f107=100,f107a=100,ap=4):
   jmag=0 #0:geographic 1: magnetic
   altkm=arange(100,1000,5)
   JF = array((1,1,1,1,0,1,1,1,1,1,1,0)).astype(bool) #Solomon 1993 version of IRI
    #JF = (1,1,1) + (0,0,0) +(1,)*14 + (0,1,0,1,1,1,1,0,0,0,1,1,0,1,0,1,1,1) #for 2013 version of IRI
#%%
   dens,Tn = rungtd1d(dtime,altkm,glat,glon,f107a,f107,ap)


#%%
   outf,oarr = iri90.iri90(JF,jmag,glat,glon % 360., -f107,
                       dtime.strftime('%m%d'),
                       dtime.hour+dtime.minute/60+dtime.second/3600,
                       altkm,'data/')

   iono = DataFrame(index=altkm,
                     columns=['ne','Tn','Ti','Te','nO+','nH+','nHE+','nO2+','nNO+',
                              'nClusterIons','nN+'])
   iono['ne'] = outf[0,:]/1e6
   iono['Tn'] = Tn['heretemp']
   iono['Ti'] = outf[2,:]; i=iono['Ti']<iono['Tn'].values; iono.ix[i,'Ti'] = iono.ix[i,'Tn']
   iono['Te'] = outf[3,:]; i=iono['Te']<iono['Tn'].values; iono.ix[i,'Te'] = iono.ix[i,'Tn']
   iono['nO+']= iono['ne'] * outf[4,:]/100
   iono['nO2+']= iono['ne'] * outf[7,:]/100
   iono['nNO+']= iono['ne'] * outf[8,:]/100
   return iono,oarr

if __name__ == '__main__':
    dtime = parse('2013-04-14T08:54:00')
    outf,oarr= demoiri(dtime)