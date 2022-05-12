#!/bin/bash
#                                    mutP mutS cross init
#python3 EvolvingMLAgents.py 256 4096 0.3 0.2 0.1 0.01  128 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 256 4096 1.0 x 0.1 0.04  128 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 256 4096 1.0 x 0.1 0.06  128 -cnt 18 -mor 6


#new hyperparams
dir=/fp/homes01/u01/ec-steinboe/resultsLinux/Results_27.03.2022_21.10.18 #1
#dir=/fp/homes01/u01/ec-steinboe/resultsLinux/Results_27.03.2022_21.10.17 #2
#dir=/fp/homes01/u01/ec-steinboe/resultsLinux/Results_27.03.2022_23.13.01 #3

#dir=/fp/homes01/u01/ec-steinboe/resultsLinux/ #4
#dir=/fp/homes01/u01/ec-steinboe/resultsLinux/ #5
#dir=/fp/homes01/u01/ec-steinboe/resultsLinux/ #6

#dir=/fp/homes01/u01/ec-steinboe/resultsLinux/ #7
#dir=/fp/homes01/u01/ec-steinboe/resultsLinux/ #8 
#dir=/fp/homes01/u01/ec-steinboe/resultsLinux/ #9


#dir=/fp/homes01/u01/ec-steinboe/resultsLinux/ #11
#dir=/fp/homes01/u01/ec-steinboe/resultsLinux/ #12
#dir=/fp/homes01/u01/ec-steinboe/resultsLinux/  #13

python3 EvolvingMLAgents.py 0 0 0 0 0 0 0 --checkpointHPC "$dir" 4096 128

