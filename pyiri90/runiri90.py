#!/usr/bin/env python3
"""
Demo of using IRI reference ionosphere in Python
michael Hirsch
MIT license
"""
from __future__ import division,absolute_import
import logging
from numpy import array
from pandas import DataFrame
from os import chdir,getcwd
#
import pyiri90
import iri90 #fortran
from msise00.runmsis import rungtd1d


def runiri(dtime,altkm,glat,glon,f107,f107a,ap,mass=48):
    jmag=0 #0:geographic 1: magnetic
    JF = array((1,1,1,1,0,1,1,1,1,1,1,0)).astype(bool) #Solomon 1993 version of IRI
    #JF = (1,1,1) + (0,0,0) +(1,)*14 + (0,1,0,1,1,1,1,0,0,0,1,1,0,1,0,1,1,1) #for 2013 version of IRI
#%% call MSIS
    dens,Tn = rungtd1d(dtime,altkm,glat,glon,f107a,f107,ap,mass,(1,)*25)
#%% call IRI
    chdir(pyiri90.__path__[0])
    logging.debug(getcwd())
    outf,oarr = iri90.iri90(JF,jmag,glat,glon % 360., -f107,
                       dtime.strftime('%m%d'),
                       dtime.hour+dtime.minute//60+dtime.second//3600,
                       altkm,'data/')
#%% arrange output
    iono = DataFrame(index=altkm,
                     columns=['ne','Tn','Ti','Te','nO+','nH+','nHE+','nO2+','nNO+',
                              'nClusterIons','nN+'])
    iono['ne'] = outf[0,:]/1e6
    iono['Tn'] = Tn['heretemp']

    iono['Ti'] = outf[2,:]
    i=iono['Ti']<iono['Tn'].values
    iono.ix[i,'Ti'] = iono.ix[i,'Tn']

    iono['Te'] = outf[3,:]
    i=iono['Te']<iono['Tn'].values
    iono.ix[i,'Te'] = iono.ix[i,'Tn']

    iono['nO+']= iono['ne'] * outf[4,:]/100
    iono['nO2+']= iono['ne'] * outf[7,:]/100
    iono['nNO+']= iono['ne'] * outf[8,:]/100
    return iono,oarr