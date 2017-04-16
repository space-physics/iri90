#!/usr/bin/env python
import numpy as np
from datetime import datetime
from pyiri90 import runiri

def test_iri90():
    altkm = np.arange(90,500,5)
    dtime = datetime(2012,1,1,12)
    latlon = (30.,0.)
    f107 = f107a = 200.
    ap = 4.

    f0 = 3.5e6 # [Hz]
    B0 = 60e-6 #[Tesla]

    iono = runiri(dtime, altkm, latlon, f107, f107a, ap)

    I = iono.loc[235,:]
    It = [212232142848.0, 1137.43994140625, 1137.43994140625, 1945.366943359375,
        199106625536.0,0,0,176997889.0, 12948521984.0]

    np.testing.assert_allclose(I, It)


if __name__ == '__main__':
    np.testing.run_module_suite()
