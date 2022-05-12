import numpy as np
import time
from datetime import datetime
import sys
import multiprocessing
import json
from pathlib import Path
import argparse
import EvolutionaryAlgorithm
#from visualizeSolution import getSolution, getSolutions
#from WaveController import WaveController
#from Individuals import BaseIndividual
from Individual import WaveIndividual
from mlagents_envs.environment import UnityEnvironment
#from mlagents_envs.side_channel.side_channel import (
#    SideChannel,
#    IncomingMessage,
#    OutgoingMessage
#)
from mlagents_envs.base_env import (
    ActionTuple
)
from myCreator import creator
import platform
import random
#from tkinter.filedialog import askdirectory
#from tkinter import *


config = {
# evaluation settings
"MAX_N_STEPS_PER_EVALUATION" : 4+1,
"RESOLUTION" : 30, # nr of action for each step
# training parameters
"POPULATION_SIZE" :128, # 64
"N_GENERATIONS" : 250, # 1064
"MUTATION_PROB" : 0.4, # chance of a mutation to occur
"MUTATION_SIGMA" : 0.1, # sigma in gaussian distribution. # gjør den avhengig av generasjonen?
"CROSSOVER_PROB" : 0.3,
"RANDOM_INIT_PROB" : 0.01, 
"MUTATION_TYPE" : "gaussianAndRandomInit", ### "gaussianAndRandomInit" Or "gaussian"
#"PARENS_PORTION" : 1, # 0.5=50% of population is choosen to be parents
"EVAL_CNT" :True,
"EVAL_MORPH" : False, 
# num params
"NUM_CONTROL_PARAMS" : 15,
"NUM_MORPHOLOGY_PARAMS" : 0,
# robot properties
"MOTOR_STRENGT" : 0.7, # [-1,1]
"NUM_OF_JOINTS" : 12,
"MIN_LEG_LENGTH" : 0.2,
"MAX_LEG_LENGTH": 3,
"MIN_LEG_TRANS" : -0.2, # 
"MAX_LEG_TRANS" : 0.8, #  
"MIRROR_MORPH" : True,
# settings
"GRAPHICS" : False,
# multi processing
"MULTI_THREAD" : True,
#stopping criteria
"EPSILON" : 50,
"GEN_STUCK" : 0,
"GEN_STUCK_WHEN_CONVERGENCE" :100, 
"HAVE_CONVERGENCE": False,
# fitness-calculation
"SCALING_FACTOR" : 0.078,
# hypervolume
"HYPERVOLUME_REF" :(0,-50),
#seed
"SEED" : 123456, #todo None, # None during training. 
# co-evolutionary strategies
"CO_EVOLUTIONARY_STRATEGY" : 0,
"INIT_TRAINING_NUM_GEN" : 0,
#
"MORPHOLOGIES_TO_KEEP" : 2,
} 

if platform.system()=='Windows': 
    config["BUILD_PATH"]="C:\\Users\\stein\\Documents\\Unity\\builds\\windows\\Crawler"
    config["RESULT_PATH"]="C:/Users/stein/Documents/Unity/results/"
    config["NUM_CORES"] = multiprocessing.cpu_count()

elif platform.system()=='Linux':
    #config["BUILD_PATH"] ="/uio/hume/student-u01/steinboe/Documents/Master/MasterThesis/builds/linux/Crawler/Crawler.x86_64"
    #config["RESULT_PATH"] = "/uio/hume/student-u01/steinboe/Documents/Master/MasterThesis/resultsLinux/"
    #config["NUM_CORES"]=32 

    #ml-nodes
    ml_hpc=False #
    robin_hpc=False
    fox=True

    if ml_hpc:
        config["BUILD_PATH"] ="/itf-fi-ml/home/steinboe/MasterThesis/builds/linux/Crawler/Crawler.x86_64"
        config["RESULT_PATH"]="/itf-fi-ml/home/steinboe/MasterThesis/resultsLinux/"
        config["NUM_CORES"]=64
    # TODO: mÅ OGSÅ ENDRES LENGRE NEDE!! UNDER: startPretrainedMorphology
    elif robin_hpc:
    #hpc 
        config["BUILD_PATH"] ="/home/steinboe/MasterThesis/builds/linux/Crawler/Crawler.x86_64"
        config["RESULT_PATH"]="/home/steinboe/MasterThesis/resultsLinux/"
        config["NUM_CORES"]=128
    elif fox:
        config["BUILD_PATH"] ="/fp/homes01/u01/ec-steinboe/builds/linux/Crawler/Crawler.x86_64"
        config["RESULT_PATH"]="/fp/homes01/u01/ec-steinboe/resultsLinux/"
        config["NUM_CORES"]=128
