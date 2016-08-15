#!/usr/bin/env python
import setuptools #enables develop
from numpy.distutils.core import setup,Extension
from glob import glob
from os.path import join

#%% fortran data files
iridata = glob(join('data','*.asc'))
#%% install
setup(name='pyiri90',
	   description='Python wrapper for IRI-90 ionosphere model',
	   author='Michael Hirsch',
	   url='https://github.com/scienceopen/pyiri90',
       packages=['pyiri90'],
       install_requires=['pathlib2'],
 ext_modules=[Extension(name='iri90',
                    sources=['fortran/iri90.f'],
                    f2py_options=['--quiet'])],
   data_files=[('pyiri90/data',iridata)]
	  )
