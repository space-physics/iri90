#!/usr/bin/env python
install_requires=['numpy','xarray']
tests_require=['nose','coveralls']
# %%

from setuptools import find_packages
from numpy.distutils.core import setup,Extension
from glob import glob
from os.path import join



#%% fortran data files
iridata = glob(join('data','*.asc'))
#%% install
setup(name='pyiri90',
      packages=find_packages(),
      version = '1.0.1',
      author='Michael Hirsch, Ph.D.',
      ext_modules=[Extension(name='iri90',
                    sources=['fortran/iri90.f'],
                    f2py_options=['--quiet'])],
      package_data={'pyiri90':['data/*.asc']},
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'tests':tests_require,
                      'plot':['matplotlib'],},
      python_requires='>=2.7',
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 5 - Production/Stable',
      'License :: OSI Approved :: MIT License',
      'Topic :: Scientific/Engineering :: Atmospheric Science',
      'Programming Language :: Python :: 3',
      ],
	  )