else:
    sys.exit("what?")

config["OP_SYSTEM"]=platform.system()


# individual and control
INDIVIDUAL = WaveIndividual
config["INDIVIDUAL"]="WaveIndividual"

def evaluate(env, sideChannel_M, individual, config, use_controller : bool = True):
    if config["EVAL_MORPH"] and use_controller:
        stringMorph =individual.morphologyString(config)
        sideChannel_M.send_string(stringMorph)
    env.reset()
    ##for i in range(5):
    ##    print("sleeping")
    ##    time.sleep(1)
    
    individual_name = list(env._env_specs)[0]
    obs,other = env.get_steps(individual_name)
    env.step()
    env.step()
    env.step()
    ##for i in range(5):
    ##    print("sleeping2")
    ##    time.sleep(1)

    distanceFitness  = -1000000
    stabilityFitness = -1000000
    stabilityFitnessData=np.zeros((config["RESOLUTION"]*(config["MAX_N_STEPS_PER_EVALUATION"]-1),6))

    index=0
    if use_controller:
        action = np.random.rand(1,21) #np.full((1,20),MOTOR_STRENGT)# does not work lol. what why? stupid
        action[0,0]=0
        action[0,13:]=config["MOTOR_STRENGT"]
        for j in range(config["MAX_N_STEPS_PER_EVALUATION"]):
            for t in range(config["RESOLUTION"]):
                if j==1 and t==0: 
                    action[0,0]=1 # see onActionReceived in CrawlerAgent :) This is basically a flag telling unity to start evaluate

                obs,other = env.get_steps(individual_name) #
                sec = 0



                if (len(obs.agent_id)>0):
                    #rrr = individual.getController().createAction(t)
                    action[0,1:13] = individual.createAction(t/config["RESOLUTION"])
                    env.set_action_for_agent(individual_name,obs.agent_id,ActionTuple(action)) #
                    env.step()
                    #print("stepping")
                    if j>0:
                        #  first observation (when j==1 and t==0) is only zeros. Change c# code? or just remove first value?
                        stabilityFitnessData[index]=obs.obs[0][0][0:6]
                        index+=1
                else:
                    print("dette skjedde ikke nei. hmm")
                    # obs.obs - for stability and obs.reward for distance traveled
                    # one obs.obs for each value in resolution

        stabilityFitness, stability1, stability2 = calculateStabilityFitness(stabilityFitnessData, config)
        distanceFitness =obs.reward[0] # return the latest achieved distance. Given a call on RewardDistancedTraveled in crawlerAgent

    else:
        for j in range(20):#config["RESOLUTION"]*config["MAX_N_STEPS_PER_EVALUATION"]):
            obs,other = env.get_steps(individual_name)
            if (len(obs.agent_id)>0):

                action = np.random.rand(1,21)
                for i in range(len(action[0])):
                    action[0,i] = np.sin(j * 0.2) * 2
            
                env.set_action_for_agent(individual_name,obs.agent_id,ActionTuple(action))
                env.step()
                # make sure this is what you would like to do
            else:
                print("not")
        stability1=0 
        stability2=0
    #print("DistanceFit: {:<20} StabilityFit: {}".format(distanceFitness, stabilityFitness))
    return (distanceFitness,stabilityFitness), stability1, stability2

