@echo off
REM               popSize generations, mutProb, mutSigma, crossProb, initProb -cnt 15/18/24 -mor 4/6?

py EvolvingMLAgents.py 8 10 0.1 0.2 0.05 0.01 8 -cnt 18 -mor 6


REM py EvolvingMLAgents.py 32 80 0.6 0.2 0.05 0.01 -cnt 18 -mor 6 -co 0

REM py EvolvingMLAgents.py 0 0 0 0 0 0 --checkpoint
 

REM py EvolvingMLAgents.py 0 0 0 0 0 0 --splitMorphologies 40 8 C:\Users\stein\Documents\Unity\results\Results_07.02.2022_15.37.33

REM     --pretraindMorphology lastGen morphologyNumber path popSize generations, (mutProb, mutSigma, crossProb, initProb)
REM py EvolvingMLAgents.py 0 0 0 0 0 0 --pretrainedMorphology 40 1 C:\Users\stein\Documents\Unity\results\Results_07.02.2022_15.37.33\subGen40Morph8
