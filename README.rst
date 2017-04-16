.. image:: https://travis-ci.org/scivision/pyiri90.svg?branch=master
    :target: https://travis-ci.org/scivision/pyiri90
.. image:: https://coveralls.io/repos/github/scivision/pyiri90/badge.svg?branch=master
    :target: https://coveralls.io/github/scivision/pyiri90?branch=master


=============
iri90-python
=============

IRI90-international reference ionosphere in Python

"IRI-90 provides monthly mean values for magnetically quiet
conditions at non-auroral latitudes in the altitude range 50km to 2000km. "

.. image:: .github/demoiri.png
    :alt: example IRI output

Installation
============
::

    python setup.py develop


Example
=======
::

	python DemoIRI90.py


Reference
=========
Optional: If you want to work with just the original Fortran code::

    cd bin
    cmake ../fortran

TODO: fix paths to data for Python and Fortran


References
----------
`Fortran Code <http://download.hao.ucar.edu/pub/stans/iri/iri90.f>`_
