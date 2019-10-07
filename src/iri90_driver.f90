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

character(:), allocatable :: datadir


jf = .true.
jf(5) = .false.
jf(12) = .true.

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

call get_command_argument(10, argv)
datadir = trim(argv)

Nalt = argc-10
allocate(altkm(Nalt), outf(11,Nalt))
do i = 1,Nalt
  call get_command_argument(10+i, argv)
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


write(stdout, '(/,100ES16.8)') oarr

end program
