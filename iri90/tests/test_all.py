import numpy as np
from pytest import approx
from datetime import datetime

import iri90


def test_altitude():
    altkm = np.arange(90, 500, 5)
    dtime = datetime(2012, 1, 1, 12)
    latlon = (30.0, 0.0)
    f107 = f107a = 200.0
    ap = 4.0

    iono = iri90.runiri(dtime, altkm, latlon, f107, f107a, ap)

    Isim = iono.loc[235, :]
    It = [
        2.12232176e11,
        1.13743994e03,
        1.13743994e03,
        1.94536694e03,
        1.99106658e11,
        np.nan,
        np.nan,
        1.76997920e08,
        1.29485240e10,
    ]

    assert Isim.values == approx(It, nan_ok=True)
