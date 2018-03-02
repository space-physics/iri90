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
      url='https://github.com/scivision/pyiri90',
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
      'Development Status :: 5 - Production/Stable',
      'Environment :: Console',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 3',
      'Topic :: Scientific/Engineering :: Atmospheric Science',
      ],
	  )
