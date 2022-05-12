#!/bin/bash                                                                                                                                                                                                 

# This is a template for a slurm job script.
# To start a job on robin-hpc please use the command "sbatch nameofthisscript.sh".                                                                                                                            

# Job name                                                                                                                                                                                                  
#SBATCH --job-name=steinarsJob                                                                                                                                                                              

# Wall clock time limit (hh:mm:ss). 
# (Note: The program will be killed when the time limit is reached.)                                                                                                         
#SBATCH --time=01:00:00                                                                                                                                                                                     

# Number of tasks to start in parallel from this script.                                                                                                                                                    
# (i.e. myprogram.py below will be started ntasks times)                                                                                                                                                    
#SBATCH --ntasks=1                                                                                                                                                                                          

# CPUs allocated per task                                                                                                                                                                                   
#SBATCH --cpus-per-task=60                                                                                                                                                                                  

# Memory allocated per cpu                                                                                                                                                                                  
#SBATCH --mem-per-cpu=1G                                                                                                                                                                                    

# Set exit on errors                                                                                                                                                                                      
set -o errexit
set -o nounset

# Load your environment                                                                                                                                                                                     
source /home/steinboe/MasterThesis/env/Scripts/activate

# Run your program with "srun yourcommand"                                                                                                                                                                  
# stdout and stderr will be written to a file "slurm-jobid.out".                                                                                                                                            
# (warning: all tasks will write to the same slurm.out file)                                                                                                                                                
srun runScript3.sh

