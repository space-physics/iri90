from matplotlib.pyplot import figure
import xarray
import numpy as np
#
Ts = ['Tn','Ti','Te']

def plotalt(iono:xarray.DataArray):
    assert isinstance(iono, xarray.DataArray)

    fg = figure(figsize=(15,12))
    axs = fg.subplots(1,2, sharey=True)
# %% densities
    ax = axs[0]
    for p in iono.sim:
        if p in Ts:
            continue
        ax.semilogx(iono.loc[:,p], iono.alt_km, label=p.item())

    ax.set_xlabel('density [m$^{-3}$]')
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


def plottime(iono:xarray.DataArray, species:tuple=None):
    """
    plots IRI90 time profile

    inputs:
    -------
    iono: DataArray containing metadata for sim
    species: optional tuple specifying which species to plot (default is to plot all species)
    """
    assert isinstance(iono, xarray.DataArray)

    if not species:
        species = [p.item() for p in iono.sim]
    elif isinstance(species,str):
        species = [species]
    else: # assuming it's an iterable
        pass

    fg = figure(figsize=(15,8))
    ax = fg.gca()

    for p in species:
        if p in Ts:
            continue
        for alt in iono.alt_km:
            ax.plot(iono.time, iono.loc[:,alt,p], marker='*',label=f'{p}, {alt.item()} km')

    ax.set_ylabel('density [m$^{-3}$]')
    ax.set_xlabel('time [UTC]')
    ax.set_title(f'{np.datetime_as_string(iono.time[0])[:-13]} to {np.datetime_as_string(iono.time[0])[:-13]}\n {iono.attrs["glatlon"]}')
    ax.legend()
    ax.grid(True)