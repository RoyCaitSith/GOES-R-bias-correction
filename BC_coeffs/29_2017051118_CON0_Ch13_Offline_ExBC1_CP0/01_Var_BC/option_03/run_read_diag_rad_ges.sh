#!/bin/bash

#####################################################
# machine set up (users should change this part)
#####################################################

#SBATCH --time=6:00:00 
#SBATCH --nodes=2
#SBATCH --ntasks=48
#SBATCH --account=zpu-kp
#SBATCH --partition=zpu-kp
#SBATCH -J diag
#SBATCH -o slurm-%j.out-%N
#SBATCH -e slurm-%j.err-%N
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=ROY.FENG@utah.edu

export DIR_OPTION="/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/24_Revision/BC_coeffs/29_2017051118_CON0_Ch13_Offline_ExBC1_CP0/01_Var_BC/option_03"

cd $DIR_OPTION && ./read_diag_rad_ges.x
