module set_crtm_cloudmod
!$$$ module documentation block
!           .      .    .                                       .
! module:   set_crtm_cloudmod
!  prgmmr: todling          org: gmao                date: 2011-06-01
!
! abstract: module providing interface to set-crtm-cloud procedures
!
! program history log:
!   2011-06-01  todling
!   2011-11-17  zhu     --- merge set_crtm_cloudmod with crtm_cloud
!
! subroutines included:
!   sub Set_CRTM_Cloud
!
! attributes:
!   language: f90
!   machine:
!
!$$$ end documentation block

  use kinds, only: i_kind,r_kind
  use constants, only: zero,one,two,five,r0_05,t0c,fv,rd,grav,pi
  use CRTM_Cloud_Define, only: CRTM_Cloud_type
  use CRTM_Cloud_Define, only: WATER_CLOUD,ICE_CLOUD,RAIN_CLOUD, &
      SNOW_CLOUD,GRAUPEL_CLOUD,HAIL_CLOUD 
  use mpeu_util, only: die

  implicit none

private
public Set_CRTM_Cloud

CONTAINS

  subroutine Set_CRTM_Cloud ( km, nac, cloud_name, icmask, nc, cloud_cont, cloud_mr, cloud_efr,jcloud, dp, tp, pr, qh, cloud)

  implicit none

  integer(i_kind) , intent(in)    :: km                ! number of levels
  integer(i_kind) , intent(in)    :: nac               ! number of actual clouds
  character(len=*), intent(in)    :: cloud_name(nac)   ! [nac]   Model cloud names: qi, ql, etc.
  logical,          intent(in)    :: icmask            ! mask determining where to consider clouds
  integer(i_kind),  intent(in)    :: nc                ! number of clouds
  integer(i_kind),  intent(in)    :: jcloud(nc)        ! cloud index
  real(r_kind),     intent(in)    :: cloud_cont(km,nc) ! cloud content 
  real(r_kind),     intent(in)    :: cloud_mr(km,nc)   ! cloud mixing ratio (kg/m2) 
  real(r_kind),     intent(in)    :: cloud_efr (km,nc) ! cloud effective radius
  real(r_kind),     intent(in)    :: dp(km)            ! [km]    
  real(r_kind),     intent(in)    :: tp(km)            ! [km]   atmospheric temperature (K)
  real(r_kind),     intent(in)    :: pr(km)            ! [km]   atmospheric pressure  
  real(r_kind),     intent(in)    :: qh(km)            ! [km]   specific humidity

  type(CRTM_Cloud_type), intent(inout) :: cloud(nc)    ! [nc]   CRTM Cloud object

  call setCloud (cloud_name, icmask, cloud_cont, cloud_mr, cloud_efr, jcloud, dp, tp, pr, qh, cloud)

  end subroutine Set_CRTM_Cloud

 
  subroutine setCloud (cloud_name, icmask, cloud_cont, cloud_mr, cloud_efr, jcloud, dp, tp, pr, qh, cloud)

  use gridmod, only: regional,wrf_mass_regional
  use wrf_params_mod, only: cold_start
  implicit none

! !ARGUMENTS:

  character(len=*), intent(in)    :: cloud_name(:)     ! [nc]    Model cloud names: Water, Ice, etc.
  logical,          intent(in)    :: icmask            !         mask for where to consider clouds  
  integer(i_kind),  intent(in)    :: jcloud(:)         !         cloud order
  real(r_kind),     intent(in)    :: cloud_cont(:,:)   ! [km,nc] cloud contents  (kg/m2)
  real(r_kind),     intent(in)    :: cloud_mr(:,:)     ! cloud mixing ratio (kg/m2) 
  real(r_kind),     intent(in)    :: cloud_efr (:,:)   ! [km,nc] cloud effective radius (microns)
  real(r_kind),     intent(in)    :: dp(:)             ! [km]    layer thickness   
  real(r_kind),     intent(in)    :: tp(:)             ! [km]    atmospheric temperature (K)
  real(r_kind),     intent(in)    :: pr(:)             ! [km]    atmospheric pressure (??)
  real(r_kind),     intent(in)    :: qh(:)             ! [km]    atmospheric specific humidity (??)

  type(CRTM_Cloud_type), intent(inout) :: cloud(:)     ! [nc]   CRTM Cloud object

