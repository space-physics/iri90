"""
IRI-90 international reference ionosphere in Python
"""
from pathlib import Path
import numpy as np
from xarray import DataArray
#
import iri90 #fortran

rdir = Path(__file__).parent
Ts = ['Tn','Ti','Te']

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
    iono = DataArray(outf[:9,:].T,
                     coords={'alt_km':z,
                             'sim':['ne','Tn','Ti','Te','nO+','nH+','nHe+','nO2+','nNO+']},
                     dims=['alt_km','sim'])

#    i=(iono['Ti']<iono['Tn']).values
#    iono.ix[i,'Ti'] = iono.ix[i,'Tn']

#    i=(iono['Te']<iono['Tn']).values
#    iono.ix[i,'Te'] = iono.ix[i,'Tn']

#%%   iri90 outputs percentage of Ne
    iono.loc[:,['nO+','nH+','nHe+','nO2+','nNO+']] *= iono.loc[:,'ne']/100.
#%% These two parameters only output if JF(6)=False, otherwise bogus values
    #iono['nClusterIons'] = iono['ne'] * outf[9,:]/100.
    #iono['nN+'] = iono['ne'] * outf[10,:]/100.
# %% negative indicates undefined
    for c in iono.sim:

        iono.loc[iono.loc[:,c]<= 0., c] = np.nan

    return iono
