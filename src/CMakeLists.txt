add_library(iri90 iridreg.for iritec.for igrf.for cira.for irifun.for iriflip.for irisub.for)
target_compile_options(iri90 PRIVATE ${FFLAGS})