def calculateStabilityFitness(data, config):
    """
    input: data - numpy array
        each row is data from a step
        row[i] = [orientation difference x, orientation difference y, orientation difference z, 
                    velocity x, velocity y, velocity z]
    
    return fitness value based on stability
    """
    # : sjekk om data bare er null

    # : Har nå fart i et øyeblikk, og ikke akselerasjon. Men er det et probleme? Lik fart betyr jo lav akselerasjon 
    # : tid mellom hvert step kan varierer
    # 
    

    # orientation:
    #  take root mean square (RMS) of orientation (because it can contain both positive and negative values)
    # low rms of orientation - means low orientation changes 
    # Dont include z-axis here?
    rmsOrientation = np.sqrt(np.mean(data**2,axis=0))[:3] #  [:2] # exclude z-axis

    # velocity
    # vil ha: lavest mulig endring.
    # derfor: low std / low variance
    # want to use std (over variance) because that gives the same unit.
    stdVelocity = np.std(data, axis=0)[3:]
    
    # when adding: need to scale on of them. This is needed to make them both contribute equally to the fitnessvalue.

    # mention that this is inspired by tønnes?
    rmsO=np.sum(rmsOrientation)*config["SCALING_FACTOR"]
    stdV=np.sum(stdVelocity)
    fitnessStability=rmsO+stdV

    # negated
    return -fitnessStability, rmsO, stdV

def run(ea, startGen=0):
    try:
        config["DATA_PATH"]
    except KeyError:
        config["DATA_PATH"] = whereToSaveData(config)

    # Begin the evolution
    for g in range(startGen,config["N_GENERATIONS"]):
        print(f"-- Evaluating generation {g} --")
        #try:
        s1= time.time()
        genData, convergence = ea.step() 
        config["HAVE_CONVERGENCE"]=convergence
        s2=time.time()
        print("Eval time:",s2-s1)
        # add data to save-array stuff
        genData["info"]["generation"]=g
        genData["info"]["time"]=s2-s1
        genData["config"]=config

        saveDataJson(genData, config['DATA_PATH']+"gen"+str(g)+".json")
        
        """
        # co-evolutionary strategies:
        if config["CO_EVOLUTIONARY_STRATEGY"]==0:
            continue
        elif config["CO_EVOLUTIONARY_STRATEGY"]==1 and g==config["INIT_TRAINING_NUM_GEN"]-1:
            print("####################### TURNING ###########")
            # Init training is done (co-evolving), only cnt will evol from now on
            config["EVAL_MORPH"]=False
        elif config["CO_EVOLUTIONARY_STRATEGY"]==2 and g==config["INIT_TRAINING_NUM_GEN"]-1:
            print("####################### TURNING ###########")

            # Init training is done (co-evolving), only mor will evol from now on
            config["EVAL_CNT"]=False
        elif config["CO_EVOLUTIONARY_STRATEGY"]==3:
            if config["SWITCH_ON_CONVERGENCE"]:
                print("have convergence:", config["HAVE_CONVERGENCE"])
                if config["HAVE_CONVERGENCE"]:
                    # first switch, happens only at first convergence.
                    if config["EVAL_CNT"] and config["EVAL_MORPH"]:
                        print("Turning of morphology training")
                        config["EVAL_MORPH"]=False

                    # switch if convergence: (can happen many times)
                    else:
                        print("Switching")
                        config["EVAL_CNT"]= not config["EVAL_CNT"]
                        config["EVAL_MORPH"]= not config["EVAL_MORPH"]
                        config["HAVE_CONVERGENCE"]=False

        elif config["CO_EVOLUTIONARY_STRATEGY"]==4 and g==config["INIT_TRAINING_NUM_GEN"]-1:
            print("##### Choosing some morphologies and turning of morph eval #####")
            config["EVAL_MORPH"]=False
            config["PRE_TRAINED_MORPHOLOGIES"]=True
            ea.chooseMorphologies()
            # run the ea. (g = generation)
            config["EVAL_MORPH"]=False
        """


            
    print("Evolution is done")
    print("Ending processes and exiting")    
    
    if config["MULTI_THREAD"]:
        ea.endAllProcesses()
    else:
        ea.endSingleProcess()




def whereToSaveData(config):
    # creating dataPath
    now = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
    dataPath = "Results_" + now+"/"
    dataPath = config["RESULT_PATH"]+dataPath
    Path(dataPath).mkdir(parents=True, exist_ok=True)
    saveDataJson(config, dataPath+"config.json")
    return dataPath

