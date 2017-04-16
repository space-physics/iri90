#!/usr/bin/env python
import setuptools #enables develop
from numpy.distutils.core import setup,Extension
from glob import glob
from os.path import join

req = ['nose','numpy','xarray','matplotlib']

#%% fortran data files
iridata = glob(join('data','*.asc'))
#%% install
setup(name='pyiri90',
      packages=['pyiri90'],
      author='Michael Hirsch, Ph.D.',
      ext_modules=[Extension(name='iri90',
                    sources=['fortran/iri90.f'],
                    f2py_options=['--quiet'])],
     data_files=[('pyiri90/data',iridata)],
     install_requires=req,
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 5 - Production / Stable',
      'License :: OSI Approved :: MIT License',
      'Topic :: Scientific/Engineering :: Atmospheric Science',
      'Programming Language :: Python :: 3.6',
      ],
	  )
