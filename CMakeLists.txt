cmake_minimum_required(VERSION 3.1)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Debug or Release")
endif()
project(iri90 Fortran)

if(CMAKE_Fortran_COMPILER_ID STREQUAL GNU)
  set(FFLAGS -std=legacy)
endif()

add_subdirectory(src)

# testiri90 is an interactive program, not for CI
add_executable(testiri90 src/iritest.for)
target_link_libraries(testiri90 iri90)

add_executable(iri90_driver src/iri90.f src/iri90_driver.f90)
