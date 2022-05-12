#!/bin/bash
generations=(
511
#1023
)

morphs=(
8
)

for dir in /fp/homes01/u01/ec-steinboe/resultsLinux/*; do
for gen in "${generations[@]}"; do
for mor in "${morphs[@]}"; do
	python3 EvolvingMLAgents.py 0 0 0 0 0 0 0 --pretrainedMorphology $gen 6 $dir/subGen${gen}Morph${mor} 256 2048 128
done
done
done
