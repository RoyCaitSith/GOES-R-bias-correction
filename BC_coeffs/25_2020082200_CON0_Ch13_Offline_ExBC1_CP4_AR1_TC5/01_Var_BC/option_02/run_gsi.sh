#!/bin/bash 

#SBATCH --time=6:00:00 
#SBATCH --nodes=2
#SBATCH --ntasks=48
#SBATCH --account=zpu-kp
#SBATCH --partition=zpu-kp
#SBATCH -J gsi
#SBATCH -o slurm-%j.out-%N
#SBATCH -e slurm-%j.err-%N
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=ROY.FENG@utah.edu

module purge
module load cmake/3.13.3
module load intel-oneapi-compilers/2021.4.0 intel-oneapi-mpi/2021.4.0 intel-oneapi-mkl/2022.0.2 hdf5

# NETCDF
export PATH="/uufs/chpc.utah.edu/sys/spack/linux-rocky8-nehalem/intel-2021.4.0/netcdf:$PATH"
export NETCDF="/uufs/chpc.utah.edu/sys/spack/linux-rocky8-nehalem/intel-2021.4.0/netcdf"

# HDF5
export HDF5=$HDF5_ROOT
export LD_LIBRARY_PATH="$HDF5/lib:$LD_LIBRARY_PATH"

set -x

RUN_COMMAND="mpirun -genv OMP_NUM_THREADS=1 -np 48 "
${RUN_COMMAND} ./gsi.x > stdout 2>&1
