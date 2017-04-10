from matplotlib.pyplot import subplots
from xarray import DataArray
#
Ts = ['Tn','Ti','Te']

def plotiono(iono:DataArray,dtime,latlon,f107,f107a,ap):
    assert isinstance(iono,DataArray)

    fg,axs = subplots(1,2,sharey=True)

    ax = axs[0]
    for p in iono.sim:
        if p in Ts:
            continue
        ax.semilogx(iono.loc[:,p],iono.alt_km,label=p.values)

    ax.set_xlabel('density [m^-3]')
    ax.set_xlim(1e6,None)
    ax.legend()
    ax.set_ylabel('altitude [km]')

    ax = axs[1]
    for p in Ts:
        ax.semilogx(iono.loc[:,p], iono.alt_km, label=p)


    ax.set_xlabel('Temperature [K]')

    ax.legend()

    fg.suptitle(f"IRI90 {latlon} {dtime} f10.7={f107} f107avg={f107a} Ap={ap}")