! !DESCRIPTION: Set the CRTM Cloud object given Model cloud properties.
!
! !REVISION HISTORY:
!
! 03May2011  Min-Jeong  Initial version.
! 14May2011  Todling    Encapsulate Min-Jeong's code in present module.
! 01July2011 Zhu        Add jcloud and cloud_efr; add codes for the regional 
! 19Feb2013  Zhu        Add cold_start for the regional
!
!EOP
!-----------------------------------------------------------------------------

  character(len=*), parameter :: myname = 'setCloud'
  integer(i_kind) :: na, nc, km, n, k, nk, idx
  real(r_kind)    :: tem1,tem2,tem3,tem4

!  Additional variables to calculate the effective radius of rain, snow, and graupel

  real(r_kind) :: piover6
  real(r_kind) :: corr
  real(r_kind) :: rho ! air density kg/m3
  real(r_kind) :: qcl ! cloud liquid mixing ratio
  real(r_kind) :: qic ! cloud ice mixing ratio
  real(r_kind) :: qrn ! cloud rain mixing ratio
  real(r_kind) :: qsn ! cloud snow mixing ratio
  real(r_kind) :: qgr ! cloud graupel mixing ratio
  real(r_kind) :: temp, nic, diaic
  real(r_kind) :: n0_snow_fac, supcol
  real(r_kind) :: lamda_cloud
  real(r_kind) :: sum1_rain, sum2_rain, lamda_rain
  real(r_kind) :: sum1_snow, sum2_snow, lamda_snow
  real(r_kind) :: sum1_grau, sum2_grau, lamda_grau

  real(r_kind), parameter :: n0_cloud    = 300.0    ! cm(-3)
  real(r_kind), parameter :: n0_rain     = 0.08     ! cm(-4)
  real(r_kind), parameter :: n0_snow     = 0.02     ! cm(-4)
  real(r_kind), parameter :: n0_grau     = 0.04     ! cm(-4)
  real(r_kind), parameter :: n0_snow_max = 1.E3     ! cm(-4)
  real(r_kind), parameter :: rho_cloud   = 1000.0   ! kg m(-3)
  real(r_kind), parameter :: rho_rain    = 1000.0   ! kg m(-3)
  real(r_kind), parameter :: rho_snow    =  100.0   ! kg m(-3)
  real(r_kind), parameter :: rho_grau    =  500.0   ! kg m(-3)
  real(r_kind), parameter :: alpha       = 0.12
  real(r_kind), parameter :: limit       = 1.E-9

!  180 K -- 274 K; hexagonal columns assumed:
  real(r_kind), dimension(95), parameter :: retab =                      &
               (/ 5.92779, 6.26422, 6.61973, 6.99539, 7.39234,           &
                  7.81177, 8.25496, 8.72323, 9.21800, 9.74075, 10.2930,  &
                  10.8765, 11.4929, 12.1440, 12.8317, 13.5581, 14.2319,  &
                  15.0351, 15.8799, 16.7674, 17.6986, 18.6744, 19.6955,  &
                  20.7623, 21.8757, 23.0364, 24.2452, 25.5034, 26.8125,  &
                  27.7895, 28.6450, 29.4167, 30.1088, 30.7306, 31.2943,  &
                  31.8151, 32.3077, 32.7870, 33.2657, 33.7540, 34.2601,  &
                  34.7892, 35.3442, 35.9255, 36.5316, 37.1602, 37.8078,  &
                  38.4720, 39.1508, 39.8442, 40.5552, 41.2912, 42.0635,  &
                  42.8876, 43.7863, 44.7853, 45.9170, 47.2165, 48.7221,  &
                  50.4710, 52.4980, 54.8315, 57.4898, 60.4785, 63.7898,  &
                  65.5604, 71.2885, 75.4113, 79.7368, 84.2351, 88.8833,  &
                  93.6658, 98.5739, 103.603, 108.752, 114.025, 119.424,  &
                  124.954, 130.630, 136.457, 142.446, 148.608, 154.956,  &
                  161.503, 168.262, 175.248, 182.473, 189.952, 197.699,  &
                  205.728, 214.055, 222.694, 231.661, 240.971, 250.639 /)

