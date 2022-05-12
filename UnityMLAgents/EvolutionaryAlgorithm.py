from multiprocessing import Pool
import multiprocessing
import os
import sys
from turtle import distance
from deap import base
#from deap import creator
from deap import tools
import random
from mlagents_envs.environment import UnityEnvironment
from itertools import chain
from functools import partial
import numpy as np
from stringLogSideChannel import StringLogSideChannel
import time
from mlagents_envs.exception import UnityTimeOutException, UnityWorkerInUseException
from itertools import repeat

def getSolution(data, solutionNr=0, distanceLim=None, stabilityLim=None):
    # solutionNR = 0: the best solution. equal popSize-1: the worst solution
    solution = data["Eval"][solutionNr]
    individual = solution["Individual"]
    controlParams = individual["controlParameters"]
    morphologyParams = individual["morphology Parameters"]
    
    fitness = solution["Fitness"]
    fitnessValues = fitness["Fitness"]

    if stabilityLim!=None:
        if abs(stabilityLim)<abs(fitnessValues[1]):
            return None



    return (controlParams, morphologyParams, fitnessValues)

def getSolutions(data, solutions=[0], distanceLim=None, stabilityLim=None):
    """
    dir
    solution: list specifing which solutions to get. Eks: [0, 5]. The best and the 6. best
    return value: info of run, and a list containing tuples of controlParameters and fitness
    of specified solutions
    """
    
    individuals = []
    for i in range(len(solutions)):
        solutionData = getSolution(data,solutions[i], distanceLim, stabilityLim)
        if solutionData!=None:
            individuals.append(solutionData)
    try:
        conf =data["config"]
    except KeyError:
        conf=None
    return (data["info"], individuals, conf)

def custom_mutation(population, type, mutation_rate, sigma, randomInitProb, mutateControl=True, mutateMorphology=False):
    #print("custom_muation. mutateCnt: "+ str(mutateControl) +". mutateMor: "+str(mutateMorphology))
    for ind in population:
        try: 
            #ind.getController().mutate(mutation_rate, sigma, mutateControl, mutateMorphology)
            ind.mutate(type, mutation_rate, sigma, randomInitProb, mutateControl, mutateMorphology)
        except:
            raise ValueError("Could not mutat individual")
        resetInd(ind)
    return population

def custom_crossover(parents, crossover_prob, recombControl=True, recombMorphology=False):
    #print("custom_recomb. recombCnt: "+ str(recombControl) +". recombMor: "+str(recombMorphology))

    for ind1, ind2 in zip(parents[::2], parents[1::2]):
        # TODO: sorted?
        try: 
            #ind1.getController().crossover(ind2, recombControl, recombMorphology)
            ind1.crossover(ind2, crossover_prob, recombControl, recombMorphology)
        except:
            raise ValueError("Could not do crossover on individual")
        # resetting fitness and evalDone flag
        resetInd(ind1) 
        resetInd(ind2) 
    return parents

def resetInd(ind):
    ind.evalDone=0       # resetting fitness and evalDone flag
    ind.fitness.values=(0,0)

def controlMorphology(evolvCnt , evolvMorph, numCntParams, numMorParams, pretrained_morphology=None):
    return [evolvCnt, evolvMorph,numCntParams, numMorParams, pretrained_morphology]

