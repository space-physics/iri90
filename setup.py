#!/usr/bin/env python
import setuptools  # noqa: F401
from numpy.distutils.core import setup, Extension
from glob import glob
from os.path import join
from pathlib import Path
import os


if os.name == 'nt':
    sfn = Path(__file__).parent / 'setup.cfg'
    stxt = sfn.read_text()
    if '[build_ext]' not in stxt:
        with sfn.open('a') as f:
            f.write("[build_ext]\ncompiler = mingw32")

# %% fortran data files
iridata = glob(join('data', '*.asc'))

ext = [Extension(name='iri90fort',
                 sources=['src/iri90.f'],
                 extra_f77_compile_args=['-w'])]
# %% install
setup(ext_modules=ext,
      package_data={'pyiri90': ['data/*.asc']})
