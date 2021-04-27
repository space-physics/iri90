"""
IRI-90 international reference ionosphere in Python
"""
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import xarray
from typing import Sequence

#
import iri90fort

rdir = Path(__file__).parent
Ts = ["Tn", "Ti", "Te"]
simout = ["ne", "Tn", "Ti", "Te", "nO+", "nH+", "nHe+", "nO2+", "nNO+"]


def datetimerange(start: datetime, end: datetime, step: timedelta) -> list:
    """like range() for datetime!"""
    assert isinstance(start, datetime)
    assert isinstance(end, datetime)
    assert isinstance(step, timedelta)

    return [start + i * step for i in range((end - start) // step)]


def runiri(
    time: datetime, altkm: np.ndarray, glatlon: tuple, f107: float, f107a: float, ap: int
) -> xarray.DataArray:
    def _collect_output() -> xarray.DataArray:
        """collect IRI90 output into xarray.DataArray with metadata"""
        iono = xarray.DataArray(
            outf[:9, :].T,
            coords={"alt_km": altkm, "sim": simout},
            dims=["alt_km", "sim"],
            attrs={
                "f107": f107,
                "f107a": f107a,
                "ap": ap,
                "glatlon": glatlon,
                "time": time,
            },
        )

        #    i=(iono['Ti']<iono['Tn']).values
        #    iono.ix[i,'Ti'] = iono.ix[i,'Tn']

        #    i=(iono['Te']<iono['Tn']).values
        #    iono.ix[i,'Te'] = iono.ix[i,'Tn']

        # %%   iri90 outputs percentage of Ne
        iono.loc[:, ["nO+", "nH+", "nHe+", "nO2+", "nNO+"]] *= iono.loc[:, "ne"] / 100.0
        # %% These two parameters only output if JF(6)=False, otherwise bogus values
        # iono['nClusterIons'] = iono['ne'] * outf[9,:]/100.
        # iono['nN+'] = iono['ne'] * outf[10,:]/100.
        # %% negative indicates undefined
        for c in iono.sim:
            iono.loc[iono.loc[:, c] <= 0.0, c] = np.nan

        return iono

    glat, glon = glatlon
    jmag = 0  # coordinates are: 0:geographic 1: magnetic

    JF = np.array((1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1), bool)  # Solomon 1993 version of IRI
    # JF = (1,1,1) + (0,0,0) +(1,)*14 + (0,1,0,1,1,1,1,0,0,0,1,1,0,1,0,1,1,1) #for 2013 version of IRI

    monthday = (
        time.month * 100 + time.day
    )  # yep, that's how the IRI code wants it, NOT as character.
    # + 25 hours for UTC time
    hourfrac = (time.hour + 25) + time.minute / 60 + time.second / 3600
    datadir = str(rdir / "data") + "/"
    # %% call IRI
    outf, oarr = iri90fort.iri90(
        JF,
        jmag,
        glat,
        glon % 360.0,
        -f107,
        monthday,  # integer
        hourfrac,
        altkm,
        datadir,
    )

    iono = _collect_output()

    return iono


def timeprofile(
    tlim: Sequence[datetime],
    dt: timedelta,
    altkm: np.ndarray,
    glatlon: tuple,
    f107: float,
    f107a: float,
    ap: int,
) -> xarray.DataArray:
    """compute IRI90 at a single altiude, over time range"""

    T = datetimerange(tlim[0], tlim[1], dt)

    iono = xarray.DataArray(
        np.empty((len(T), altkm.size, 9)),
        coords={"time": T, "alt_km": altkm, "sim": simout},
        dims=["time", "alt_km", "sim"],
        attrs={"f107": f107, "f107a": f107a, "ap": ap, "glatlon": glatlon},
    )

    for t in T:
        iono.loc[t, ...] = runiri(t, altkm, glatlon, f107, f107a, ap)

    return iono
