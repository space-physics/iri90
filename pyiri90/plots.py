from matplotlib.pyplot import figure
from xarray import DataArray
from numpy import zeros
#
from . import plasmaprop

def plotiono(iono:DataArray):
    assert isinstance(iono,DataArray)

    ax = figure().gca()
    for p in iono.sim:
        ax.plot()

def summary(iono:DataArray,reflectionheight,f0,latlon,dtime):
    assert isinstance(iono,DataArray)

    ax = figure().gca()
    ax.plot(iono.loc[:,'ne'],iono.alt_km,'b',label='$N_e$')

    if reflectionheight is not None:
        ax.axhline(reflectionheight,color='m',linestyle='--',label='reflection height')

    ax.legend()
    ax.set_ylabel('altitude [km]')
    ax.set_xlabel('Number Density')

    ax.autoscale(True,'y',True)
    ax.set_title(f'({latlon[0]}, {latlon[1]})  {dtime}  @ {f0/1e6:.1f} MHz',y=1.06)

def sweep(iono,fs,B0,latlon,dtime):
    hr = zeros(fs.size)
    for i,f in enumerate(fs):
        wp,wH,hr[i] = plasmaprop(iono,f,B0)

    ax = figure().gca()
    ax.plot(fs/1e6, hr)
    ax.set_xlabel('frequency [MHz]')
    ax.set_ylabel('altitude [km]')
    ax.set_title('Reflection Height: first order approx. $\omega_p = \omega$')

def plotR(R,zkm):
    ax = figure().gca()
    if R is not None:
        ax2 = ax.twiny()
        #ax2.plot(dNe,zkm,'r',label='$ \partial N_e/\partial z $')

        ax2.plot(R,zkm,'r',label='$\Gamma$')

        ax2.legend(loc='right')
