#!/bin/bash

# Example of running python script with a job array

#SBATCH -J Lisa_final		                                # Job name
#SBATCH -p workstations			                                    # Partition. workstations or assemblix. See sinfo
#SBATCH --array=1-999                                       # how many tasks in the array
#SBATCH -c 1                                                    # one CPU core per task
#SBATCH -t 7:00			                                            # Time limit per job
#SBATCH --chdir /homes/ljbhu/thema2/project/pypovray        	  # Working dir
#SBATCH -o /homes/ljbhu/thema2/project/pypovray/slurms/output.%a.out          # STDOUT

# Run python script with a command line argument
# srun deals with using the slurm reservation, making the relevant hardware available to the script/program to run, and if applicable, MPI communication
srun python3 eindopdracht_LisaHu_MaartjevdHulst.py $SLURM_ARRAY_TASK_ID

#Run in terminal met SBATCH