!  Abscissas of Gauss-Laguerre Integration

  real(r_kind), dimension(32) :: xk = (/ 0.0444893658333, 0.23452610952, &
            0.576884629302, 1.07244875382, 1.72240877644, 2.52833670643, &
             3.49221327285, 4.61645677223, 5.90395848335,  7.3581268086, &
             8.98294126732,  10.783012089,  12.763745476, 14.9309117981, &
             17.2932661372, 19.8536236493, 22.6357789624, 25.6201482024, &
             28.8739336869, 32.3333294017, 36.1132042245, 40.1337377056, &
             44.5224085362, 49.2086605665, 54.3501813324, 59.8791192845, &
             65.9833617041, 72.6842683222, 80.1883747906,  88.735192639, &
             98.8295523184, 111.751398227 /)

!  total weights (weight*exp(xk)) of Gauss-Laguerre Integration

  real(r_kind), dimension(32) :: totalw = (/ 0.114187105768, 0.266065216898, &
             0.418793137325, 0.572532846497, 0.727648788453, 0.884536718946, &
              1.04361887597,  1.20534920595,  1.37022171969,  1.53877595906, &
              1.71164594592,   1.8895649683,  2.07318851235,  2.26590144444, &
              2.46997418988,  2.64296709494,  2.76464437462,  3.22890542981, &
              2.92019361963,   4.3928479809,  4.27908673189,  5.20480398519, &
              5.11436212961,  4.15561492173,  6.19851060567,  5.34795780128, &
              6.28339212457,  6.89198340969,  7.92091094244,  9.20440555803, &
              11.1637432904,  15.3902417688 /)

  real(r_kind), dimension(32) :: psd_rain, psd_snow, psd_grau

  km = size(cloud_cont,1)
  nc = size(cloud_cont,2)
  na = size(cloud_name)

! Handle hand-split case as particular case
! -----------------------------------------
  if (cold_start .or. (na /= nc .and. (.not. regional))) then

!    Initialize Loop over clouds ...
     do n = 1, nc
        Cloud(n)%Type = CloudType_(cloud_name(jcloud(n)))
        Cloud(n)%water_content(:) = zero
        cloud(n)%Effective_Radius(:) = zero
        cloud(n)%effective_variance(:) = two
     enddo

     if(icmask) then
        Cloud(1)%water_content(:) = cloud_cont(:,1)
        Cloud(2)%water_content(:) = cloud_cont(:,2)
        Cloud(3)%water_content(:) = cloud_cont(:,3)
        Cloud(4)%water_content(:) = cloud_cont(:,4)
        Cloud(5)%water_content(:) = cloud_cont(:,5)

        ! Set cloud content of liquid water, ice, rain, snow, and graupel to zero
!        Cloud(1)%water_content(:) = zero
!        Cloud(2)%water_content(:) = zero
!        Cloud(3)%water_content(:) = zero
!        Cloud(4)%water_content(:) = zero
!        Cloud(5)%water_content(:) = zero
     else
        Cloud(1)%water_content(:) = zero
        Cloud(2)%water_content(:) = zero
        Cloud(3)%water_content(:) = zero
        Cloud(4)%water_content(:) = zero
        Cloud(5)%water_content(:) = zero
     endif

!    Calculate effective radius for each cloud component (wired to 2)
!    ----------------------------------------------------------------
     if(icmask) then
        do k=1,km
           qcl = cloud_mr(k,1)
           qic = cloud_mr(k,2)
           qrn = cloud_mr(k,3)
           qsn = cloud_mr(k,4)
           qgr = cloud_mr(k,5)

           ! No liquid water, ice, rain, snow, and graupel
!           qcl = zero
!           qic = zero
!           qrn = zero
!           qsn = zero
!           qgr = zero

           ! liquid water cloud drop size
           rho    = pr(k) / rd / (tp(k) * (one + fv*qh(k)))
           supcol = t0c-tp(k)
!           tem4   = max(zero, supcol*r0_05)
!           cloud(1)%effective_radius(k) = five + five * min(one, tem4)

           piover6 = pi/6.0
           if (qcl > limit) then
              lamda_cloud = (piover6*rho_cloud*n0_cloud/rho/qcl)**(1.0/3.0)
              cloud(1)%effective_radius(k) = max(2.51, min(10000.0*1.5/lamda_cloud, 50.))
           end if

           ! ice water cloud particle size