def saveDataJson(data, dataPath):
    print(dataPath)
    with open(dataPath, 'w') as filename:
        json.dump(data, filename, indent=2)

def findLastGen(NumGen, resultPath):
    """
    Input the number (int) of generation set in training, and result path
    returns the actual number (int) of generations before ending
    (Note: same func as in visualiseSolution, but does not work correctly when imported)
    """
    lastGen=NumGen
    for i in range(NumGen):
        theFile = resultPath+'gen'+str(lastGen)+'.json'
        try:
            open(theFile)
            print(theFile)
            print("found:",lastGen)
            return lastGen
        except FileNotFoundError:
            lastGen-=1

    sys.exit("Did not find any generations")


def splitMorphologies(input):
    #genNum=input[0]
    #morphNum=input[1]

    numGen=int(input[0])
    numMorph=int(input[1])
    
    checkpoint=input[2]

    
    # setting the new config
    config = json.load(open(checkpoint+'/config.json'))
    
    # open last genfile:
    genData = json.load(open(checkpoint+"/"+"gen"+str(numGen)+".json"))
    # overrwriting the config for with the newest generation
    config = genData["config"]
    ea = EvolutionaryAlgorithm.EvolutionaryAlgorithm(config, evaluate, INDIVIDUAL, creator)#, CONTROL)
    morphParams = ea.findMorphologies( numMorph,genData)


    config["CURRENT_GENERATION"]=numGen
    config["PRETRAINED_MORPHOLOGIES"]=morphParams

    Path(checkpoint+"/subGen"+str(numGen)+"Morph"+str(numMorph)+"/").mkdir(parents=True, exist_ok=True)
    saveDataJson(config, checkpoint+"/subGen"+str(numGen)+"Morph"+str(numMorph)+"/morphologiesGen"+str(numGen)+".json")
   

def startFromCheckpoint():
    sys.exit("Does not work on HPC")

    root=Tk()
    global config
    checkpoint=askdirectory(initialdir=config["RESULT_PATH"], title='Please select a directory')
    # setting the new config
    print("check", checkpoint)
    config = json.load(open(checkpoint+'/config.json'))
    print(config)
    lastGen=findLastGen(config["N_GENERATIONS"], checkpoint+"/")-1
    print("last gen was:", lastGen)
    print("#########################################")
    
    # open last genfile:
    lastGenData = json.load(open(checkpoint+"/"+"gen"+str(lastGen)+".json"))
    # overrwriting the config for with the newest generation
    config = lastGenData["config"]
    
    ea = EvolutionaryAlgorithm.EvolutionaryAlgorithm(config, evaluate, INDIVIDUAL, creator)#, CONTROL)
    s1=time.time()
    ea.loadCheckpoint(lastGenData) 
    print("time:",time.time()-s1)
    # run the ea. (g = generation)
    run(ea, startGen=lastGen+1)
    print("Total time: ", time.time()-start)

def startFromCheckpointHPC(input):
    checkpoint = input[0]
    newGen = int(input[1])
    cores = int(input[2])
    global config
    

    # setting the new config
    print("checkpointHPC path:", checkpoint)
    config = json.load(open(checkpoint+'/config.json'))
    lastGen=findLastGen(config["N_GENERATIONS"], checkpoint+"/")-1
    print("last gen was:", lastGen)
    print("#########################################")
    
    # open last genfile:
    lastGenData = json.load(open(checkpoint+"/"+"gen"+str(lastGen)+".json"))
    # overrwriting the config for with the newest generation
    config = lastGenData["config"]
    config["N_GENERATIONS"]=newGen
    config["NUM_CORES"]=cores
    config["BATCH_SIZE"] = config["POPULATION_SIZE"]//config["NUM_CORES"]

    print(config)
    ea = EvolutionaryAlgorithm.EvolutionaryAlgorithm(config, evaluate, INDIVIDUAL, creator)#, CONTROL)
    ea.loadCheckpoint(lastGenData) 
    run(ea, startGen=lastGen+1)


