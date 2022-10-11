#!/bin/bash -l

####################################
#     ARIS slurm script template   #
#                                  #
# Submit script: sbatch filename   #
#                                  #
####################################

#SBATCH --job-name=jobname    # Job name
#SBATCH --output=jobname.%j.out # Stdout (%j expands to jobId)
#SBATCH --error=jobname.%j.err # Stderr (%j expands to jobId)
#SBATCH --ntasks=20     # Number of tasks(processes)
#SBATCH --nodes=1     # Number of nodes requested
#SBATCH --ntasks-per-node=20     # Tasks per node
#SBATCH --cpus-per-task=1     # Threads per task
#SBATCH --time=00:01:00   # walltime
#SBATCH --mem=56G   # memory per NODE
#SBATCH --partition=compute    # Partition
#SBATCH --account=myaccount   # Replace with your system project

if [ x$SLURM_CPUS_PER_TASK == x ]; then
  export OMP_NUM_THREADS=1
else
  export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
fi


## LOAD MODULES ##
module purge        # clean up loaded modules 

# load necessary modules
module load gnu/4.9.2
module load intel/15.0.3
module load intelmpi/5.0.3
module load cuda/8.0.61

## RUN YOUR PROGRAM ##
srun -n 20 echo 'hello world'