class EvolutionaryAlgorithm:
    def __init__(self, config, evaluation_function, individual_reference, creator):
        self.individual_reference=individual_reference
        self.evaluation_function = evaluation_function 
        self.config =config
        self.singleCoreEnv = None
        self.singleCoreSideChannel_M = None
        self.singleCoreSideChannel_Config = None
        self.config["GEN_STUCK"] = 0
        self.config["PREV_HYPERVOLUME"] = 0.0

        
        # seed. For testing
        if config["SEED"] !=None:
            random.seed(config["SEED"])
            np.random.seed(config["SEED"])
            print("Setting seed :)  :",random.random())
            config["UNITY_ENV_SEED"] = config["SEED"]
        config["UNITY_ENV_SEED"]=0


        # multiprocessing pool and queue
        if config["MULTI_THREAD"]:
            self.pool = multiprocessing.Pool(processes=config["NUM_CORES"])

        # toolbox
        self.toolbox = base.Toolbox()        
        self.toolbox.register("cntMorph_generator", controlMorphology, self.config["EVAL_CNT"], self.config["EVAL_MORPH"],\
            self.config["NUM_CONTROL_PARAMS"], self.config["NUM_MORPHOLOGY_PARAMS"])
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.cntMorph_generator)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("evaluate",self.evaluation_function)
        self.toolbox.register("recombination", custom_crossover, crossover_prob=config["CROSSOVER_PROB"]) 
        self.toolbox.register("mutation", custom_mutation, type=config["MUTATION_TYPE"], \
            mutation_rate=self.config["MUTATION_PROB"], sigma=self.config["MUTATION_SIGMA"], \
            randomInitProb=config["RANDOM_INIT_PROB"])
        self.toolbox.register("parentSelection", tools.selTournamentDCD)
        self.toolbox.register("survivalSelection", tools.selNSGA2)
        
        print("INIT, evalMorph: ",self.config["EVAL_MORPH"])

    def step(self):

        # init - evaluation
        # parent selection, recomb, mutation, evaluation, survival selection 

        # parent selection # change order?
        offspring = self.toolbox.parentSelection(self.pop, len(self.pop)) # round(len(self.pop)*self.config["PARENS_PORTION"])) # av self.pop

        offspring = [self.toolbox.clone(ind) for ind in offspring]

        # recomb/crossover
        offspring = self.toolbox.recombination(offspring, recombControl=self.config["EVAL_CNT"], recombMorphology=self.config["EVAL_MORPH"])
        
        # mutation # endrer selve individene
        #print("config:"+str(self.config["EVAL_MORPH"])) # todo: fjern denne linjen
        offspring = self.toolbox.mutation(offspring, mutateControl=self.config["EVAL_CNT"], mutateMorphology=self.config["EVAL_MORPH"])

        # evaluation
        # Evaluate the new population (evaluating self.pop)
        # todo: only evaluate individuals with evalDone = 0
        offspring = self.evaluatePop(offspring)

        #Survival selection
        self.pop = self.toolbox.survivalSelection(self.pop + offspring, self.config["POPULATION_SIZE"])

        return self.evaluateResults() # ser bare på self.pop

    def loadMorphology(self):
        self.pop = self.toolbox.population(n=self.config["POPULATION_SIZE"])
        for s in range(self.config["POPULATION_SIZE"]):
            self.pop[s].morphologyParams=self.config["PRETRAINED_MORPHOLOGY"]
            self.pop[s].fitness.values=(-10000,-10000)

         # evaluate the first individuals
        self.pop =self.evaluatePop(self.pop)
        # This is just to assign the crowding distance to the individuals # no actual selection is done. # "Having the size of individuals equals to k will have no effect other than sorting the population according to their front rank."
        self.pop = self.toolbox.survivalSelection(self.pop, len(self.pop))

    def loadCheckpoint(self, checkpointData, pretrainedMorphology=None):
        
        checkpointData = getSolutions(checkpointData, list(range(self.config["POPULATION_SIZE"])))

        self.pop = self.toolbox.population(n=self.config["POPULATION_SIZE"])
        for s in range(self.config["POPULATION_SIZE"]):
            indData=checkpointData[1][s]
            indControlParams=indData[0]
            indMorphologyParams=indData[1]
            #indFitness = indData[2]

            self.pop[s].controlParams=indControlParams
            if pretrainedMorphology==None:
                self.pop[s].morphologyParams=indMorphologyParams
            else: 
                self.pop[s].morphologyParams=pretrainedMorphology
                
            self.pop[s].fitness.values=(-10000,-10000)
            
        # NOE MER?? data fra info?
        # counters ovs..

         # evaluate the first individuals
        self.pop =self.evaluatePop(self.pop)
        # This is just to assign the crowding distance to the individuals # no actual selection is done. # "Having the size of individuals equals to k will have no effect other than sorting the population according to their front rank."
        self.pop = self.toolbox.survivalSelection(self.pop, len(self.pop))

    def findMorphologies(self, numMorph, checkpointData=None):
        if checkpointData!=None:
            self.loadCheckpoint(checkpointData)

        # TODO: find all in front
        paretoFront = tools.sortNondominated(self.pop, len(self.pop), first_front_only=True)[0]
        #indWithMorphToKeep = self.toolbox.survivalSelection(self.pop, numMorph)
        print("sorting")
        paretoFront.sort(key=lambda x: x.fitness.values[1], reverse=True)
        # call it allFitnessValues
        print("sorted")
        maxDistance = paretoFront[-1].fitness.values[1]

        # TODO: pick out individuals based on distance between fitness values
        # Find max fitness2 (distance)
        # Divide range in 8 points 
        valueList=[]
        for i in range(numMorph):
            valueList.append((maxDistance/(numMorph-1))*i)

        indWithMorphToKeep=[]
        for value in valueList:
            indWithMorphToKeep.append(min(paretoFront, key=lambda x:abs(x.fitness.values[1]-value)))
        
        #
        # find de tilhørende individene til fitness values.

        #returner disse morfologi parameterne
        return [ind.morphologyParams for ind in indWithMorphToKeep], [ind.fitness.values for ind in indWithMorphToKeep]

    def chooseMorphologies(self, checkpointData=None):
        morphToKeep = self.findMorphologies(checkpointData, self.config["MORPHOLOGIES_TO_KEEP"])

        newPop = self.toolbox.population(n=self.config["POPULATION_SIZE"])
        for i in range(self.config["POPULATION_SIZE"]):
            ind = newPop[i]
            ind.morphologyParams=morphToKeep[i%self.config["MORPHOLOGIES_TO_KEEP"]]

        self.pop =self.evaluatePop(self.pop)
        # This is just to assign the crowding distance to the individuals # no actual selection is done. # "Having the size of individuals equals to k will have no effect other than sorting the population according to their front rank."
        self.pop = self.toolbox.survivalSelection(self.pop, len(self.pop))

    def reset(self, population_size):
        # is actually init, but ok
        self.pop = self.toolbox.population(n=population_size)
        # evaluate the first individuals
        self.pop =self.evaluatePop(self.pop)
        # This is just to assign the crowding distance to the individuals # no actual selection is done. # "Having the size of individuals equals to k will have no effect other than sorting the population according to their front rank."
        self.pop = self.toolbox.survivalSelection(self.pop, len(self.pop))

    def endAllProcesses(self):
        print("Shutting down all processes")
        # TODO: call env.close() for alle envs

        # prevent adding anything more to the process pool and wait for all processes to finish
        self.pool.terminate()
        print("Ja blir denne egentlig avslutten???")
        self.pool.join()
        print("Jada faktisk")     
    
    def endSingleProcess(self):
        print("Avslutt!")
        self.singleCoreEnv.close()

    def evaluatePop(self, popToEval):
        if self.config["MULTI_THREAD"]:
            # do multiprocess evaluation of population
            # popsize is divisible with 8
            data=[]
            for i in range(self.config["NUM_CORES"]):
                popBatch = popToEval[i*self.config["BATCH_SIZE"] : (i+1)*self.config["BATCH_SIZE"]]
                #for ind in popBatch:
                #    print(ind.controlParams)
                data.append(popBatch)
                # eventuelt legg in batch her og sjekk at popToEval blir endret.
            #outData = self.pool.map(partial \
            #    (process_main, config=self.config, ind_ref=self.individual_reference, eval_func=self.evaluation_function) \
            #    , data)
            outData = self.pool.starmap(process_main, zip(data, repeat(self.config), repeat(self.individual_reference), repeat(self.evaluation_function)))
            # unnesting the nested list: 
            outData = list(chain.from_iterable(outData))


        else: # not multiprocessing
            if self.singleCoreEnv ==None:
                self.singleCoreSideChannel_M = StringLogSideChannel("621f0a70-4f87-11ea-a6bf-784f4387d1f7")
                self.singleCoreSideChannel_Config = StringLogSideChannel("621f0a70-4f87-11ea-a6bf-784f4387d1f6")
                self.singleCoreEnv = UnityEnvironment(file_name=self.config["BUILD_PATH"], \
                    seed = self.config["UNITY_ENV_SEED"], side_channels = [self.singleCoreSideChannel_M, self.singleCoreSideChannel_Config],  \
                    no_graphics=not self.config["GRAPHICS"], worker_id=0)
                # warmUp
                warmUpEnvironment(self.singleCoreEnv, self.singleCoreSideChannel_M, self.config, self.individual_reference, self.evaluation_function) 
            for ind in popToEval:
                if not ind.evalDone:
                    ind.fitness.values, ind.stability1, ind.stability2 = self.toolbox.evaluate(self.singleCoreEnv, self.singleCoreSideChannel_M, ind, self.config)
                    ind.evalDone=1
            outData=popToEval

        return outData

    def evaluateResults(self):
        # Gather all the fitnesses in one list and print the stats. Find the best solutions so far

        fits=[]
        bestFitDist=-1000000
        bestFitStability=-1000000
        #pointSet=[ind.fitness.values for ind in self.pop]
        #bestSolution=None
        for ind in self.pop:
            # todo: change to ind.fitness.values when multiobjective
            fits.append(ind.fitness.values)
            if ind.fitness.values[0]>bestFitDist:
                bestFitDist=ind.fitness.values[0]
            if ind.fitness.values[1]>bestFitStability:
                bestFitStability=ind.fitness.values[1]
                #bestSolution=copy.copy(ind) 

        distFits = [x[0] for x in fits]
        stabilityFits = [x[1] for x in fits]        

        length = len(self.pop)
        meanDist = sum(distFits) / length
        sumDist = sum(x*x for x in distFits)
        stdDist = abs(sumDist / length - meanDist**2)**0.5
        worstFitDist = min(distFits)

        meanStability = sum(stabilityFits) / length
        sumStability = sum(x*x for x in stabilityFits)
        stdStability = abs(sumStability / length - meanStability**2)**0.5
        worstFitStability = min(stabilityFits)
        #bestFit = max(fits)
        divCnt, divMor =self.diversityMeasure()

        # create data_dict
        data={}
        data["info"]={
        #distance
        "bestFitDist" : bestFitDist, 
        "worstFitDist" : worstFitDist, 
        "meanDist" : meanDist, 
        "stdDist" : stdDist,
        # stability
        "bestFitStability" : bestFitStability, 
        "worstFitStability" : worstFitStability, 
        "meanStability" : meanStability, 
        "stdStability" : stdStability,
        "diversityInControlParams" : divCnt,
        "diversityInMorphologyParams" : divMor,
        }
    


        paretoFront = tools.sortNondominated(self.pop, len(self.pop), first_front_only=True)[0]
        pointsetParetoF = [ind.fitness.values for ind in paretoFront]
        sortedPointsetParetoF = sorted(pointsetParetoF, key=lambda x: x[0])

        hypervolume = self.hypervolume(self.config["HYPERVOLUME_REF"],sortedPointsetParetoF)
        
        print("\n")
        print("        DistanceFit:                 StabilityFit: ")
        print("  Max   {:<28} {} ".format(bestFitDist, bestFitStability))
        print("  Min   {:<28} {} ".format(worstFitDist, worstFitStability))
        print("  Avg   {:<28} {} ".format(meanDist, meanStability))
        print("  Std   {:<28} {} ".format(stdDist, stdStability))
        print("  Diversity control", divCnt)
        print("  Diversity morphology", divMor)        
        print("  Hypervolume:", hypervolume)
        print("\n")

        data["info"]["Hypervolume"]=hypervolume
        data["info"]["ParetoFront"]=sortedPointsetParetoF
        
        
        # stop criteria:
        convergence = False
        if hypervolume < self.config["PREV_HYPERVOLUME"]+self.config["EPSILON"]:
            self.config["GEN_STUCK"]+=1
            print("Best solution not improved more then epsilon-value for: "+ str(self.config["GEN_STUCK"])+" generation(s) in a row")
        else:
            self.config["GEN_STUCK"] = 0
            self.config["PREV_HYPERVOLUME"]=hypervolume
        try:
            if self.config["GEN_STUCK"]==self.config["GEN_STUCK_WHEN_CONVERGENCE"]:
                # we have convergence for to long
                convergence=True
                print("Setter convergence")
                self.config["GEN_STUCK"]=0
        except KeyError:
            # not all pretrained files has this, but it is not neeede atm either
            pass


        # append data for each individual
        data["Eval"]=[]
        for ind in self.pop:
            subDict = {
            "Individual":{
                "controlParameters":ind.controlParams,
                "morphology Parameters": ind.morphologyParams,
                "stability": [ind.stability1, ind.stability2]
            },
            "Fitness":{
                "Fitness":ind.fitness.values
            }
            }
            data["Eval"].append(subDict)

        return data,convergence #bestSolution

    def area(self,a,b):
        c=(b[0]-a[0], b[1]-a[1])
        return c[0]*c[1]

    def hypervolume(self,ref, pointset):
        """
        Calculating hypervolume
        """
        sum=0
        for i in range(len(pointset)):
            sum+=self.area(ref,pointset[i])
            ref=(pointset[i][0],ref[1])
        return sum

    def diversityMeasure(self):
        """
        simple diversity measure between control/morph parameters in this generation
        Sum the euclidean distance between all control/morph parameters
        """

        # makes numpy array with parameters
        cntNumpy = np.zeros((self.config["POPULATION_SIZE"],self.config["NUM_CONTROL_PARAMS"]))
        morNumpy = np.zeros((self.config["POPULATION_SIZE"],self.config["NUM_MORPHOLOGY_PARAMS"]))
        for i in range(self.config["POPULATION_SIZE"]):
            cntNumpy[i]=self.pop[i].controlParams
            morNumpy[i]=self.pop[i].morphologyParams

        totalDistCnt=0
        totalDistMor=0
        numCalulations=0
        for i in range(self.config["POPULATION_SIZE"]):
            for j in range(self.config["POPULATION_SIZE"]):
                if i!=j:
                    numCalulations+=1
                    totalDistCnt+=np.linalg.norm(cntNumpy[i]-cntNumpy[j])
                    totalDistMor+=np.linalg.norm(morNumpy[i]-morNumpy[j])

        return totalDistCnt/numCalulations, totalDistMor/numCalulations

