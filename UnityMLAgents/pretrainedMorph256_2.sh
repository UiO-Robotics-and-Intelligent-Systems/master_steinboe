#!/bin/bash

#sleep 8m
generations=(
#511
#1023
4095
)

morphs=(
8
)

#for dir in /fp/homes01/u01/ec-steinboe/resultsLinux/*; do
dir="/fp/homes01/u01/ec-steinboe/resultsLinux/Results_28.02.2022_16.19.02"
for gen in "${generations[@]}"; do
for mor in "${morphs[@]}"; do
	python3 EvolvingMLAgents.py 0 0 0 0 0 0 0 --pretrainedMorphology $gen 2 $dir/subGen${gen}Morph${mor} 256 8192 128
#done
done
done
