project('iri90', 'fortran',
  default_options : ['default_library=static', 'buildtype=release'])

fc = meson.get_compiler('fortran')
if fc.get_id() == 'gcc'
  old = '-std=legacy'
endif

subdir('src')

# testiri90 is an interactive program, not for CI
testiri90_exe = executable('testiri90', 'src/iritest.for',
  link_with: iri90_lib)

iri90_driver_exe = executable('iri90_driver', 'src/iri90.f', 'src/iri90_driver.f90')
