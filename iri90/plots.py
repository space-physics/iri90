from matplotlib.pyplot import figure
import xarray
import numpy as np
from datetime import datetime
from typing import Sequence, List

try:
    import ephem
except ImportError:
    ephem = None
#
Ts = ["Tn", "Ti", "Te"]


def plotalt(iono: xarray.DataArray, species: Sequence[str] = None):
    """
    plots IRI90 altitude profile

    inputs:
    -------
    iono: DataArray containing metadata for sim
    species: optional tuple specifying which species to plot (default is to plot all species)
    """
    assert isinstance(iono, xarray.DataArray)

    species = _pickspecies(iono.sim, species)

    fg = figure(figsize=(15, 12))
    axs = fg.subplots(1, 2, sharey=True)
    # %% densities
    ax = axs[0]
    for p in species:
        if p in Ts:
            continue
        ax.semilogx(iono.loc[:, p], iono.alt_km, label=p)

    ax.set_xlabel("density [m$^{-3}$]")
    ax.set_ylabel("altitude [km]")
    ax.set_xlim(1e6, None)
    ax.legend()
    ax.grid(True)
    # %% temperature
    ax = axs[1]
    for p in Ts:
        ax.plot(iono.loc[:, p], iono.alt_km, label=p)

    ax.set_xlabel("Temperature [K]")
    ax.legend()
    ax.grid(True)

    ia = iono.attrs
    fg.suptitle(
        f"IRI90 {ia['glatlon']} {ia['time']}\n f10.7={ia['f107']} f107avg={ia['f107a']} Ap={ia['ap']}"
    )


def plottime(iono: xarray.DataArray, species: Sequence[str] = None):
    """
    plots IRI90 time profile

    inputs:
    -------
    iono: DataArray containing metadata for sim
    species: optional tuple specifying which species to plot (default is to plot all species)
    """
    assert isinstance(iono, xarray.DataArray)

    species = _pickspecies(iono.sim, species)

    fg = figure(figsize=(15, 8))
    ax = fg.gca()

    for p in species:
        if p in Ts:
            continue
        for alt in iono.alt_km:
            ax.plot(
                iono.time,
                iono.loc[:, alt, p],
                marker="*",
                label=f"{p}, {alt.item()} km",
            )

    _sunfid(ax, iono)

    ax.set_ylabel("density [m$^{-3}$]")
    ax.set_xlabel("time [UTC]")
    ax.set_title(
        f'{np.datetime_as_string(iono.time[0])[:-13]} to {np.datetime_as_string(iono.time[-1])[:-13]}\n {iono.attrs["glatlon"]}'
    )
    ax.set_yscale("log")
    ax.legend()
    ax.grid(True)


def _pickspecies(sim: xarray.DataArray, species: Sequence[str] = None) -> List[str]:
    if not species:
        specie = [p.item() for p in sim]
    elif isinstance(species, str):
        specie = [species]
    elif isinstance(species, (list, tuple, np.ndarray)):
        specie = species  # type: ignore

    return specie


def _sunfid(ax, iono: xarray.DataArray):
    """plot sunrise, sunset fiducials
    ephem uses UTC internally: http://rhodesmill.org/pyephem/date.html#time-zones

    matplotlib color names: https://matplotlib.org/examples/color/named_colors.html
    """

    if ephem is None:
        return

    dt = iono.time[0].dt
    t0 = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)

    o = ephem.Observer()
    o.lat = str(iono.attrs["glatlon"][0])
    o.lon = str(iono.attrs["glatlon"][1])
    o.date = t0

    sun = ephem.Sun()
    sunrise = o.next_rising(sun).datetime()
    sunset = o.next_setting(sun).datetime()

    ax.axvline(sunrise, color="gold", linestyle="--", linewidth=2, label="sunrise")
    ax.axvline(sunset, color="red", linestyle="--", linewidth=2, label="sunset")
