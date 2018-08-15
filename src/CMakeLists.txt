cmake_minimum_required(VERSION 2.8.12)
project( iri90 Fortran )

add_compile_options(-mtune=native)

add_executable(testiri90 iridreg.for iritec.for igrf.for cira.for irifun.for iriflip.for irisub.for iritest.for)
