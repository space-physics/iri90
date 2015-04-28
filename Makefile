# USAGE: 
# make -s FC=<compiler>
# EXAMPLE:
# make -s FC=gfortran 
#

# use gfortran by default
ifeq ($(strip $(fc)),)
FC=gfortran
endif

FFLAGS = -O3 -I $(INCLUDE) -L $(LIBDIR) -fno-align-commons 

.SUFFIXES: .o .F .F90 .f90 .f .mod

%.o: %.for
	$(FC) $(FFLAGS) -c  -o $@ $<

SOURCES =  iridreg.for iritec.for igrf.for cira.for irifun.for iriflip.for irisub.for iritest.for 

OBJS := $(addsuffix .o, $(basename $(SOURCES)))
EXEC = iritest

$(EXEC): $(OBJS)
	$(FC) -o $@ $(OBJS) $(LIBS) $(LDFLAGS)

INCLUDE = /usr/include
LIBDIR = /usr/lib

clean:
	rm -f *.o *.mod $(EXEC)

