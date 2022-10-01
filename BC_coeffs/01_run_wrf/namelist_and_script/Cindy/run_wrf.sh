#!/bin/bash

#####################################################
# machine set up (users should change this part)
#####################################################

#SBATCH --time=72:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --account=zpu-kp
#SBATCH --partition=zpu-kp
#SBATCH -J 17062418 
#SBATCH -o slurm-%j.out-%N
#SBATCH -e slurm-%j.err-%N
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=ROY.FENG@utah.edu

export WORK_DIRECTORY=/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng
export SCRATCH_DIRECTORY=/scratch/general/lustre/u1237353/CHPC_2017062418 
export RUN_WRF_DIRECTORY=$SCRATCH_DIRECTORY/Run_WRF

ln -sf $WORK_DIRECTORY/WPS/geogrid.exe $RUN_WRF_DIRECTORY/geogrid.exe
ln -sf $WORK_DIRECTORY/WPS/ungrib/Variable_Tables/Vtable.GFS $RUN_WRF_DIRECTORY/Vtable
ln -sf $WORK_DIRECTORY/WPS/ungrib.exe $RUN_WRF_DIRECTORY/ungrib.exe
ln -sf $WORK_DIRECTORY/WPS/link_grib.csh $RUN_WRF_DIRECTORY/link_grib.csh
ln -sf $WORK_DIRECTORY/WPS/metgrid.exe $RUN_WRF_DIRECTORY/metgrid.exe
$RUN_WRF_DIRECTORY/link_grib.csh $SCRATCH_DIRECTORY/GFS_Anl_Boundary_Condition_Data/gfs* $RUN_WRF_DIRECTORY
mv $SCRATCH_DIRECTORY/namelist.wps $RUN_WRF_DIRECTORY/namelist.wps

mpirun -np $SLURM_NTASKS $RUN_WRF_DIRECTORY/geogrid.exe >& $RUN_WRF_DIRECTORY/log.geogrid
$RUN_WRF_DIRECTORY/ungrib.exe >& $RUN_WRF_DIRECTORY/log.ungrib 
mpirun -np $SLURM_NTASKS $RUN_WRF_DIRECTORY/metgrid.exe >& $RUN_WRF_DIRECTORY/log.metgrid

ln -sf $SCRATCH_DIRECTORY/Metgrid_Data/met_em* $RUN_WRF_DIRECTORY
ln -sf $WORK_DIRECTORY/WRF/run/* $RUN_WRF_DIRECTORY
mv $SCRATCH_DIRECTORY/namelist.input $RUN_WRF_DIRECTORY/namelist.input

mpirun -np $SLURM_NTASKS $RUN_WRF_DIRECTORY/real.exe >& $RUN_WRF_DIRECTORY/log.real 
mpirun -np $SLURM_NTASKS $RUN_WRF_DIRECTORY/wrf.exe >& $RUN_WRF_DIRECTORY/log.wrf 

exit 0
