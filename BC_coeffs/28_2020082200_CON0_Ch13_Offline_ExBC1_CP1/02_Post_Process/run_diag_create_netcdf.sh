#!/bin/bash

#####################################################
# machine set up (users should change this part)
#####################################################

#SBATCH --time=72:00:00 
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --account=zpu-kp
#SBATCH --partition=zpu-kp
#SBATCH -J netcdf
#SBATCH -o slurm-%j.out-%N
#SBATCH -e slurm-%j.err-%N
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=ROY.FENG@utah.edu

module purge
module load ncl
module load ncview
module load cmake/3.13.3
module load intel-oneapi-compilers/2021.4.0 intel-oneapi-mpi/2021.4.0 intel-oneapi-mkl/2022.0.2 hdf5

# Miniconda3
export PATH="$HOME/mymini3/bin:$PATH"

# NCL
export NCARG_COLORMAP_PATH="/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/03_cpex_figures/colormaps"

# NETCDF
export NETCDF="/uufs/chpc.utah.edu/sys/spack/linux-rocky8-nehalem/intel-2021.4.0/netcdf-impi"
export PATH="$NETCDF:$PATH"
export LD_LIBRARY_PATH="$NETCDF/lib:$LD_LIBRARY_PATH"

# HDF5
export HDF5="$HDF5_ROOT"
export PATH="$HDF5:$PATH"
export LD_LIBRARY_PATH="$HDF5/lib:$LD_LIBRARY_PATH"

export DIR_MAIN="/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/24_Revision/BC_coeffs/19_2017051118_CON0_Ch13_Offline_ExBC1_CP4_AR1_TC3/02_Post_Process"

cd $DIR_MAIN && python script_02_create_diag_netcdf.py
