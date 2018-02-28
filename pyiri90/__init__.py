"""
IRI-90 international reference ionosphere in Python
"""
from datetime import datetime,timedelta
from pathlib import Path
import numpy as np
import xarray
#
import iri90 #fortran

rdir = Path(__file__).parent
Ts = ['Tn','Ti','Te']


def datetimerange(start:datetime, end:datetime, step:timedelta) -> list:
    """like range() for datetime!"""
    assert isinstance(start, datetime)
    assert isinstance(end, datetime)
    assert isinstance(step, timedelta)

    return [start + i*step for i in range((end-start) // step)]


def runiri(t:datetime, altkm:float, glatlon:tuple, f107:float, f107a:float, ap:int) -> xarray.DataArray:

    def _collect_output() -> xarray.DataArray:
        """ collect IRI90 output into xarray.DataArray with metadata"""
        if isinstance(altkm,(list,tuple,np.ndarray)):  # altitude profile
            iono = xarray.DataArray(outf[:9,:].T,
                         coords={'alt_km':altkm,
                                 'sim':['ne','Tn','Ti','Te','nO+','nH+','nHe+','nO2+','nNO+']},
                         dims=['alt_km','sim'],
                         attrs={'f107':f107, 'f107a':f107a, 'ap':ap, 'glatlon':glatlon,'time':t})
        else:
            iono = xarray.DataArray(outf[:9,:].T,
                         coords={'time':t,
                                 'sim':['ne','Tn','Ti','Te','nO+','nH+','nHe+','nO2+','nNO+']},
                         dims=['alt_km','sim'],
                         attrs={'f107':f107, 'f107a':f107a, 'ap':ap, 'glatlon':glatlon,'alt_km':altkm,})

    #    i=(iono['Ti']<iono['Tn']).values
    #    iono.ix[i,'Ti'] = iono.ix[i,'Tn']

    #    i=(iono['Te']<iono['Tn']).values
    #    iono.ix[i,'Te'] = iono.ix[i,'Tn']

    # %%   iri90 outputs percentage of Ne
        iono.loc[:,['nO+','nH+','nHe+','nO2+','nNO+']] *= iono.loc[:,'ne']/100.
    # %% These two parameters only output if JF(6)=False, otherwise bogus values
        #iono['nClusterIons'] = iono['ne'] * outf[9,:]/100.
        #iono['nN+'] = iono['ne'] * outf[10,:]/100.
    # %% negative indicates undefined
        for c in iono.sim:
            iono.loc[iono.loc[:,c]<= 0., c] = np.nan

        return iono

    glat,glon = glatlon
    jmag=0 # coordinates are: 0:geographic 1: magnetic

    JF = np.array((1,1,1,1,0,1,1,1,1,1,1,0),bool) #Solomon 1993 version of IRI
    #JF = (1,1,1) + (0,0,0) +(1,)*14 + (0,1,0,1,1,1,1,0,0,0,1,1,0,1,0,1,1,1) #for 2013 version of IRI

    monthday = (t.strftime('%m%d'))
    hourfrac = t.hour + t.minute//60+ t.second//3600
    datadir = str(rdir/'data')+'/'
#%% call IRI
    outf,oarr = iri90.iri90(JF,jmag,
                            glat, glon % 360.,
                            -f107,
                            monthday,
                            hourfrac,
                            altkm,
                            datadir)

    iono = _collect_output()

    return iono




def timeprofile(tlim:tuple, dt:timedelta, altkm:float, glatlon:tuple, f107:float, f107a:float, ap:int):
    """compute IRI90 at a single altiude, over time range"""

    T = datetimerange(tlim[0], tlim[1], dt)

    for t in T:
        iono = runiri(t, altkm, glatlon, f107, f107a, ap)
