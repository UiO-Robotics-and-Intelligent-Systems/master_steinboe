#!/bin/bash

#paths=(
#"Results_01.02.2022_16.00.45"  
#"Results_02.02.2022_11.25.01"
#"Results_01.02.2022_05.01.27" 
#"Results_01.02.2022_16.05.45" 
#"Results_31.01.2022_20.12.18"
#"Results_01.02.2022_05.01.29"
#"Results_01.02.2022_21.36.54"
#"Results_31.01.2022_20.12.22"
#"Results_01.02.2022_05.01.30" 
#"Results_01.02.2022_21.36.58" #bare 511 2 og 5 
#"Results_31.01.2022_20.12.30"
#"Results_01.02.2022_05.01.38" # bare 511 2 og 5
#"Results_01.02.2022_21.38.34" # bare 511 2 og 5
#"Results_31.01.2022_20.12.38"
#"Results_01.02.2022_16.00.40"
#"Results_02.02.2022_11.24.58"
#)

#for dir in "${paths[@]}"; do
#    python3 EvolvingMLAgents.py 0 0 0 0 0 0 --checkpointHPC /home/steinboe/MasterThesis/resultsLinux/$dir 8192 128 &
#    wait
#done

#python3 EvolvingMLAgents.py 256 2048 0.3 0.2 0.1 0.01 -cnt 18 -mor 6 -co 0
python3 EvolvingMLAgents.py 0 0 0 0 0 0 0 --checkpointHPC /home/steinboe/MasterThesis/resultsLinux/Results_22.02.2022_15.33.21/subGen511Morph5/256ind_2048gen/morphology4 2048 128
