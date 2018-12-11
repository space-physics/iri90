cmake_minimum_required(VERSION 3.1)
project(iri90 Fortran)

add_compile_options(-mtune=native -g -O0)


add_library(iri90 iridreg.for iritec.for igrf.for cira.for irifun.for iriflip.for irisub.for)

add_executable(testiri90 iritest.for)
target_link_libraries(testiri90 iri90)

add_executable(iri90_driver iri90.f iri90_driver.F90)
target_compile_definitions(iri90_driver PRIVATE 
  BIN_DIR='${CMAKE_CURRENT_BINARY_DIR}')