def process_main(batch, config, ind_ref, eval_func):
    #print(os.getpid(),"working")
    try:
        e = env
    except NameError:
        id = int((((time.time()%1)*1000000) *os.getpid())%10000)
        declareEnv(config, ind_ref, eval_func, worker_id=id)

    # do the job
    # if item is of correct type: evaluate this batch
    if type(batch)==list and type(batch[0]==config["INDIVIDUAL"]):
        for ind in batch:
            ind.fitness.values, ind.stability1, ind.stability2 =eval_func(env,sideChannel_M, ind, config)
            ind.evalDone=1
    else:
        sys.exit("Unknown data type in queue:", type(batch))
    
    return batch

def declareEnv(config, ind_ref, eval_func, worker_id):
    global env
    global sideChannel_M
    env, sideChannel_M = createEnvironment(config, worker_id)
    warmUpEnvironment(env, sideChannel_M, config, ind_ref, eval_func)

def createEnvironment(config,worker_id):
    print("Creating environment and sideChannel_M")
    sideChannel_M = StringLogSideChannel("621f0a70-4f87-11ea-a6bf-784f4387d1f7")
    sideChannel_Config = StringLogSideChannel("621f0a70-4f87-11ea-a6bf-784f4387d1f6")
    done =False
    counter = 0
    while not done:
        try:
            env = UnityEnvironment(file_name=config["BUILD_PATH"], seed = config["UNITY_ENV_SEED"], side_channels = [sideChannel_M, sideChannel_Config], no_graphics=not config["GRAPHICS"], worker_id=worker_id)
            done=True
        except UnityWorkerInUseException:
            worker_id+=1
            counter+=1
            if counter >10:
                done=True
        except UnityTimeOutException:
            print("UnityTimeOutException, prøver igjen")
            counter+=1
            if counter >10:
                done=True
    env.reset()

    # TODO send config string
    return env, sideChannel_M

def warmUpEnvironment(env, sideChannel_M, config, individual_ref, eval_func):
    
    for i in range(2):
        ind = individual_ref([config["EVAL_CNT"], config["EVAL_MORPH"], config["NUM_CONTROL_PARAMS"], config["NUM_MORPHOLOGY_PARAMS"]])
        print(f"(warmup) fitness was{eval_func(env, sideChannel_M, ind, config, use_controller=False)[0]}") 

def configString(config):
    """Sends a string of config settings to unity
    Input: config file
    Output: String with relevante values
    """