def startPretrainedMorphology(input):
    # skal du ha nye hyperparamterer for denne treningen så må du sende det med etter --pretrainedMorphology path morphNum ....
    #--pretrainedMorphology 511 0 path  #--pretrainedMorphology gen morphologyNum path 
    if len(input)!=6 and len(input)!=10:
        sys.exit("--pretraindMorphology need 6 (or 10) params: lastGen morphologyNumber path popSize generations, cores, (mutProb, mutSigma, crossProb, initProb)")
        #                                                          0        1            2   3          4          5        6         7         8         9
    lastGen = int(input[0])
    morphologiNumber=int(input[1])
    checkpoint= input[2]

    #assert (lastGen==511 or lastGen==1023), "Generation to start from is not 511 or 1023, lastGen="+str(lastGen)

    global config
    # open last genfile:
    config = json.load(open(checkpoint+"/"+"morphologiesGen"+str(lastGen)+".json"))
    # overrwriting the config for with the newest generation

    #TODO: Endre for hpc eller ml-nodes:
    if ml_hpc:
        config["DATA_PATH"]="/itf-fi-ml"+config["DATA_PATH"]
        config["BUILD_PATH"]="/itf-fi-ml"+config["BUILD_PATH"]
        config["RESULT_PATH"]="/itf-fi-ml"+config["RESULT_PATH"]

    #config = genData["config"]
    print("old config:")
    print(config)
    # setting the new config
    config["MORPHOLOGI_NUMBER"]=morphologiNumber
    config["PRETRAINED_MORPHOLOGY"] = config["PRETRAINED_MORPHOLOGIES"][morphologiNumber]

    config["POPULATION_SIZE"]=int(input[3])
    config["N_GENERATIONS"]=int(input[4])
    if len(input)==10:
        config["MUTATION_PROB"] = int(input[6])
        config["MUTATION_SIGMA"] = int(input[7])
        config["CROSSOVER_PROB"] = int(input[8])
        config["RANDOM_INIT_PROB"] = int(input[9])

    config["NUM_CORES"]=int(input[5])
        
    config["BATCH_SIZE"] = config["POPULATION_SIZE"]//config["NUM_CORES"]

    # create dataPath 
    config["DATA_PATH"] = checkpoint+"/"+str(config["POPULATION_SIZE"])+"ind_"+str(config["N_GENERATIONS"])+"gen/morphology"+str(morphologiNumber)+"/"
    Path(config["DATA_PATH"]).mkdir(parents=True, exist_ok=True)

    ea = EvolutionaryAlgorithm.EvolutionaryAlgorithm(config, evaluate, INDIVIDUAL, creator)#, CONTROL)
    config["EVAL_MORPH"]=False
    print("new config")
    print(config)
    ea.loadMorphology() #bug: skjer også for ea.reset()
    saveDataJson(config, config["DATA_PATH"]+"config.json")
    run(ea, startGen=lastGen+1)


