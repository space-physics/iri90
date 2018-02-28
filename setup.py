#!/usr/bin/env python
install_requires=['numpy','xarray']
tests_require=['pytest','coveralls']
# %%
from setuptools import find_packages
from numpy.distutils.core import setup,Extension
from glob import glob
from os.path import join

#%% fortran data files
iridata = glob(join('data','*.asc'))

ext = [Extension(name='iri90',
                    sources=['fortran/iri90.f'],
                    f2py_options=['--quiet'],
                    extra_f77_compile_args=['-w'])]
#%% install
setup(name='pyiri90',
      packages=find_packages(),
      version = '1.1.0',
      author='Michael Hirsch, Ph.D.',
      description='IRI90 from Python, clean and flexible ionospheric model',
      long_description=open('README.rst').read(),
      ext_modules=ext,
      package_data={'pyiri90':['data/*.asc']},
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'tests':tests_require,
                      'plot':['matplotlib'],},
      python_requires='>=3.5',
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 5 - Production/Stable',
      'License :: OSI Approved :: MIT License',
      'Topic :: Scientific/Engineering :: Atmospheric Science',
      'Programming Language :: Python :: 3',
      ],
	  )