!           tem2 = tp(k) - t0c
!           tem1 = grav/rd
!           tem3 = tem1 * cloud(2)%water_content(k) * (pr(k)/dp(k)) / (tp(k) * (one + fv * qh(k)))
!
!           if (tem2 < -50.0_r_kind ) then
!              cloud(2)%effective_radius(k) =  (1250._r_kind/9.917_r_kind)*tem3**0.109_r_kind
!           elseif (tem2 < -40.0_r_kind ) then
!              cloud(2)%effective_radius(k) =  (1250._r_kind/9.337_r_kind)*tem3**0.08_r_kind
!           elseif (tem2 < -30.0_r_kind ) then
!              cloud(2)%effective_radius(k) =  (1250._r_kind/9.208_r_kind)*tem3**0.055_r_kind
!           else
!              cloud(2)%effective_radius(k) =  (1250._r_kind/9.387_r_kind)*tem3**0.031_r_kind
!           endif

!           idx  = int(tp(k)-179.)
!           idx  = min(max(idx,1), 94)
!           corr = tp(k) - int(tp(k))
!           cloud(2)%effective_radius(k) = retab(idx)*(1.-corr) + retab(idx+1)*corr

!           cloud(2)%effective_radius(k) = 75
!           cloud(2)%effective_radius(k) = 30

           temp  = rho*qic
           temp  = sqrt(sqrt(temp*temp*temp))
           nic   = min(max(5.38E7*temp, 1.E3), 1.E6)
           diaic = min(11.9 * sqrt(rho*qic/nic), 500.E-6)
           if (qic > limit) then
              cloud(2)%effective_radius(k) = max(10.01, min(1.E6*0.75*0.163*diaic, 125.))
           end if

           !cloud rain/snow/graupel effective radius

!           sum1_rain = 0.0
!           sum2_rain = 0.0
!           sum1_snow = 0.0
!           sum2_snow = 0.0
!           sum1_grau = 0.0
!           sum2_grau = 0.0

           if ( qrn > limit ) then
              lamda_rain = (pi*rho_rain*n0_rain/rho/qrn)**0.25
              cloud(3)%effective_radius(k) = max(10000.0*1.5/800., min(10000.0*1.5/lamda_rain, 999.))
           end if
!           do nk = 1, 32
!              psd_rain(nk) = n0_rain*exp(-2.0*lamda_rain*xk(nk))
!              sum1_rain    = sum1_rain + totalw(nk) * (xk(nk)**3) * psd_rain(nk)
!              sum2_rain    = sum2_rain + totalw(nk) * (xk(nk)**2) * psd_rain(nk)
!           end do
!           cloud(3)%effective_radius(k) = 10000.0 * sum1_rain/sum2_rain

           n0_snow_fac = max(min(exp(alpha*supcol), n0_snow_max/n0_snow), 1.)
           if ( qsn > limit ) then
              lamda_snow = (pi*rho_snow*n0_snow*n0_snow_fac/rho/qsn)**0.25
              cloud(4)%effective_radius(k) = max(10000.0*0.5/1000., min(10000.0*0.5/lamda_snow, 999.))
           end if
!           do nk = 1, 32
!              psd_snow(nk) = n0_snow*exp(-2.0*lamda_snow*xk(nk))
!              sum1_snow    = sum1_snow + totalw(nk) * (xk(nk)**3) * psd_snow(nk)
!              sum2_snow    = sum2_snow + totalw(nk) * (xk(nk)**2) * psd_snow(nk)
!           end do
!           cloud(4)%effective_radius(k) = 10000.0 * sum1_snow/sum2_snow

           if ( qgr > limit ) then
              lamda_grau = (pi*rho_grau*n0_grau/rho/qgr)**0.25
              cloud(5)%effective_radius(k) = max(10000.0*1.5/600., min(10000.0*1.5/lamda_grau, 999.))
           end if
