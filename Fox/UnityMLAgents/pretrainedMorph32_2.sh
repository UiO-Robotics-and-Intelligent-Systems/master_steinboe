#!/bin/bash

paths=(
#"Results_01.02.2022_16.00.45" #
#"Results_02.02.2022_11.25.01" #
#"Results_01.02.2022_05.01.27" 
#"Results_01.02.2022_16.05.45" 
#"Results_31.01.2022_20.12.18"
#"Results_01.02.2022_05.01.29"
#"Results_01.02.2022_21.36.54" #
#"Results_31.01.2022_20.12.22"
#"Results_01.02.2022_05.01.30" #
"Results_01.02.2022_21.36.58" #bare 511 2 og 5 
#"Results_31.01.2022_20.12.30"
"Results_01.02.2022_05.01.38" # bare 511 2 og 5
"Results_01.02.2022_21.38.34" # bare 511 2 og 5
#"Results_31.01.2022_20.12.38"
#"Results_01.02.2022_16.00.40"
#"Results_02.02.2022_11.24.58"#
)
generations=(
511 #fedig tror jeg
#1023 # ikke ferdig
)

morphs=(
8
)
    
for gen in "${generations[@]}"; do
for dir in "${paths[@]}"; do
for mor in "${morphs[@]}"; do
    python3 EvolvingMLAgents.py 0 0 0 0 0 0 --pretrainedMorphology $gen 2 /home/steinboe/MasterThesis/resultsLinux/$dir/subGen${gen}Morph${mor} 32 4096 &
    wait
done
done
done
