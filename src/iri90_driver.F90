program basictest
use, intrinsic:: iso_fortran_env, only: stderr=>error_unit, stdout=>output_unit
implicit none

logical :: jf(12)
integer, parameter :: jmag = 0
integer :: iyyyy, mmdd, Nalt
real :: glat, glon, dhour
integer :: ymdhms(6)
real :: f107a

real :: oarr(30)
real, allocatable :: altkm(:), outf(:,:)
character(80) :: argv
integer :: i, argc

#ifndef BIN_DIR
#define BIN_DIR '.'
#endif
character(*), parameter :: datadir = BIN_DIR // '/../iri90/data/'


! --- per irisub.for docs
integer :: icalls, nmono, iyearo, idaynro
logical :: rzino, igino 
real :: ut0

COMMON/const2/icalls,nmono,iyearo,idaynro,rzino,igino,ut0
icalls=0
nmono=-1
iyearo=-1
idaynro=-1
rzino=.true.
igino=.true.
ut0=-1

jf = .true.
jf(4:6) = .false.

! --- command line input
argc = command_argument_count()
if (argc < 10) then
  write(stderr,*) 'need input parameters: year month day hour minute second glat glon f107a altkm(vector)'
  stop 1
endif

do i=1,6
  call get_command_argument(i,argv)
  read(argv,*) ymdhms(i)
enddo

call get_command_argument(7, argv)
read(argv,*) glat

call get_command_argument(8, argv)
read(argv,*) glon

call get_command_argument(9, argv)
read(argv,*) f107a

Nalt = argc-9
allocate(altkm(Nalt), outf(11,Nalt))
do i = 1,Nalt
  call get_command_argument(9+i, argv)
  read(argv,*) altkm(i)
enddo

! --- parse

mmdd = ymdhms(2) * 100 + ymdhms(3)
dhour = ymdhms(4) + ymdhms(5) / 60. + ymdhms(6) / 3600.


call IRI90(JF,JMAG,glat,glon, &
     -f107a, &
     MMDD, DHOUR+25., &
     altkm, Nalt, datadir, &
     OUTF,OARR)

!print '(A,ES10.3,A,F5.1,A)','NmF2 ',oarr(1),' [m^-3]     hmF2 ',oarr(2),' [km] '
!print '(A,F10.3,A,I3,A,F10.3)','F10.7 ',oarr(41), ' Ap ',int(oarr(51)),' B0 ',oarr(10)

!print *,'Altitude    Ne    O2+'
do i = 1,Nalt
  write(stdout, '(F10.3, 11ES16.8)') altkm(i), outf(:11,i)
enddo

print *,new_line(' ')

write(stdout, '(100ES16.8)') oarr

end program

