cmake_minimum_required(VERSION 3.14...3.21)

project(iri90 LANGUAGES Fortran)

if(CMAKE_Fortran_COMPILER_ID STREQUAL GNU)
  add_compile_options(-std=legacy)
endif()

add_subdirectory(src)

# testiri90 is an interactive program, not for CI
add_executable(testiri90 src/iritest.for)
target_link_libraries(testiri90 PRIVATE iri90)

add_executable(iri90_driver src/iri90.f src/iri90_driver.f90)
