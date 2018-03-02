#!/usr/bin/env python
import numpy as np
from datetime import datetime
from pyiri90 import runiri

def test_altitude():
    altkm = np.arange(90,500,5)
    dtime = datetime(2012,1,1,12)
    latlon = (30.,0.)
    f107 = f107a = 200.
    ap = 4.

    iono = runiri(dtime, altkm, latlon, f107, f107a, ap)

    I = iono.loc[235,:]
    It = [2.12232176e+11, 1.13743994e+03, 1.13743994e+03,
          1.94536694e+03, 1.99106658e+11, np.nan, np.nan, 1.76997920e+08,   1.29485240e+10]

    np.testing.assert_allclose(I, It)
    
if __name__ == '__main__':
    np.testing.run_module_suite()
