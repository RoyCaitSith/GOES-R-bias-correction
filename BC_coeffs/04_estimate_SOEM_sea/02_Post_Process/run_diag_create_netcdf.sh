#!/bin/bash

#####################################################
# machine set up (users should change this part)
#####################################################

#SBATCH --time=128:00:00 
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --account=zpu-kp
#SBATCH --partition=zpu-kp
#SBATCH -J netcdf
#SBATCH -o slurm-%j.out-%N
#SBATCH -e slurm-%j.err-%N
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=ROY.FENG@utah.edu

# Miniconda3
export PATH="/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/mymini3/bin:$PATH"

export DIR_MAIN="/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/24_Revision/BC_coeffs/04_estimate_SOEM_sea/02_Post_Process"

cd $DIR_MAIN && python script_02_create_diag_netcdf.py
