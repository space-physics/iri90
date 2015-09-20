#!/usr/bin/env python3
import setuptools #enables develop
from numpy.distutils.core import setup,Extension
from glob import glob
from os.path import join

#%% fortran data files
iridata = glob(join('data','*.asc'))
#%%
with open('README.rst','r') as f:
    long_description = f.read()
#%% install
setup(name='pyiri90',
      version='0.1',
	   description='Python wrapper for IRI-90 ionosphere model',
	   long_description=long_description,
	   author='Michael Hirsch',
	   url='https://github.com/scienceopen/pyiri90',
	   install_requires=['msise00',
                     'numpy','six','pytz','pandas'],
    packages=['pyiri90'],
    dependency_links = ['https://github.com/scienceopen/msise00/tarball/master#egg=msise00'
                            ],
    ext_modules=[Extension(name='iri90',
                    sources=['fortran/iri90.f'],
                    f2py_options=['--quiet'])],
   data_files=[('pyiri90/data',iridata)]
	  )
