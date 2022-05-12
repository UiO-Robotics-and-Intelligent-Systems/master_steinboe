#!/bin/bash
#for dir in /fp/homes01/u01/ec-steinboe/resultsLinux/*/
#do
dir="/fp/homes01/u01/ec-steinboe/resultsLinux/Results_28.02.2022_16.19.02"
python3 EvolvingMLAgents.py 0 0 0 0 0 0 0 --splitMorphologies 4095 8 $dir
dir="/fp/homes01/u01/ec-steinboe/resultsLinux/Results_28.02.2022_17.09.10"
python3 EvolvingMLAgents.py 0 0 0 0 0 0 0 --splitMorphologies 4095 8 $dir
#done
