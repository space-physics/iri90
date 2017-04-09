"""
IRI-90 international reference ionosphere in Python
"""
from pathlib import Path
import os
import numpy as np
from xarray import DataArray
#
import iri90 #fortran

e = 1.6021766208e-19 # electron charge, coulomb
me = 9.10938356e-31 # electron mass, kg
eps0 = 8.85418782e-12 # permittivity of free space m^-3 kg^-1 s^4 A^2

root = Path(__file__).parents[1]

def runiri(dt,z,glatlon,f107,f107a,ap):
    glat,glon = glatlon
    jmag=0 # coordinates are: 0:geographic 1: magnetic

    JF = np.array((1,1,1,1,0,1,1,1,1,1,1,0),bool) #Solomon 1993 version of IRI
    #JF = (1,1,1) + (0,0,0) +(1,)*14 + (0,1,0,1,1,1,1,0,0,0,1,1,0,1,0,1,1,1) #for 2013 version of IRI

#%% call IRI
    cwd = os.getcwd()
    os.chdir(root)
    outf,oarr = iri90.iri90(JF,jmag,glat,glon % 360., -f107,
                       dt.strftime('%m%d'),
                       dt.hour+dt.minute//60+dt.second//3600,
                       z,'data/')
    os.chdir(cwd)
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
    return iono

def plasmaprop(iono,f,B0):
    Ne = iono.loc[:,'ne'].astype(float)
    w = 2*np.pi*f

    wp = np.sqrt(Ne*e**2/(eps0*me)) # electron plasma frequency [rad/sec]
    wH = B0*e/me               # electron gyrofrequency [rad/sec]


    if (w <= wp).any(): # else reflection doesn't occur, passes right through (radar freq > MUF)
        reflectionheight = iono.alt_km[abs(w-wp).argmin()]
    else:
        print(f'radar freq {f/1e6:.1f} MHz  >  max. plasma freq {wp.max()/(2*np.pi)/1e6:.1f} MHz: no reflection')
        reflectionheight = None

    return wp,wH,reflectionheight

def appleton(wp,w0,wH,theta):
    #%% Appleton-Hartree dispersion formula
    """
    Assumptions:
    aligned with geomagnetic field B
    cold, collisionless plasma

    first order approximation: reflection occurs where w0 = wp  (radar frequency = plasma frequency)
    """
    assert np.isfinite(wp).all() # else whole calculation breaks down due to low altitude nan
    X = wp**2/w0
    Y = wH/w0

    print(f'electron gyrofreq {wH} rad/sec')
    print(wp)
    print(f'X {X}  Y {Y}')
    print(Y)
    print(X[:10])
    n2 = 1-( X / (1-Y*np.cos(theta)))
#    nr2 = 1-( X / (1 - 0.5*Y**2*np.sin(theta)**2/(1-X) + Y*np.cos(theta)))
#
#    print(n2[:10])
    n = np.sqrt(n2)
#    nr= np.sqrt(1 - X / (1 - 0.5*Y**2*np.sin(theta)**2/(1-X) - Y*np.cos(theta)))
    print(n[:10])
    R = np.zeros(n.size)
    for i in range(n.size-1):
        R[i] = (n[i]-n[i+1])**2 / (n[i] + n[i+1])**2
    print(R)

    return R