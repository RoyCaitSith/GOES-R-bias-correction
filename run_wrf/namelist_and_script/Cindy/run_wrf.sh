#!/bin/bash

#####################################################
# machine set up (users should change this part)
#####################################################

#SBATCH --time=72:00:00
#SBATCH --nodes=2
#SBATCH --ntasks=48
#SBATCH --account=zpu-kp
#SBATCH --partition=zpu-kp
#SBATCH -J 17062000 
#SBATCH -o slurm-%j.out-%N
#SBATCH -e slurm-%j.err-%N
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=ROY.FENG@utah.edu

module purge
module load intel-oneapi-compilers/2021.4.0
module load openmpi/4.1.1
module load netcdf-c/4.8.1 netcdf-fortran/4.5.3
module load parallel-netcdf/1.12.2
module load hdf5
module load perl

export NETCDF="/uufs/chpc.utah.edu/sys/spack/linux-rocky8-nehalem/intel-2021.4.0/netcdf-impi"
export PATH="$NETCDF:$PATH"
export LD_LIBRARY_PATH="$NETCDF/lib:$LD_LIBRARY_PATH"
export HDF5="$HDF5_ROOT"
export PATH="$HDF5:$PATH"
export LD_LIBRARY_PATH="$HDF5/lib:$LD_LIBRARY_PATH"

export SCRATCH_DIRECTORY=/scratch/general/lustre/u1237353/Cindy_ASRC01 
export RUN_WRF_DIRECTORY=$SCRATCH_DIRECTORY/Run_WRF

mpirun -np $SLURM_NTASKS $RUN_WRF_DIRECTORY/wrf.exe >& $RUN_WRF_DIRECTORY/log.wrf

exit 0
