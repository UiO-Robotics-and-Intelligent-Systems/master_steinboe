#!/bin/bash
#SBATCH --account=ec12
#SBATCH --job-name=R1M2_1
#SBATCH --time=1-0:0:0
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=128
#SBATCH --mem-per-cpu=1G
set -o errexit
set -o nounset
source /fp/homes01/u01/ec-steinboe/env/Scripts/activate
srun pretrainedMorph256_2.sh
