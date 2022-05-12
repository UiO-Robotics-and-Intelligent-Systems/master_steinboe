import json
import argparse
from tkinter.filedialog import askdirectory
import sys
from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.side_channel.side_channel import SideChannel
from Individual import WaveIndividual
from EvolvingMLAgents import evaluate
from stringLogSideChannel import StringLogSideChannel
import random
import numpy as np
import platform
import time
from EvolutionaryAlgorithm import createEnvironment, warmUpEnvironment, getSolutions, getSolution

if platform.system()=='Windows': 
    BUILD_PATH="C:\\Users\\stein\\Documents\\Unity\\builds\\windows\\Crawler"
    RESULT_PATH="C:/Users/stein/Documents/Unity/results/"
elif platform.system()=='Linux':
    BUILD_PATH ="/uio/hume/student-u01/steinboe/Documents/master/MasterThesis/builds/linux/Crawler/Crawler.x86_64"
    RESULT_PATH = "/uio/hume/student-u01/steinboe/Documents/master/MasterThesis/results"
else:
    sys.exit("what?")

def inspectGenerations(solutions, generations):
    """
    input: RESULT_PATH
    solutions: list of which solutions to be found for each generation 
    generations: list of generations to view

    returns: data (list), each element represent a generation. 
            Each element is a tuple of info (dict) and solutions (list) 
    
    """
    data=[]
    for g in generations:
        endGen=g
        theGenDir=None
        for i in range(g+1):
            theFile = RESULT_PATH+'gen'+str(endGen)+'.json'
            try:
                theGenDir = json.load(open(theFile))
                break
            except FileNotFoundError:
                print("Generation ",endGen, "not found. Getting ", endGen-1, "instead")
                endGen-=1

        if theGenDir==None:
            sys.exit("Could not find generation "+str(g))
        data.append(getSolutions(theGenDir,solutions))

    return data

#def createEnvironment(config,worker_id):
#    print("Creating environment and sideChannel_M")
#    sideChannel_M = StringLogSideChannel("621f0a70-4f87-11ea-a6bf-784f4387d1f7") 
#    sideChannel_Config = StringLogSideChannel("621f0a70-4f87-11ea-a6bf-784f4387d1f6")
#    env = UnityEnvironment(file_name=BUILD_PATH, seed = config["UNITY_ENV_SEED"], side_channels = [sideChannel_M, sideChannel_Config], no_graphics=not config["GRAPHICS"], worker_id=worker_id)
#    env.reset()
#    return env, sideChannel_M
#
#def warmUpEnvironment(env, config, individual_ref, eval_func):
#    env.reset()
#    print("Warming up environemnt")
#    for i in range(2):
#        ind = individual_ref([config["EVAL_CNT"], config["EVAL_MORPH"], config["NUM_CONTROL_PARAMS"], config["NUM_MORPHOLOGY_PARAMS"]])
#        print(f"(warmup) fitness was {eval_func(env, sideChannel_M, ind, config, use_controller=False)}") 

def findLastGen(NumGen):
    """
    Input the number (int) of generation set in training,
    returns the actual number (int) of generations before ending
    """
    lastGen=NumGen
    for i in range(NumGen+1):
        theFile = RESULT_PATH+'gen'+str(lastGen)+'.json'
        try:
            open(theFile)
            print(theFile)

            return lastGen
        except FileNotFoundError:
            lastGen-=1

    sys.exit("Did not find any generations")


if __name__ == "__main__":
    howMuchLonger = 1 # how many times longer evaluation
    # for slow motion: increse resolution: will give a different fitness :(

    RESULT_PATH = askdirectory(initialdir=RESULT_PATH, title='Please select a directory')
    RESULT_PATH = RESULT_PATH+"/"
    config = json.load(open(RESULT_PATH+'config.json'))
    config["RESULT_PATH"]=RESULT_PATH
    config["BUILD_PATH"]=BUILD_PATH
    config["UNITY_ENV_SEED"]=0

    lastGen=findLastGen(config["N_GENERATIONS"])

    generations = [lastGen]
    solutions = [2,9,10,16,25] # oldResults: 13.12
    #solutions = [1, 10, 15, 35] #15.12.2021_18.57.12. Best dist: 35, Best stability: 1, God dist, dårlig stability: 15, litt dårligere: 10

    #generations = list(range(config["N_GENERATIONS"]))
    #solutions = list(range(config["POPULATION_SIZE"]//2))

    data = inspectGenerations(solutions, generations)
    
    #settings
    config["GRAPHICS"]=True
    if config["INDIVIDUAL"]=="WaveIndividual":
        indRef = WaveIndividual

    worker_id = 0

    # create and warmUp env:
    env, sideChannel_M = createEnvironment(config, worker_id)
    warmUpEnvironment(env, sideChannel_M, config, indRef, evaluate)

    config["MAX_N_STEPS_PER_EVALUATION"]=config["MAX_N_STEPS_PER_EVALUATION"]*howMuchLonger

    # Iterating through data:
    for g in range(len(generations)):
        genInfo=data[g][0]
        print("---------------------- Generation:",generations[g],"----------------------")
        for s in range(len(solutions)):

           
            print("Solution:",solutions[s])
            indData=data[g][1][s]
            indControlParams=indData[0]
            indMorphologyParams=indData[1]
            indFitness = indData[2]

            # todo! Må sjekke at vi evolvuerer morphology? eller vil den da baere få reset-verdi? Test det :)

            ind = indRef([config["EVAL_CNT"], config["EVAL_MORPH"], config["NUM_CONTROL_PARAMS"], config["NUM_MORPHOLOGY_PARAMS"]])
            ind.controlParams=indControlParams
            ind.morphologyParams=indMorphologyParams
            newFitness, stability1, stability2 = evaluate(env, sideChannel_M, ind, config)
            print("prevFitness: "+str(indFitness)+". New fitness: "+str(newFitness))

    
    env.close()
    

