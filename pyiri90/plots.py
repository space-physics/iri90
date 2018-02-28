from matplotlib.pyplot import figure
from xarray import DataArray
from datetime import datetime
#
Ts = ['Tn','Ti','Te']

def plotiono(iono:DataArray):
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

    ia = iono.attrs
    fg.suptitle(f"IRI90 {ia['glatlon']} {ia['time']}\n f10.7={ia['f107']} f107avg={ia['f107a']} Ap={ia['ap']}")

