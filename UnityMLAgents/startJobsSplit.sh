#!/bin/bash
#SBATCH --account=ec12
#SBATCH --job-name=512Split
#SBATCH --time=0-0:10:0
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=128
#SBATCH --mem-per-cpu=1G
set -o errexit
set -o nounset
source /fp/homes01/u01/ec-steinboe/env/Scripts/activate
srun splitMorph.sh 

