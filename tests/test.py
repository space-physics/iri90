#!/usr/bin/env python
import numpy as np
from datetime import datetime
from pyiri90 import runiri,plasmaprop

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
#%%
    wp,wH,reflectionheight = plasmaprop(iono,f0,B0)

    np.testing.assert_almost_equal(wH,10552920.141612744)
    np.testing.assert_almost_equal(wp[43],74761613.912995234)
    np.testing.assert_almost_equal(reflectionheight,100.)

if __name__ == '__main__':
    np.testing.run_module_suite()