#!/bin/bash
#python3 EvolvingMLAgents.py 120 250 0.4 0.1 0.3 0.01 -cnt 18 -mor 6

#@echo off
#               popSize generations, mutProb, mutSigma, crossProb, initProb -cnt 15/18/24 -mor 4/6?
#py EvolvingMLAgents.py 32 100 0.5 0.1 0.1 0.01 -cnt 18 -mor 6
# python3 EvolvingMLAgents.py 120 250 0.1 0.1 0.2 0.01 -cnt 18 -mor 6

# del 1: vanlig co-evolving. del 2: noen annet. del 3: noen annet

# FOR TESTING DEL 1.0: (HUSK Å IKKE SETTE SEED TIL NONE) 128 gen vs 64. Er 500 gen mer enn nok? Skal convergere på ca 50%
#python3 EvolvingMLAgents.py 64 500 0.5 0.2 0.1 0.01 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 64 500 0.5 0.2 0.1 0.01 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 64 500 0.5 0.2 0.1 0.01 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 64 500 0.5 0.2 0.1 0.01 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 128 500 0.5 0.2 0.1 0.01 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 128 500 0.5 0.2 0.1 0.01 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 128 500 0.5 0.2 0.1 0.01 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 128 500 0.5 0.2 0.1 0.01 -cnt 18 -mor 6
# det holder med 64 (det er en begrensning sier jeg), men må kanskje ha mer enn 500 gen. Prøver 1000

# fOR TESTING DEL 1.1: hyperparameter for vanlig co-evol (mulig resultat man skal ta med seg)
#python3 EvolvingMLAgents.py 64 1000 0.5 0.2 0.1 0.01 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 64 1000 0.5 0.2 0.1 0.01 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 64 1000 0.5 0.2 0.1 0.01 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 64 1000 0.5 0.2 0.1 0.01 -cnt 18 -mor 6

#python3 EvolvingMLAgents.py 64 1000 0.6 0.2 0.05 0.01 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 64 1000 0.6 0.2 0.05 0.01 -cnt 18 -mor 6
# kom hit første gang
#python3 EvolvingMLAgents.py 64 1000 0.6 0.2 0.05 0.01 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 64 1000 0.6 0.2 0.05 0.01 -cnt 18 -mor 6
# kom hit nå- Hvorfor funker det ikke lengre???? Dette må fikses
#python3 EvolvingMLAgents.py 64 1000 0.4 0.2 0.2 0.01 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 64 1000 0.4 0.2 0.2 0.01 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 64 1000 0.4 0.2 0.2 0.01 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 64 1000 0.4 0.2 0.2 0.01 -cnt 18 -mor 6

#python3 EvolvingMLAgents.py 64 1000 0.3 0.2 0.1 0.01 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 64 1000 0.3 0.2 0.1 0.01 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 64 1000 0.3 0.2 0.1 0.01 -cnt 18 -mor 6
#python3 EvolvingMLAgents.py 64 1000 0.3 0.2 0.1 0.01 -cnt 18 -mor 6
#
# MER SOM ER FORNUFTIG
# Tren med annen init-prob

# FOR TESTING DEL 2.1: Velg parameter fra over, kjør co-evolution versjon 1. Ikke konvergens mål før man skrur av mor
python3 EvolvingMLAgents.py 64 1000 0.1 0.2 0.1 0.01 -cnt 18 -mor 6 -co 1 -initGen 500
python3 EvolvingMLAgents.py 64 1000 0.1 0.2 0.1 0.01 -cnt 18 -mor 6 -co 1 -initGen 500
#
#python3 EvolvingMLAgents.py 64 1000 0.3 0.2 0.1 0.01 -cnt 18 -mor 6 -co 1 -initGen 300
#python3 EvolvingMLAgents.py 64 1000 0.3 0.2 0.1 0.01 -cnt 18 -mor 6 -co 1 -initGen 300
#
#python3 EvolvingMLAgents.py 64 1000 0.3 0.2 0.1 0.01 -cnt 18 -mor 6 -co 1 -initGen 1000 # 1000 betyr konvergens
#python3 EvolvingMLAgents.py 64 1000 0.3 0.2 0.1 0.01 -cnt 18 -mor 6 -co 1 -initGen 1000 # 1000 betyr konvergens

# FOR TESTING DEL 2.2: Velg parameter fra over, kjør co-evolution versjon 2. Ikke konvergens mål før man skrur av cnt
#python3 EvolvingMLAgents.py 64 1000 0.3 0.2 0.1 0.01 -cnt 18 -mor 6 -co 2 -initGen 100
#python3 EvolvingMLAgents.py 64 1000 0.3 0.2 0.1 0.01 -cnt 18 -mor 6 -co 2 -initGen 100
#
#python3 EvolvingMLAgents.py 64 1000 0.3 0.2 0.1 0.01 -cnt 18 -mor 6 -co 2 -initGen 300
#python3 EvolvingMLAgents.py 64 1000 0.3 0.2 0.1 0.01 -cnt 18 -mor 6 -co 2 -initGen 300

#python3 EvolvingMLAgents.py 64 1000 0.3 0.2 0.1 0.01 -cnt 18 -mor 6 -co 2 -initGen 1000 # 1000 betyr konvergens
#python3 EvolvingMLAgents.py 64 1000 0.3 0.2 0.1 0.01 -cnt 18 -mor 6 -co 2 -initGen 1000 # 1000 betyr konvergens


# FOR TESTING DEL 2.3: Velg parameter fra over, kjør co-evolution versjon 3. 
# avgjør om du bruker konvergens eller x-antal init-conv fra testene over (beste hadde vært og prøv alt igjen, men det har vi ikke tid til)
# bruk bare konvergens mellom ny switching
#python3 EvolvingMLAgents.py 64 1000 0.3 0.2 0.1 0.01 -cnt 18 -mor 6 -co 3 -initGen 1000 # 1000 betyr konvergens
#python3 EvolvingMLAgents.py 64 1000 0.3 0.2 0.1 0.01 -cnt 18 -mor 6 -co 3 -initGen 1000 # 1000 betyr konvergens
#python3 EvolvingMLAgents.py 64 1000 0.3 0.2 0.1 0.01 -cnt 18 -mor 6 -co 3 -initGen 1000 # 1000 betyr konvergens
#python3 EvolvingMLAgents.py 64 1000 0.3 0.2 0.1 0.01 -cnt 18 -mor 6 -co 3 -initGen 1000 # 1000 betyr konvergens




# FOR TESTING DEL 3.0: Velg parameter fra over, kjør co-evolution versjon 1 og 2


