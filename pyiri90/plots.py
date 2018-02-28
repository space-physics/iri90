from matplotlib.pyplot import figure
from xarray import DataArray
from datetime import datetime
#
Ts = ['Tn','Ti','Te']

def plotiono(iono:DataArray, dtime:datetime, latlon:tuple, f107:float, f107a:float, ap:float):
    assert isinstance(iono, DataArray)

    fg = figure(figsize=(15,12))
    axs = fg.subplots(1,2, sharey=True)
# %% densities
    ax = axs[0]
    for p in iono.sim:
        if p in Ts:
            continue
        ax.semilogx(iono.loc[:,p], iono.alt_km, label=p.values)

    ax.set_xlabel('density [m^-3]')
    ax.set_ylabel('altitude [km]')
    ax.set_xlim(1e6,None)
    ax.legend()
    ax.grid(True)
# %% temperature
    ax = axs[1]
    for p in Ts:
        ax.plot(iono.loc[:,p], iono.alt_km, label=p)


    ax.set_xlabel('Temperature [K]')
    ax.legend()
    ax.grid(True)

    fg.suptitle(f"IRI90 {latlon} {dtime}\n f10.7={f107} f107avg={f107a} Ap={ap}")

