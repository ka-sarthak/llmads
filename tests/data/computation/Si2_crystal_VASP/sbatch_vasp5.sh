#!/bin/bash

# Request 16 nodes (2048 MPI tasks at 128 tasks per node) for 20 minutes.   

#SBATCH --job-name=Si_VR
#SBATCH --nodes=1
#SBATCH --tasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --time=23:55:00

# Replace [budget code] below with your project code (e.g. t01)
#SBATCH --account=e720
#SBATCH --partition=standard
#SBATCH --qos=standard

# Setup the job environment (this module needs to be loaded before any other modules)
module load epcc-job-env
module load vasp/5
# Load the VASP module, avoid any unintentional OpenMP threading by
# setting OMP_NUM_THREADS, and launch the code.
export OMP_NUM_THREADS=1


srun --distribution=block:block --hint=nomultithread vasp_std > output01.txt
