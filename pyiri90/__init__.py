"""
IRI-90 international reference ionosphere in Python
"""
from pathlib import Path
import numpy as np
from xarray import DataArray
#
import iri90 #fortran

rdir = Path(__file__).parent

def runiri(dt,z,glatlon,f107,f107a,ap):
    glat,glon = glatlon
    jmag=0 # coordinates are: 0:geographic 1: magnetic

    JF = np.array((1,1,1,1,0,1,1,1,1,1,1,0),bool) #Solomon 1993 version of IRI
    #JF = (1,1,1) + (0,0,0) +(1,)*14 + (0,1,0,1,1,1,1,0,0,0,1,1,0,1,0,1,1,1) #for 2013 version of IRI

#%% call IRI
    outf,oarr = iri90.iri90(JF,jmag,glat,glon % 360., -f107,
                       dt.strftime('%m%d'),
                       dt.hour+dt.minute//60+dt.second//3600,
                       z,str(rdir/'data')+'/')
#%% arrange output
    iono = DataArray(np.empty((z.size,9)),
                     coords={'alt_km':z,
                             'sim':['ne','Tn','Ti','Te','nO+','nH+','nHe+','nO2+','nNO+']},
                     dims=['alt_km','sim'])
    #                          'nClusterIons','nN+'])
    iono.loc[:,'ne'] = outf[0,:]  # ELECTRON DENSITY/M-3
    iono.loc[:,'Tn'] = outf[1,:]  # NEUTRAL TEMPERATURE/K

    iono.loc[:,'Ti'] = outf[2,:]  # ION TEMPERATURE/K
#    i=(iono['Ti']<iono['Tn']).values
#    iono.ix[i,'Ti'] = iono.ix[i,'Tn']

    iono.loc[:,'Te'] = outf[3,:]  # ELECTRON TEMPERATURE/K
#    i=(iono['Te']<iono['Tn']).values
#    iono.ix[i,'Te'] = iono.ix[i,'Tn']

#%%   iri90 outputs percentage of Ne
    iono.loc[:,'nO+'] = iono.loc[:,'ne'] * outf[4,:]/100. #O+ ion density / M-3
    iono.loc[:,'nH+'] = iono.loc[:,'ne'] * outf[5,:]/100. #H+ ion density / M-3
    iono.loc[:,'nHe+']= iono.loc[:,'ne'] * outf[6,:]/100. #He+ ion density / M-3
    iono.loc[:,'nO2+']= iono.loc[:,'ne'] * outf[7,:]/100. #O2+ "" "" ""
    iono.loc[:,'nNO+']= iono.loc[:,'ne'] * outf[8,:]/100. #NO+ "" "" ""

#%% These two parameters only output if JF(6)=False, otherwise bogus values
    #iono['nClusterIons'] = iono['ne'] * outf[9,:]/100.
    #iono['nN+'] = iono['ne'] * outf[10,:]/100.

    iono.loc[outf[1,:]<0,'Tn'] = np.nan
    iono.loc[outf[2,:]<0,'Ti'] = np.nan
    iono.loc[outf[3,:]<0,'Te'] = np.nan
    return iono
