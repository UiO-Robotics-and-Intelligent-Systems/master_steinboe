#!/bin/bash
for dir in /fp/homes01/u01/ec-steinboe/resultsLinux/*/
do
python3 EvolvingMLAgents.py 0 0 0 0 0 0 0 --splitMorphologies 511 8 $dir
done