if __name__ == "__main__":
    start=time.time()
    # argument from program call:
    parser = argparse.ArgumentParser()
    parser.add_argument('popSize', metavar='popSize', type=int, help='Size of population (int)')
    parser.add_argument('generations', metavar='generations', type=int, help='Number of generations (int)')
    parser.add_argument('mutProb', metavar='mutProb', type=float, help='Mutation probability (float)')
    parser.add_argument('mutSigma', metavar='mutSigma', type=float, help='Mutationsigma (float)')
    parser.add_argument('crossProb', metavar='crossProb', type=float, help='Crossover probability (float)')
    parser.add_argument('initProb', metavar='initProb', type=float, help='Random init probability (float)')
    parser.add_argument('cores', metavar='cores', type=int, help='Number of cores to use')

    parser.add_argument('-cnt', dest='numCnt', type=int, help='Number of control parameters (15, 18 or 24), if any', default=0)
    parser.add_argument('-mor', dest='numMor', type=int, help='Number of morphology parameters (4), if any', default=0)
    parser.add_argument('-co', dest='co', type=int, help='Specify co-evolutionary strategy (0,1,2,3,4)', default=0)
    parser.add_argument('-initGen', dest='initGen', type=int, help='Number of init generations before switching training type', default=100)
    parser.add_argument('-', dest='initGen', type=int, help='Number of init generations before switching training type', default=100)
    parser.add_argument('--checkpoint', dest='checkpoint', action='store_true', default=False, help='Continue from checkpoint')

    parser.add_argument('--checkpointHPC', dest='checkpointHPC', type=str, nargs='+', help='Continue from checkpoint on HPC, needs path and new max-generation')
    parser.add_argument('--splitMorphologies', dest='splitMorphologies', type=str, nargs='+', help='Splits intNumMorph bodies from the front in generation intGen into seperate sub folders. Needs NumGen,NumMorph and path')
    parser.add_argument('--pretrainedMorphology', dest='pretrainedMorphology', type=str, nargs='+', help='Continue from a pretrained morphology. Input int decides which one')
     #--pretrainedMorphology 511 0 path  #--pretrainedMorphology gen morphologyNum path (path er: ...\Results_date_time\sub511\)

    args = parser.parse_args()

    if args.checkpoint:
        print("########### Starting from checkpoint ############")
        startFromCheckpoint()
        sys.exit()
    elif args.checkpointHPC:
        print("########### Starting from checkpoint HPC ############")
        startFromCheckpointHPC(args.checkpointHPC)
        sys.exit()
    elif args.pretrainedMorphology:
        print("######### Continue from pretrained morphologies ###########")
        startPretrainedMorphology(args.pretrainedMorphology)
        sys.exit()
    elif args.splitMorphologies:
        print("######### Splits the front into subfolders with different morphologies ###########")
        print(args.splitMorphologies)
        splitMorphologies(args.splitMorphologies)
        sys.exit()
    else:
        print("############ Starting new training #######")


    config["POPULATION_SIZE"] = args.popSize  #64 # 64
    config["N_GENERATIONS"] = args.generations  #50 # 1064
    config["MUTATION_PROB"] = args.mutProb  #0.4 # chance of a mutation to occur
    config["MUTATION_SIGMA"] = args.mutSigma  #0.1
    config["CROSSOVER_PROB"] = args.crossProb  #0.1
    config["RANDOM_INIT_PROB"] = args.initProb  #0.1
    config["CO_EVOLUTIONARY_STRATEGY"] = args.co # 0
    config["INIT_TRAINING_NUM_GEN"]=args.initGen # default 100
    # Co-evolutionary strategies:   0: default co-evolution (can train only body og cnt also)
    #                               1: First co-evol, then only control
    #                               2: First co-evol, then only morphology??
    #                               3: First co-evol, then only control, then only morphology, keep switching?
    config["NUM_CORES"]=args.cores


    if args.numCnt==0 and args.numMor==0:
        sys.exit("Need to specify training for either cnt of morph")
    
    config["EVAL_CNT"] = bool(args.numCnt)
    config["EVAL_MORPH"] = bool(args.numMor)
    config["NUM_CONTROL_PARAMS"] = args.numCnt
    config["NUM_MORPHOLOGY_PARAMS"] = args.numMor
    
    if config["INIT_TRAINING_NUM_GEN"]==1000:
        config["SWITCH_ON_CONVERGENCE"]=True



    # checks before training. Multiprocessing
    if config["MULTI_THREAD"]:
        config["GRAPHICS"]=False
        #if config["POPULATION_SIZE"] % config["NUM_CORES"] !=0:
            #sys.exit("Population size is not divisible by 8")
            # set correct batchSize. One batch for each core
        config["BATCH_SIZE"] = config["POPULATION_SIZE"]//config["NUM_CORES"]
        print("Cores:",config["NUM_CORES"], "Batch size:", config["BATCH_SIZE"])
    else:
        #no multiprocess
        config["NUM_CORES"]=1

    #
    print("Starting training with this configuration:")
    print(config)

    # Encapsulated the EA in an object where we pass references to the evaluation function, the individual and the controller 
    ea = EvolutionaryAlgorithm.EvolutionaryAlgorithm(config, evaluate, INDIVIDUAL, creator)#, CONTROL)
    s1=time.time()
    ea.reset(config["POPULATION_SIZE"]) 
    print("time:",time.time()-s1)
    # run the ea. (g = generation)
    run(ea)
    print("Total time: ", time.time()-start)
    
