#!/usr/bin/env python
req=['nose','numpy','xarray','matplotlib']
# %%
try:
    import conda.cli
    conda.cli.main('install',*req)
except Exception as e:
    import pip
    pip.main(['install'] + req)
# %%
import setuptools #enables develop
from numpy.distutils.core import setup,Extension
from glob import glob
from os.path import join



#%% fortran data files
iridata = glob(join('data','*.asc'))
#%% install
setup(name='pyiri90',
      packages=['pyiri90'],
      version = '1.0.1',
      author='Michael Hirsch, Ph.D.',
      ext_modules=[Extension(name='iri90',
                    sources=['fortran/iri90.f'],
                    f2py_options=['--quiet'])],
      package_data={'pyiri90':['data/*.asc']},
      install_requires=req,
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 5 - Production/Stable',
      'License :: OSI Approved :: MIT License',
      'Topic :: Scientific/Engineering :: Atmospheric Science',
      'Programming Language :: Python :: 3',
      ],
	  )
