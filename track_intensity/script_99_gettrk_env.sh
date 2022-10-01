module purge
module load ncl
module load ncview
module load cmake/3.21.4
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
