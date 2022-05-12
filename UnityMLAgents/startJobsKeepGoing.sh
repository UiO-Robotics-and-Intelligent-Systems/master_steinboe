#!/bin/bash
#SBATCH --account=ec12
#SBATCH --job-name=keepG
#SBATCH --time=1-0:0:0
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
set -o errexit
set -o nounset
#source /fp/homes01/u01/ec-steinboe/env/Scripts/activate
srun keepGoing.sh
