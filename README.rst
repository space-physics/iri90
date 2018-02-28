.. image:: https://travis-ci.org/scivision/pyiri90.svg?branch=master
    :target: https://travis-ci.org/scivision/pyiri90
   
.. image:: https://coveralls.io/repos/github/scivision/pyiri90/badge.svg?branch=master
    :target: https://coveralls.io/github/scivision/pyiri90?branch=master


=======
PyIRI90
=======

IRI90-international reference ionosphere in Python

    IRI-90 provides **monthly mean values** for magnetically quiet
conditions at non-auroral latitudes in the **altitude range 50km to 2000km**.

However, IRI90 is often used as an initialization for conditions at auroral latitudes, understanding the caveats.

.. image:: .github/demoiri.png
    :alt: example IRI output

Install
=======
::

    pip install pyiri90
    
or for the latest development version::

    git clone https://github.com/scivision/pyiri90
    cd pyiri90
    python -m pip install -e .


Usage
=====
PyIRI90 is as small and clean as possible to enable your custom IRI90 applications.

Altitude profile 
----------------
density and temperature::

	python AltitudeProfile.py


Notes
=====
Optional: If you want to work with just the original Fortran code::

    cd bin
    cmake ../fortran


References
----------
`Fortran Code <http://download.hao.ucar.edu/pub/stans/iri/iri90.f>`_
