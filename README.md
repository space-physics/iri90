[![Build Status](https://travis-ci.org/scivision/iri90.svg?branch=master)](https://travis-ci.org/scivision/iri90)
[![Coverage Status](https://coveralls.io/repos/github/scivision/iri90/badge.svg?branch=master)](https://coveralls.io/github/scivision/iri90?branch=master)
[![Build status](https://ci.appveyor.com/api/projects/status/4h8pm345hscdpyf7?svg=true)](https://ci.appveyor.com/project/scivision/iri90)
[![PyPi version](https://img.shields.io/pypi/pyversions/iri90.svg)](https://pypi.python.org/pypi/iri90)
[![PyPi Download stats](http://pepy.tech/badge/iri90)](http://pepy.tech/project/iri90)


# IRI90: International reference ionosphere in Python

> IRI-90 provides **monthly mean values** for magnetically quiet
> conditions at non-auroral latitudes in the **altitude range 50km to
> 2000km**.

However, IRI90 is often used as an initialization for conditions at
auroral latitudes, understanding the caveats.

![example IRI output](.github/demoiri.png)

## Install

A Fortran compiler such as `gfortran` is needed.
We use `f2py` (part of `numpy`) to seamlessly use Fortran libraries from Python.
If you don't have one, here is how to install Gfortran:

* Linux: `apt install gfortran`
* Mac: `brew install gcc`
* [Windows](https://www.scivision.dev/windows-gcc-gfortran-cmake-make-install/)

```sh
pip install iri90
```
or for the latest development version:

```sh
python -m pip install -e .
```

### Windows
If you get ImportError on Windows for the Fortran module, try:
```posh
del *.pyd
python setup.py build_ext --inplace --compiler=mingw32
```

## Usage

This IRI90 Python module is as small and clean as possible to enable your custom IRI90 applications.

```python
import iri90

iono = iri90.runiri(dtime, altkm, latlon, f107, f107s, ap=p.ap)
```

`iono` is an xarray.DataArray indexable by species, altitude, etc. and includes metadata.

### Altitude profile

density and temperature:
```sh
python AltitudeProfile.py
```

## Notes

Optional: If you want to work with just the original Fortran code:
```sh
cd bin
cmake ../src
cmake --build .
```

### References

[Fortran Code](http://download.hao.ucar.edu/pub/stans/iri/iri90.f)
