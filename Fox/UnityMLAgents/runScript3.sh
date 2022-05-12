#!/bin/bash

paths=(
#"Results_01.02.2022_16.00.45"  
#"Results_02.02.2022_11.25.01"
#"Results_01.02.2022_05.01.27" 
#"Results_01.02.2022_16.05.45" 
#"Results_31.01.2022_20.12.18"
#"Results_01.02.2022_05.01.29"
#"Results_01.02.2022_21.36.54"
#"Results_31.01.2022_20.12.22"
#"Results_01.02.2022_05.01.30" 
#"Results_01.02.2022_21.36.58" 
#"Results_31.01.2022_20.12.30"
#"Results_01.02.2022_05.01.38"
#"Results_01.02.2022_21.38.34" 
#"Results_31.01.2022_20.12.38"
#"Results_01.02.2022_16.00.40"
#"Results_02.02.2022_11.24.58"
)
generations=(
511
1023
)

for gen in "${generations[@]}"; do
for dir in "${paths[@]}"; do
    python3 EvolvingMLAgents.py 0 0 0 0 0 0 --pretrainedMorphology 511 0 /home/steinboe/MasterThesis/resultsLinux/$dir/subGen511 &
    python3 EvolvingMLAgents.py 0 0 0 0 0 0 --pretrainedMorphology 511 1 /home/steinboe/MasterThesis/resultsLinux/$dir/subGen511 &
    python3 EvolvingMLAgents.py 0 0 0 0 0 0 --pretrainedMorphology 511 2 /home/steinboe/MasterThesis/resultsLinux/$dir/subGen511 &
    python3 EvolvingMLAgents.py 0 0 0 0 0 0 --pretrainedMorphology 511 3 /home/steinboe/MasterThesis/resultsLinux/$dir/subGen511 &
    python3 EvolvingMLAgents.py 0 0 0 0 0 0 --pretrainedMorphology 511 4 /home/steinboe/MasterThesis/resultsLinux/$dir/subGen511 &
    python3 EvolvingMLAgents.py 0 0 0 0 0 0 --pretrainedMorphology 511 5 /home/steinboe/MasterThesis/resultsLinux/$dir/subGen511 &
    python3 EvolvingMLAgents.py 0 0 0 0 0 0 --pretrainedMorphology 511 6 /home/steinboe/MasterThesis/resultsLinux/$dir/subGen511 &
    python3 EvolvingMLAgents.py 0 0 0 0 0 0 --pretrainedMorphology 511 7 /home/steinboe/MasterThesis/resultsLinux/$dir/subGen511 &
done
done