!           do nk = 1, 32
!              psd_grau(nk) = n0_grau*exp(-2.0*lamda_grau*xk(nk))
!              sum1_grau    = sum1_grau + totalw(nk) * (xk(nk)**3) * psd_grau(nk)
!              sum2_grau    = sum2_grau + totalw(nk) * (xk(nk)**2) * psd_grau(nk)
!           end do
!           cloud(5)%effective_radius(k) = 10000.0 * sum1_grau/sum2_grau

           cloud(1)%effective_radius(k)=max(zero, cloud(1)%effective_radius(k))
           cloud(2)%effective_radius(k)=max(zero, cloud(2)%effective_radius(k))
           cloud(3)%effective_radius(k)=max(zero, cloud(3)%effective_radius(k))
           cloud(4)%effective_radius(k)=max(zero, cloud(4)%effective_radius(k))
           cloud(5)%effective_radius(k)=max(zero, cloud(5)%effective_radius(k))
        end do
        cloud(1)%effective_variance(:) = two
        cloud(2)%effective_variance(:) = two
        cloud(3)%effective_variance(:) = two
        cloud(4)%effective_variance(:) = two
        cloud(5)%effective_variance(:) = two
     else
        cloud(1)%effective_radius  (:) = zero
        cloud(2)%effective_radius  (:) = zero
        cloud(3)%effective_radius  (:) = zero
        cloud(4)%effective_radius  (:) = zero
        cloud(5)%effective_radius  (:) = zero
        cloud(1)%effective_variance(:) = two
        cloud(2)%effective_variance(:) = two
        cloud(3)%effective_variance(:) = two
        cloud(4)%effective_variance(:) = two
        cloud(5)%effective_variance(:) = two
     endif
  else ! Handle general case with arbitray number of clouds
       ! --------------------------------------------------

!    Loop over clouds ...
!    --------------------
     do n = 1, nc

!       Map Model cloud names into CRTM Cloud indices
!       ---------------------------------------------
        Cloud(n)%Type = CloudType_(cloud_name(jcloud(n)))

        if(icmask) then
           Cloud(n)%water_content(:) = cloud_cont(:,n)
        else
           Cloud(n)%water_content(:) = zero
        endif

!       Calculate effective radius of given cloud type
!       ----------------------------------------------
        if(icmask) then
           if (regional .and. (.not. wrf_mass_regional)) then
              cloud(n)%Effective_Radius(:) = cloud_efr(:,n)
           else
              cloud(n)%Effective_Radius(:) = EftSize_(cloud_name(jcloud(n)))
           end if
        else
           cloud(n)%Effective_Radius(:) = zero
        endif
        cloud(n)%effective_variance(:) = two

     enddo

  endif
  end subroutine setCloud

  function CloudType_(name) Result(ctype)
    character(len=*), parameter :: myname = 'CloudType_'
    character(len=*) :: name  ! Model cloud name
    integer(i_kind)  :: ctype ! CRTM cloud type

    if ( trim(name) == 'ql' ) then
       ctype = WATER_CLOUD
    else if ( trim(name) == 'qi' ) then
       ctype = ICE_CLOUD
    else if ( trim(name) == 'qh' ) then
       ctype = HAIL_CLOUD
    else if ( trim(name) == 'qg' ) then
       ctype = GRAUPEL_CLOUD
    else if ( trim(name) == 'qr' ) then
       ctype = RAIN_CLOUD
    else if ( trim(name) == 'qs' ) then
       ctype = SNOW_CLOUD

    else
       call die(myname,"cannot recognize cloud name <"//trim(name)//">")
    end if

  end function CloudType_

  function EftSize_(name) Result(csize)
    character(len=*), parameter :: myname = 'EftSize_'
    character(len=*) :: name  ! Model cloud name
    real(r_kind)     :: csize ! CRTM cloud type

! Note: Values below from Tom Auligne
    if ( trim(name) == 'ql' ) then
       csize = 10.0_r_kind  ! in micron
    else if ( trim(name) == 'qi' ) then
       csize = 30.0_r_kind
    else if ( trim(name) == 'qh' ) then
       csize = zero ! RT: can somebody fill this in?
    else if ( trim(name) == 'qg' ) then
       csize = 600.0_r_kind
    else if ( trim(name) == 'qr' ) then
       csize = 300.0_r_kind
    else if ( trim(name) == 'qs' ) then
       csize = 600.0_r_kind

    else
       call die(myname,"cannot recognize cloud name <"//trim(name)//">")
    end if

  end function EftSize_

end module set_crtm_cloudmod
