"""
IRI-90 international reference ionosphere in Python
"""
from __future__ import division,absolute_import
import logging
from numpy import array
from pandas import DataFrame
#
import iri90 #fortran

def runiri(dt,z,glatlon,f107,f107a,ap):
    glat,glon = glatlon
    jmag=0 # coordinates are: 0:geographic 1: magnetic

    JF = array((1,1,1,1,0,1,1,1,1,1,1,0),bool) #Solomon 1993 version of IRI
    #JF = (1,1,1) + (0,0,0) +(1,)*14 + (0,1,0,1,1,1,1,0,0,0,1,1,0,1,0,1,1,1) #for 2013 version of IRI

#%% call IRI
    outf,oarr = iri90.iri90(JF,jmag,glat,glon % 360., -f107,
                       dt.strftime('%m%d'),
                       dt.hour+dt.minute//60+dt.second//3600,
                       z,'data/')
#%% arrange output
    iono = DataFrame(index=z,
                     columns=['ne','Tn','Ti','Te','nO+','nH+','nHe+','nO2+','nNO+',
                              'nClusterIons','nN+'])
    iono['ne'] = outf[0,:]  # ELECTRON DENSITY/M-3
    iono['Tn'] = outf[1,:]  # NEUTRAL TEMPERATURE/K

    iono['Ti'] = outf[2,:]  # ION TEMPERATURE/K
#    i=(iono['Ti']<iono['Tn']).values
#    iono.ix[i,'Ti'] = iono.ix[i,'Tn']

    iono['Te'] = outf[3,:]  # ELECTRON TEMPERATURE/K
#    i=(iono['Te']<iono['Tn']).values
#    iono.ix[i,'Te'] = iono.ix[i,'Tn']

#   iri90 outputs percentage of Ne
    iono['nO+'] = iono['ne'] * outf[4,:]/100. #O+ ion density / M-3
    iono['nH+'] = iono['ne'] * outf[5,:]/100. #H+ ion density / M-3
    iono['nHe+']= iono['ne'] * outf[6,:]/100. #He+ ion density / M-3
    iono['nO2+']= iono['ne'] * outf[7,:]/100. #O2+ "" "" ""
    iono['nNO+']= iono['ne'] * outf[8,:]/100. #NO+ "" "" ""
    iono['nClusterIons'] = iono['ne'] * outf[9,:]/100.
    iono['nN+'] = iono['ne'] * outf[10,:]/100.
    return iono
