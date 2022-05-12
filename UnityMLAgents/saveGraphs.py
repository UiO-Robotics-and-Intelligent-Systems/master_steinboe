import json
from tkinter.filedialog import askdirectory
import sys
from EvolutionaryAlgorithm import getSolutions, getSolution 
import os
import numpy as np
import platform
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from tkinter import *
import random
import time
import scipy.stats as st
import re
from statsmodels.nonparametric.smoothers_lowess import lowess as  sm_lowess
import statsmodels.api as sm
import pandas as pd
import seaborn as sns
from scipy.stats import spearmanr
from scipy.stats import pearsonr

plt.rc('font', size=18) 


random.seed(98765432) # only for colors

testing = False #todo: fjern    
plotConfig ={
    "EVAL_TIME" : 12,
    "ONLY_RUNDATA" : True,
    "OVERWRITE_RUNDATA":False,
    "NO_TITLE" : True,
    "NO_LEGEND" : True,
    "CHOOSE_DIR": False,
    "VIEW_GRAPH" :False,
    "RESULTS_ORIGINAL": False,  
    "RESULTS_ARCHIVE" : True,
    "EACH_SUB_FOLDER" : False,
    "DIVERSITY2" : True, 
    "PLOT_EACH_RUN": True,
    "DIVERSITY2_STEP":1024,
    "COLOR_ARRAY" : np.zeros((24,3)),
    "NUM_CONTROL_PARAMS" : 18,
    "NUM_MORPHOLOGY_PARAMS" : 6,

    "STABILITY_LIM" : None,
    "DISTANCE_LIM" : None,

    "GENERATIONS" : 4096, # TODO! 
    "POP_SIZE" : 256,
}

#if testing:
    #plotConfig["GENERATIONS"]=80

for i in range(24):
        plotConfig["COLOR_ARRAY"][i]=np.array([random.random(), random.random(), random.random()])

plotConfig["COLOR_ARRAY"]=np.array(
[[0.3809753,  0.08503984, 0.67345867],
 [0.88842423, 0.15377358, 0.8969029 ],
 [0.8, 0.8, 0],
 [0.99717745, 0.79783645, 0.85211819],
[0.34745665, 0.18011587, 0.26053   ],
 [0, 0, 1],
 [0.95915235, 0.70937606, 0.10208488],
 [0.05855674, 0.51210808, 0.13489599],
 [0.1, 0.1, 0.1],
 [0.89057299, 0.41509111, 0.26435728],
[0.38262577, 0.32875468, 0.02926836],
 [0.54363148, 0.63738221, 0.63169754],
 [0, 1, 1],
 [0.02649979, 0.76141652, 0.41049721],
 [0.9318808,  0.21475345, 0.52003784],
 [0.99, 0.5,  0],
 [0.63249594, 0.88869362, 0.4661602 ],
 [0.66572503, 0.44844524, 0.88258502],
 [0.60815189, 0.16430778, 0.94804337],
 [0.34450163, 0.56811463, 0.55069991],
 [0.62567043, 0.82708938, 0.13250081],
 [0.19600494, 0.24236123, 0.82495919],
 [0.71106506, 0.68460949, 0.93399185],
 [0.40757718, 0.4483467,  0.43437362],
 [0.37539834, 0.92799112, 0.50589176]])

fig = plt.figure()
ax = fig.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

print(plotConfig["COLOR_ARRAY"])

print(plotConfig["COLOR_ARRAY"].shape)



if platform.system()=='Windows': 
    plotConfig["RESULTS_PATH_ORIGINAL"]="C:/Users/stein/Documents/Unity/results/"
    plotConfig["RESULTS_PATH_ARCHIVE"]="C:/Users/stein/Documents/Unity/resultsArchive/"
elif platform.system()=='Linux':
    plotConfig["RESULTS_PATH_ORIGINAL"] = "/uio/hume/student-u01/steinboe/Documents/master/MasterThesis/results"
else:
    sys.exit("what?")

def saveDataJson(data, dataPath):
    print(dataPath)
    with open(dataPath, 'w') as filename:
        json.dump(data, filename, indent=2)

def findLastGen(resultPath):
    """
    Input the number (int) of generation set in training, and result path
    returns the actual number (int) of generations before ending
    (Note: same func as in visualiseSolution, but does not work correctly when imported)
    """
    NumGen=8192 # kanskje øk for sikkerhetsskyld

    print(NumGen)
    lastGen=NumGen
    for i in range(NumGen):
        theFile = resultPath+'gen'+str(lastGen)+'.json'
        try:
            f=open(theFile)
            f.close()
            print("found:",lastGen)
            return lastGen
        except FileNotFoundError:
            lastGen-=1

    sys.exit("Did not find any generations")

def inspectGenerations(solutions, generations, resultPath):
    """
    input: resultPath
    solutions: list of which solutions to be found for each generation 
    generations: list of generations to view

    returns: data (list), each element represent a generation. 
            Each element is a tuple of info (dict), solutions (list), and config (dict) (config could be None) 
    (Note: same func as in visualiseSolution, but does not work correctly when imported)
    """
    data=[]
    for g in generations:
        endGen=g
        theGenDir=None
        for i in range(g+1):
            theFile = resultPath+'gen'+str(endGen)+'.json'
            try:
                print("open:", theFile)
                f=open(theFile)
                theGenDir = json.load(f)
                f.close()
                break
            except FileNotFoundError:
                print("Generation ",endGen, "not found. Getting ", endGen-1, "instead")
                endGen-=1

        if theGenDir==None:
            sys.exit("Could not find generation "+str(g))
        data.append(getSolutions(theGenDir,solutions,stabilityLim=plotConfig["STABILITY_LIM"]))

    return data

def extractGenInfo(generationInfo, dataName):
    """
    input: generationInfo is a list of the "info" dict for each generation
    dataName is the string we want to extract from each info-dict

    returns a list with this dataName-value (float) for each generation
    """
    dataList = []
    for gInfo in generationInfo:
        dataList.append(gInfo[dataName])
    return dataList


def saveAndClose(location, show=False):

    plt.tight_layout()
    plt.savefig(location,dpi=300)
    #if show:
    #    plt.show()
    plt.close()
    fig = plt.figure()
    ax = fig.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

def bestMeanWorst(allGenerations, generationInfo, folder, plotConfig):
    ### Best, mean and worst for one training ###
    print("Making best mean worst graph")
    name="Distance, Best-, mean- and worst fitness measure"
    bestFits=extractGenInfo(generationInfo, dataName="bestFitDist")
    mean=extractGenInfo(generationInfo, dataName="meanDist")
    worstFits=extractGenInfo(generationInfo, dataName="worstFitDist")
    if plotConfig["PLOT_EACH_RUN"]:
        plt.plot(allGenerations, bestFits, linewidth=0.8)
        plt.plot(allGenerations, mean, linewidth=0.8)
        plt.plot(allGenerations, worstFits, linewidth=0.8)
        if not plotConfig["NO_LEGEND"]:
            plt.legend(["bestFitDist", "meanDist", "worstFitDist"],loc='center left', bbox_to_anchor=(1, 0.5),fontsize='x-small')
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.ylim(0,55)
        if not plotConfig["NO_TITLE"]:
            plt.title(name)
        saveAndClose(plotConfig["RESULT_PATH"]+folder+name, show=plotConfig["VIEW_GRAPH"])
    return bestFits, mean, worstFits
    ############################################################

def stds(allGenerations, generationInfo, folder, plotConfig):
    print("Making std")
    name="Std in fitness"
    stds=extractGenInfo(generationInfo, dataName="stdDist")
    stds=extractGenInfo(generationInfo, dataName="stdStability")
    if plotConfig["PLOT_EACH_RUN"]:
        plt.plot(allGenerations, stds, linewidth=0.8) 
        plt.plot(allGenerations, stds, linewidth=0.8)   
        if not plotConfig["NO_LEGEND"]:
            plt.legend(["stdDist", "stdStability"],loc='center left', bbox_to_anchor=(1, 0.5),fontsize='x-small')
        plt.xlabel("Generation")
        plt.ylabel("")  
        plt.ylim(1,4)
        if not plotConfig["NO_TITLE"]:
            plt.title(name)
        saveAndClose(plotConfig["RESULT_PATH"]+folder+name, show=plotConfig["VIEW_GRAPH"])
    ############################################################
    return stds

def plotColorName(colorsCnt, colorsMor, folder, plotConfig):
    name = "colorNames"
    for i in range(len(colorsCnt)):
        plt.scatter(i,0,c=colorsCnt[i], label=i)
    
    for i in range(len(colorsMor)):
        plt.scatter(i,1,c=colorsCnt[i], label=i)

    if not plotConfig["NO_TITLE"]:
        plt.title(name)
    saveAndClose(plotConfig["RESULT_PATH"]+folder+name, show=plotConfig["VIEW_GRAPH"])


def diversity3(data, allGenerations, folder, plotConfig):
    print("Making diversity3")

    morParams = plotConfig["NUM_CONTROL_PARAMS"]#len(data[0][1][0][1])
    cntParams = plotConfig["NUM_MORPHOLOGY_PARAMS"]#18#len(data[0][1][0][0])

    colorsCnt=plotConfig["COLOR_ARRAY"][:cntParams,:]
    colorsMor=plotConfig["COLOR_ARRAY"][:morParams,:]

    #plotColorName(colorsCnt, colorsMor, folder, plotConfig)

    for g in range(0,len(allGenerations)+1,step):
        if g==len(allGenerations): g=len(allGenerations)-1
        nameMorph = "Diversity in morphology params, gen"+str(g)
        nameCnt = "Diversity in control params, gen"+str(g)
        individualInfo = data[g][1]
        # individualInfo: list? of individuals. Dvs individualinfo[i] = ind_i. ind_i[0]=list of cntParams, ind_i[1]=morph params, ind_i[2]=fitness [distance, stability]
        individualInfo = individualInfo.copy()
        individualInfo.sort(key=lambda x: x[2][0], reverse=False)

        individualInfo = np.array(individualInfo)
        
        ######
        Cntparams0 = individualInfo[:,0,0] 
        MorParams0 = individualInfo[:,1,0]
        distance = individualInfo[:,2,0] # same for all params. Only different for each individual
        ######
        for i in range(len(individualInfo)):
            cnt= individualInfo[i][0]
            #height=[i]*len(cnt)
            height = [individualInfo[i][2][0]/plotConfig["EVAL_TIME"]]*len(cnt)
            
            # todo: Få den til å produsere grafer med begge typer y-akse. Får både cnt og mor!
            # todo: også få en legend som viser hvilket parameter til hvilken farge
            plt.scatter(cnt,height,c=colorsCnt,s=20)
        
        plt.xlim((-1.1,1.1))
        plt.ylim((-0.17,5))
        plt.xlabel("Parameter value")
        plt.ylabel("Fitness(speed)")
        plt.title(nameCnt)
        saveAndClose(plotConfig["RESULT_PATH"]+folder+nameCnt, show=plotConfig["VIEW_GRAPH"])


        for i in range(len(individualInfo)):
            mor= individualInfo[i][1]
            height = [individualInfo[i][2][0]/plotConfig["EVAL_TIME"]]*len(mor)

            #height=[i]*len(mor)
            plt.scatter(mor,height, c=colorsMor, s=20)

        plt.xlim((-1.1,1.1))
        plt.ylim((-0.17,5))
        plt.xlabel("Parameter value")
        plt.ylabel("Fitness(speed)")
        plt.title(nameMorph)
        saveAndClose(plotConfig["RESULT_PATH"]+folder+nameMorph, show=plotConfig["VIEW_GRAPH"])

    # TODO: MAKE diversity in cnt params
    return 

def diversity2(data, allGenerations, folder, plotConfig): 
    #nb: plots every individaul. Not only front
    step = plotConfig["DIVERSITY2_STEP"]
    print("Making diversity2, with step:",step)


    cntParams = plotConfig["NUM_CONTROL_PARAMS"]#len(data[0][1][0][1])
    morParams = plotConfig["NUM_MORPHOLOGY_PARAMS"]#18#len(data[0][1][0][0])

    colorsCnt=plotConfig["COLOR_ARRAY"][:cntParams,:]
    colorsMor=plotConfig["COLOR_ARRAY"][:morParams,:]

    #plotColorName(colorsCnt, colorsMor, folder, plotConfig)

    for gen_i in range(len(data)):
        g=gen_i*plotConfig["DIVERSITY2_STEP"]
        if g==plotConfig["GENERATIONS"]: g=plotConfig["GENERATIONS"]-1
        nameMorph = "Diversity in morphology params, gen"+str(g)
        nameCnt = "Diversity in control params, gen"+str(g)
        individualInfo = data[gen_i]
        # individualInfo: list? of individuals. Dvs individualinfo[i] = ind_i. ind_i[0]=list of cntParams, ind_i[1]=morph params, ind_i[2]=fitness [distance, stability]

        for i in range(len(individualInfo)):
            cnt= individualInfo[i][0]
            #height=[i]*len(cnt)
            height = [individualInfo[i][2][0]/plotConfig["EVAL_TIME"]]*len(cnt)
            
            # todo: Få den til å produsere grafer med begge typer y-akse. Får både cnt og mor!
            # todo: også få en legend som viser hvilket parameter til hvilken farge
            plt.scatter(cnt,height,c=colorsCnt,s=20)
        
        plt.xlim((-1.1,1.1))
        plt.ylim((-0.17,5))
        plt.xlabel("Parameter value")
        plt.ylabel("Fitness(speed)")
        plt.title(nameCnt)
        saveAndClose(plotConfig["RESULT_PATH"]+folder+nameCnt, show=plotConfig["VIEW_GRAPH"])


        for i in range(len(individualInfo)):
            mor= individualInfo[i][1]
            height = [individualInfo[i][2][0]/plotConfig["EVAL_TIME"]]*len(mor)

            #height=[i]*len(mor)
            plt.scatter(mor,height, c=colorsMor, s=20)

        plt.xlim((-1.1,1.1))
        plt.ylim((-0.17,5))
        plt.xlabel("Parameter value")
        plt.ylabel("Fitness(speed)")
        plt.title(nameMorph)
        saveAndClose(plotConfig["RESULT_PATH"]+folder+nameMorph, show=plotConfig["VIEW_GRAPH"])

    # TODO: MAKE diversity in cnt params
    return 


def diversity(allGenerations, generationInfo, folder, plotConfig):
    print("Making diversity")
    name = "Diversity in control or morphology params"
    divCnt=extractGenInfo(generationInfo, dataName="diversityInControlParams")
    divMor=extractGenInfo(generationInfo, dataName="diversityInMorphologyParams")
    if plotConfig["PLOT_EACH_RUN"]:
        plt.plot(allGenerations, divCnt, linewidth=0.8)
        plt.plot(allGenerations, divMor, linewidth=0.8)
        if not plotConfig["NO_LEGEND"]:
            plt.legend(["divCnt", "divMor"],loc='center left', bbox_to_anchor=(1, 0.5),fontsize='x-small')
        plt.xlabel("Generation")
        plt.ylabel("")
        if not plotConfig["NO_TITLE"]:
            plt.title(name)
        saveAndClose(plotConfig["RESULT_PATH"]+folder+name, show=plotConfig["VIEW_GRAPH"])
    return divCnt, divMor


def paretoFronts(allGenerations, generationInfo, folder, plotConfig, lines=False):
    print("Making pareto fronts graph")
    name = "Pareto fronts over generations, lines="+str(lines)
    fronts=extractGenInfo(generationInfo, dataName="ParetoFront")

    #todo: remove stuff over lim
    for i in range(len(fronts)):
        if plotConfig["STABILITY_LIM"]:
            fronts[i] = [x for x in fronts[i] if abs(x[1])<abs(plotConfig["STABILITY_LIM"])]

        if plotConfig["DISTANCE_LIM"]:
            fronts[i] = [x for x in fronts[i] if abs(x[0])<abs(plotConfig["DISTANCE_LIM"])]

    colors = cm.rainbow(np.linspace(0, 1, len(fronts)))
    for gen in range(len(fronts)):
        x1=[p[0] for p in fronts[gen]]
        x1Speed = [x/plotConfig["EVAL_TIME"] for x in x1]
        y1=[p[1] for p in fronts[gen]]
        if plotConfig["PLOT_EACH_RUN"]:
            if lines:
                plt.plot(x1Speed,y1, color=colors[gen], linewidth=0.8)#
            else:
                plt.plot(x1Speed,y1,'o', color=colors[gen], linewidth=0.8)#
    if plotConfig["PLOT_EACH_RUN"]:
        plt.xlabel("Speed")
        plt.ylabel("Stability")    
        if not plotConfig["NO_TITLE"]:
            plt.title(name)
        plt.ylim(-8,0)
        plt.xlim(-0.17,5)
        saveAndClose(plotConfig["RESULT_PATH"]+folder+name, show=plotConfig["VIEW_GRAPH"])
    return x1,y1, fronts #last front, and all

def plotMultiFronts(runs, dirNames, location, lines=True):
    """
    frontRuns - list of runs. Each run is a list of fronts.

    Should plot last front for each run i frontRuns
    """
    dataIndex=11 # for fronts
    frontRuns = [x[dataIndex] for x in runs]
    lastGens= [x[1][-1] for x in runs]
    startGens=[x[1][0] for x in runs]
    print("lastGens:", lastGens)
    #todo: need to plot with generation also (In case some have come further)
    name = "Pareto fronts over multiple (sub)Runs, lines="+str(lines)

    print("Creating ", name)
    legend=[]
    fig=plt.figure()
    ax=plt.subplot(111)
    colors=plotConfig["COLOR_ARRAY"][:len(frontRuns),:]
    for i in range(len(frontRuns)):
        lastGen = lastGens[i]#len(frontRuns[i])-1 #todo find lastgen
        startGen = startGens[i]
        lastFront = frontRuns[i][lastGen-startGen]
        legend.append(dirNames[i])
        x1=[p[0] for p in lastFront]
        x1Speed = [x/plotConfig["EVAL_TIME"] for x in x1]
        y1=[p[1] for p in lastFront] 
        if plotConfig["PLOT_EACH_RUN"]:
            if lines:
                ax.plot(x1Speed,y1,c=colors[i], linewidth=0.8)#, color=colors[gen])#
            else:
                ax.scatter(x1Speed,y1,s=10, edgecolors='none',c='r')
                #plt.scatter(x1Speed,y1,'o',s=12,c='r')#, color=colors[gen])#
    
    if not plotConfig["NO_LEGEND"]:
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.85, box.height * 0.85])
        plt.legend(legend,loc='center left', bbox_to_anchor=(1, 0.5),fontsize='x-small')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlabel("Speed")
    plt.ylabel("Stability")   
    if not plotConfig["NO_TITLE"]: 
        plt.title(name)
    plt.ylim(-8,0)
    plt.xlim(-0.17,5)
    saveAndClose(location+name, show=plotConfig["VIEW_GRAPH"])

def boxPlotStability(allGenerations, data, folder, plotConfig, config):
    print("making boxplots for stability")
    stability = np.zeros((len(allGenerations),config["POPULATION_SIZE"],2))
    for g in allGenerations:
        for ind in range(config["POPULATION_SIZE"]):
            stability[g][ind]=data[g][1][ind][3]
            


    for g in allGenerations:
        name="boxplotStability, gen"+str(g) #+", mean:"+str(np.mean(stability1[g]))+str(np.mean(stability2[g]))
        #print(np.mean(stability[g], axis=0))
        plt.boxplot((stability[g,:,0], stability[g,:,1]))
        if not plotConfig["NO_TITLE"]:
            plt.title(name)
        saveAndClose(plotConfig["RESULT_PATH"]+folder+name, show=plotConfig["VIEW_GRAPH"])

def hypervolume(allGenerations, generationInfo, folder, plotConfig):
    print("Making hypervolume plot")
    name="hypervolume"
    #hypervolume = extractGenInfo(generationInfo, dataName="Hypervolume")
    hypervolume = extractGenInfo(generationInfo, dataName="New Hypervolume")

    if plotConfig["PLOT_EACH_RUN"]:
        plt.plot(allGenerations, hypervolume, linewidth=0.8)
        plt.xlabel("Generation")
        plt.ylabel("Hypervolume")
        plt.ylim(200,3000)
        if not plotConfig["NO_LEGEND"]:
            plt.legend("Full training",fontsize='x-small')
        if not plotConfig["NO_TITLE"]:
            plt.title(name)
    saveAndClose(plotConfig["RESULT_PATH"]+folder+name, show=plotConfig["VIEW_GRAPH"])

    return hypervolume

def plotSplitMorph(plotConfig, folder, allFronts, lines=True):
    # TODO: plot dots for fitness til de utvalgte morphologiene
    # deretter paretofronten i denne generasjonene.

    # må se gjennom hvilke undermapper man finner, og finn filer med passende navn.
    # for hvert av disse lager man et plot, og lagrer det i graphs.
    root, dirs, files =next(os.walk(plotConfig["RESULT_PATH"]))
    #each folder inside a run
    print("looking in ", dirs)
   
    for dir in dirs:
        if dir=='graphs': continue
        intsInString = re.findall(r'\d+', dir)
        gen=int(intsInString[0])
        f=open(plotConfig["RESULT_PATH"]+dir+'/morphologiesGen'+str(gen)+'.json')
        morphologiFile = json.load(f)
        f.close()
        print("the file:", morphologiFile)
        try:
            fitnessList = morphologiFile["PRETRAINED_MORPHOLOGIES_FITNESS"]
        except KeyError:
            print("cant find PRETRAINED_MORPHOLOGIES_FITNESS in config")
            break
        print(fitnessList)
        # plot fitnessList with xlim and ylim
        
        plt.scatter([x[0] for x in fitnessList],[x[1] for x in fitnessList])
        for i in range(len(fitnessList)):
            plt.annotate(str(i), (fitnessList[i][0], fitnessList[i][1]))
        
        # plot front in gen

        x1=[p[0] for p in allFronts[gen]]
        x1Speed = [x/plotConfig["EVAL_TIME"] for x in x1]
        y1=[p[1] for p in allFronts[gen]]
        if lines:
            plt.plot(x1Speed,y1, color='red')#
        else:
            plt.plot(x1Speed,y1,'o', color='red')#
        name="Pareto front and chosen morphologies in gen "+str(gen)
        print("Making", name)
        plt.xlabel("Speed")
        plt.ylabel("Stability")    
        if not plotConfig["NO_TITLE"]:
            plt.title(name)
        plt.ylim(-8,0)
        plt.xlim(-0.17,5)
        saveAndClose(folder+name, show=plotConfig["VIEW_GRAPH"])

def plotOriginalResultsMain(plotConfig, startingGen=0, onlyHypervolume=False):    
    print("startGen:", startingGen)
    plotConfig["RESULT_PATH"]+="/"
    print("opening:",plotConfig["RESULT_PATH"]+'config.json')
    f=open(plotConfig["RESULT_PATH"]+'config.json')
    config = json.load(f)
    f.close()
    try:
        startingGen=config["CURRENT_GENERATION"]+1
    except KeyError:
        pass
    
    lastGen=findLastGen(plotConfig["RESULT_PATH"])

    allGenerations = list(range(startingGen,lastGen+1))
    allSolutions = list(range(startingGen,config["POPULATION_SIZE"]))

    data = inspectGenerations(allSolutions, allGenerations, plotConfig["RESULT_PATH"])
    
    generationInfo = []
    # each generation
    for g in range(len(allGenerations)):
        genInfo=data[g][0]
        generationInfo.append(genInfo)
        """
        # each solution
        for s in range(len(allSolutions)):
            ind=data[g][1][s]
            indControlParams=ind[0]
            indFitness = ind[1]
        """
    folder = "graphs/"
    saveLocation=plotConfig["RESULT_PATH"]+folder
    if not os.path.exists(saveLocation):
        os.makedirs(saveLocation)
    
    print("data:", generationInfo[0])
    print("lager stuff i:", saveLocation)

    
    newData=[]
    for g in range(0,len(allGenerations)+1,plotConfig["DIVERSITY2_STEP"]):
        print("Saving individuals in generation",g)
        if g==len(allGenerations): g=len(allGenerations)-1
        individualInfo = data[g][1]
        # individualInfo: list? of individuals. Dvs individualinfo[i] = ind_i. ind_i[0]=list of cntParams, ind_i[1]=morph params, ind_i[2]=fitness [distance, stability]
        #individualInfo = individualInfo.copy()
        individualInfo.sort(key=lambda x: x[2][0], reverse=False)
        newData.append(individualInfo)

    if plotConfig["DIVERSITY2"]:
        diversity2(newData, allGenerations, folder, plotConfig)

    lastGenInfo = newData[-1] # individualInfo for the last generation

    #test:
    #print("##################################okkk#################################")
    #print(startingGen)
    #print(len(allGenerations))
    #print(generationInfo[0])
    #print(folder)
    #print(plotConfig)
    #print("##################################okkk#################################")


    #if startingGen!=0:
    #    sys.exit()
    #test done
    
    
    if not onlyHypervolume:
        best, mean, worst = bestMeanWorst(allGenerations, generationInfo, folder, plotConfig)
        std= stds(allGenerations, generationInfo, folder, plotConfig)
        divCnt, divMor = diversity(allGenerations, generationInfo, folder, plotConfig)
        lastFrontX, lastFrontY,allFronts =paretoFronts(allGenerations, generationInfo, folder, plotConfig, lines=False)
        lastFrontXLine, lastFrontYLine, allFrontsLine = paretoFronts(allGenerations, generationInfo, folder, plotConfig, lines=True)
        plotSplitMorph(plotConfig, saveLocation, allFrontsLine)
    else:
        best = mean = worst = std = divCnt = divMor = lastFrontX = lastFrontY = allFronts = lastFrontXLine = lastFrontYLine = allFrontsLine = None
    
    hypV= hypervolume(allGenerations, generationInfo, folder, plotConfig)
    

    #boxPlotStability(allGenerations, data, folder, plotConfig,config)
    return [lastGenInfo,allGenerations, hypV, best, mean, worst, std, divCnt, divMor, lastFrontX, lastFrontY, allFronts, lastFrontXLine, lastFrontYLine, allFrontsLine]
    #return [data,allGenerations, hypV, best, mean, worst, std, divCnt, divMor, lastFrontX, lastFrontY, allFronts, lastFrontXLine, lastFrontYLine, allFrontsLine]

def plotMulti(runs, dirNames, location, alsoMean=True, fronts=False):
    #todo: sjekk plotConfig for hvilke plots vi skal ha. Bruker bare hypervolum i starten :)
    hypervolumeMean=None

    #todo: sjekk at alle runs[i][0] - allGenerations - er like for alle i
    # bruker den første nå:
    allGenerations = list(range(plotConfig["GENERATIONS"])) #runs[0][1]

    # hyperVolume:
    name = "Hypervolumes over different runs"
    print("#### creating multi-hypervolume graph ####")
    fig=plt.figure()
    ax=plt.subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    dataIndex=2
    colors=plotConfig["COLOR_ARRAY"][:len(runs),:]

    for i in range(len(runs)):
        #print("ruuns", runs)
        allGenerations=runs[i][1]
        ax.plot(allGenerations, runs[i][dataIndex], c=colors[i], linewidth=0.8)
    
    if not plotConfig["NO_TITLE"]:
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.85, box.height * 0.85])

        plt.title(name)
    plt.ylim(200,3000)
    print(dirNames)
    if dirNames[0][:8]=="Results_":
        dirNames=[x[19:] for x in dirNames]
    
    if not plotConfig["NO_LEGEND"]:
        plt.legend(dirNames,loc='center left', bbox_to_anchor=(1, 0.5),fontsize='x-small')
    plt.xlabel("Generation")
    plt.ylabel("Hypervolume")
    saveAndClose(location+name, show=False)

    if alsoMean: # fiks dette!
        # all runs need to have same number of generations!
        hyperRuns = [x[dataIndex] for x in runs]
        length=plotConfig["GENERATIONS"] #len(min(hyperRuns,key = lambda x: len(x))) ##### todo: her er du din tulling.
        name = "Average hypervolum over different runs, conf-int 1std"
        print(len(hyperRuns),length)
        hypervolumeData=np.zeros((len(hyperRuns), length))
        for i in range(len(hyperRuns)):
            hypervolumeData[i,:]=hyperRuns[i]
        hypervolumeMean=np.mean(hypervolumeData, axis=0)
        hypervolumeStd = np.std(hypervolumeData, axis=0)
        allGenerations=list(range(length))
        plt.plot(allGenerations, hypervolumeMean, linewidth=0.8)#np.mean(hyperRuns, axis=0))

        minVal = hypervolumeMean - 1*hypervolumeStd
        maxVal = hypervolumeMean + 1*hypervolumeStd
        plt.fill_between(allGenerations, minVal, maxVal, color='blue',alpha=0.2)
        
        if not plotConfig["NO_TITLE"]:
            plt.title(name)

        plt.ylim(200,3000)
        plt.xlabel("Generation")
        plt.ylabel("Hypervolume")
        saveAndClose(location+name, show=False)


    if fronts:
        plotMultiFronts(runs, dirNames, location, lines=True)
        plotMultiFronts(runs, dirNames, location, lines=False)

    #return hypervolumeMean, hypervolumeStd
    allRuns = []
    for i in range(len(hyperRuns)):
        allRuns.append((hyperRuns[i], None))
    
    return [(hypervolumeMean, hypervolumeStd)], allRuns
    
def plotMultiConfig(data, dirNames, location, onlyFillFirst=True):
    name="Average hypervolum over different config runs,  conf-int 1std"
    print("Making:", name)
    allGenerations = list(range(plotConfig["GENERATIONS"]))#list(range(avgData[1].shape[0]))
    fig=plt.figure()
    ax=plt.subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    colors=plotConfig["COLOR_ARRAY"][4:,:]

    dirNames = [x[4:] for x in dirNames]
    print("gi meg lunsjpenga'a, ssssssssjukka!", len(data))
    j=0
    for i in range(len(data)):
        if onlyFillFirst and i==0: continue
        if (i-1)%3==0: j+=1
        ax.plot(allGenerations,data[i][0], c='black', linewidth=0.8, alpha=0.8)

    if not plotConfig["NO_LEGEND"]:
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.87, box.height * 0.87])
        plt.legend(dirNames,loc='center left', bbox_to_anchor=(1, 0.5),fontsize='x-small')

    if onlyFillFirst:
        i=0
        min=data[i][0] - 1*data[i][1]
        max=data[i][0] + 1*data[i][1]
        plt.fill_between(allGenerations, min,max,color='blue',alpha=0.2) 

    plt.ylim(200,3000)
    if not plotConfig["NO_TITLE"]:
        plt.title(name)
    plt.xlabel("Generation")
    plt.ylabel("Hypervolume")
    saveAndClose(location+name)

    ###############

    name="Average hypervolum over different config runs, no std"
    print("Making:", name)
    allGenerations = list(range(plotConfig["GENERATIONS"]))#list(range(avgData[1].shape[0]))
    fig=plt.figure()
    ax=plt.subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    colors=plotConfig["COLOR_ARRAY"][:len(data),:]

    dirNames = [x[4:] for x in dirNames]
    for i in range(len(data)):
        ax.plot(allGenerations,data[i][0], c=colors[i], linewidth=0.8)


    if not plotConfig["NO_LEGEND"]:
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.87, box.height * 0.87])
        plt.legend(dirNames,loc='center left', bbox_to_anchor=(1, 0.5),fontsize='x-small')

    #for i in range(len(data)):
    #    min=data[i][0] - 2*data[i][1]
    #    max=data[i][0] + 2*data[i][1]
    #    plt.fill_between(allGenerations, min,max,color=colors[i],alpha=0.2)

    plt.ylim(200,3000)
    if not plotConfig["NO_TITLE"]:
        plt.title(name)
    plt.xlabel("Generation")
    plt.ylabel("Hypervolume")
    saveAndClose(location+name)



def sortData(runData, plotConfig, dMax=100000, dMin=0, sMax=100000, sMin=0):
        # ind_i = data[run_index][individual_i]  ind_i[0]=list of cntParams, ind_i[1]=morph params, ind_i[2]=fitness [distance, stability]
    
    morParams = plotConfig["NUM_MORPHOLOGY_PARAMS"]
    cntParams = plotConfig["NUM_CONTROL_PARAMS"]
    runs = len(runData)
    plotConfig["NUM_RUNS"]=runs
    popSize=plotConfig["POP_SIZE"]

    dataMorP=[]
    dataCntP=[]
    dataMorX=[] # nested list of all morph-params. dataMorX[i] = list of ind i's params
    dataCntX=[] # nested list of all cnt-params 
    dataY = [] # fitness (distance). dataY[i] - fitness for individual i
    for i in range(morParams):
        dataMorP.append([])
    for i in range(cntParams):
        dataCntP.append([])
    #np.full((morParams,runs,popSize,2), None)
    #np.full((cntParams,runs,popSize,2), None)

    # hei du! jada, joda det er litt rar rekkefølge her, men det funker fint/fjell
    for run_i in range(runs):
        print(len(runData[run_i][0]))
        for ind_i in range(len(runData[run_i][0])):
            ind=runData[run_i][0][ind_i]
            fitDist=ind[2][0]
            fitStab=ind[2][1]
            
            #check limits
            if (abs(fitDist)<abs(dMin)) or (abs(fitDist)>abs(dMax)):
                continue
            if (abs(fitStab)<abs(sMin)) or (abs(fitStab)>abs(sMax)):
                continue

            fitSpeed = fitDist/plotConfig["EVAL_TIME"]
            for mor_i in range(morParams):
                morParamV=ind[1][mor_i]
                dataMorP[mor_i].append([morParamV,fitSpeed])

            for cnt_i in range(cntParams):
                cntParamV=ind[0][cnt_i]
                dataCntP[cnt_i].append([cntParamV,fitSpeed])

            dataY.append(fitSpeed)
            dataMorX.append(ind[1])
            dataCntX.append(ind[0])

    dataMorP=np.asarray(dataMorP) #dataMorP.reshape(morParams,runs*popSize,2)
    dataCntP=np.asarray(dataCntP) #dataCntP.reshape(cntParams,runs*popSize,2)
    dataMorX = np.asarray(dataMorX)
    dataCntX = np.asarray(dataCntX)
    dataY = np.asarray(dataY)

    print("dataMorP",dataMorP.shape)
    print("dataCntP",dataCntP.shape)
    print("dataMorX:",dataMorX.shape)
    print("dataCntX:",dataCntX.shape)
    print("dataY:",dataY.shape)

    return dataMorP, dataCntP, plotConfig, dataMorX, dataCntX, dataY


def plotMultiScatterParams(dataMorP, dataCntP, plotConfig, location):

    print("plotMultiScatter")
    morParams = plotConfig["NUM_MORPHOLOGY_PARAMS"]
    cntParams = plotConfig["NUM_CONTROL_PARAMS"]

    for mor_i in range(morParams): #one plot, save
        plt.scatter(dataMorP[mor_i,:,1],dataMorP[mor_i,:,0],alpha=0.1,s=20, edgecolors='none',c='b')

        #save and stuff
        name="Morphology param "+str(mor_i)+" for last generation over all runs"
        plt.ylim((-1.1,1.1))
        plt.xlim((-0.17,5))
        plt.ylabel("Parameter value")
        plt.xlabel("Fitness(speed)")
        if not plotConfig["NO_TITLE"]:
            plt.title(name)
        saveAndClose(location+name, show=plotConfig["VIEW_GRAPH"])

    for cnt_i in range(cntParams): #one plot, save
        plt.scatter(dataCntP[cnt_i,:,1],dataCntP[cnt_i,:,0],alpha=0.1,s=20, edgecolors='none',c='b')

        #save and stuff
        name="Control param "+str(cnt_i)+" for last generation over all runs"
        plt.ylim((-1.1,1.1))
        plt.xlim((-0.17,5))
        plt.ylabel("Parameter value")
        plt.xlabel("Fitness(speed)")
        if not plotConfig["NO_TITLE"]:
            plt.title(name)
        saveAndClose(location+name, show=plotConfig["VIEW_GRAPH"])

def correlation(dataMorP, dataCntP, plotConfig, location):

    print("correlation")
    morParams = plotConfig["NUM_MORPHOLOGY_PARAMS"]
    cntParams = plotConfig["NUM_CONTROL_PARAMS"]

    print("index: pearson: p: adjusted-p: spearman: p: adjusted-p:")
    for mor_i in range(morParams): #one plot, save
        pCorr, pP = pearsonr(dataMorP[mor_i,:,1],dataMorP[mor_i,:,0])
        sCorr, sP = spearmanr(dataMorP[mor_i,:,1],dataMorP[mor_i,:,0])
        print(mor_i, "{:.3f}".format(pCorr), "{:.8f}".format(pP), "{:.8f}".format(pP*morParams), "{:.3f}".format(sCorr), "{:.8f}".format(sP), "{:.8f}".format(sP*morParams))

    print("\n\n")
    print("index: pearson: spearman:")
    for cnt_i in range(cntParams): #one plot, save
        pCorr, pP = pearsonr(dataCntP[cnt_i,:,1],dataCntP[cnt_i,:,0])
        sCorr, sP = spearmanr(dataCntP[cnt_i,:,1],dataCntP[cnt_i,:,0])
        print(cnt_i, "{:.3f}".format(pCorr), "{:.8f}".format(pP), "{:.8f}".format(pP*cntParams), "{:.3f}".format(sCorr), "{:.8f}".format(sP), "{:.8f}".format(sP*cntParams))

def plotKernalDensityEstimate(data, name, plotConfig, location):
    print("plotKernalDensityEstimate")
    
    for i in range(len(data)):
        y = (data[i][:,0]+1)/2     # -1-1 -> 0-2 -> 0-1 
        x = data[i][:,1]/100 # 0-70 -> 0-1(0.7)
        #dataMorP and dataCntP in on shape: (x,2)
        ymin, ymax = -0.08, 1.08 # todo
        xmin, xmax = -0.08, 0.60
        #
        # Peform the kernel density estimate
        xx, yy = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
        positions = np.vstack([xx.ravel(), yy.ravel()])
        values = np.vstack([x, y])
        kernel = st.gaussian_kde(values)
        f = np.reshape(kernel(positions).T, xx.shape)
        #
        plt.close()
        fig = plt.figure()
        ax = fig.gca()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        #ax.set_xlim(xmin, xmax)
        #ax.set_ylim(ymin, ymax)
        #
        # Contourf plot
        #cfset = ax.contourf(xx, yy, f, cmap='Reds')
        ## Or kernel density estimate plot instead of the contourf plot
        ax.imshow(np.rot90(f), cmap='Reds', extent=[xmin, xmax, ymin, ymax])
        #
        # Contour plot
        #cset = ax.contour(xx, yy, f, colors='k',linewidths=0.5)
        # Label plot
        ax.clabel(cset, inline=1, fontsize=7)
        ax.set_ylabel("Parameter value (-1 to 1) -> (0 to 1)")
        ax.set_xlabel("Fitness (speed) *10^-3")
        plt.title(name+str(i))
        #plt.figure()
        #plt.xlim(xmin, xmax)
        #plt.ylim(ymin, ymax)
        plt.scatter(x,y,alpha=0.1,s=20, edgecolors='none',c='b')
        saveAndClose(location+name+str(i), show=plotConfig["VIEW_GRAPH"])


def linearRegression(y,x):
    x =sm.add_constant(x)
    model = sm.OLS(y,x)
    results = model.fit()
    print(results.summary())    

def corrMat(data, name, location):
    df = pd.DataFrame(data)
    correlation_mat = df.corr()

    sns.heatmap(correlation_mat, annot = True)
    if not plotConfig["NO_TITLE"]:
        plt.title(name)
    saveAndClose(location+name)



def loadRunData(plotConfig, location):
    print("Run data only. Opening runData.json at",location)
    f=open(location+'runData.json')
    s=time.time()
    data = json.load(f)
    print("time to open:",time.time()-s)

    dataMorP, dataCntP, plotConfig, dataMorX, dataCntX, dataY = sortData(data,plotConfig)#, sMax=-7.5)

    #name="Correlation matrix morphology params dmin=0"
    #corrMat(dataMorX, name, location)
    #name="Correlation matrix controll params dmin=0"
    #corrMat(dataCntX, name, location)
    plt.rc('font', size=18) 
    plotMultiScatterParams(dataMorP, dataCntP, plotConfig,location)
    plt.rc('font', size=11.5) 

    #correlation(dataMorP, dataCntP, plotConfig, location)
    #
    #dataMorP, dataCntP, plotConfig, dataMorX, dataCntX, dataY = sortData(data,plotConfig, sMax=-7.5, dMin=5)
    #name="Correlation matrix morphology params dmin=5"
    #corrMat(dataMorX, name, location)
    #name="Correlation matrix controll params dmin=5"
    #corrMat(dataCntX, name, location)
    
    #linearRegression(dataY, dataMorX)
    #linearRegression(dataY, dataCntX)
    #print("#######################")
    #linearRegression(dataY, np.concatenate((dataMorX, dataCntX),axis=1))


    #name = "Kernal density estimatation for morphology param"
    #plotKernalDensityEstimate(dataMorP, name, plotConfig, location)
    #name = "Kernal density estimatation for controll param"
    #plotKernalDensityEstimate(dataCntP, name, plotConfig,location)





    # Dont use: loess why? Use the linux version on M-drive!!!!

    
    legendNamesMain=[]
    for i in range(len(data)):
        legendNamesMain.append("Run"+str(i))
    return plotMulti(data, legendNamesMain, location=location,fronts=True)
    #return None, None

if __name__ == "__main__":




    #root.withdraw()
    #root.update()
    if plotConfig["RESULTS_ORIGINAL"]:
        root = Tk()
        if plotConfig["CHOOSE_DIR"]:
            plotConfig["RESULTS_PATH_ORIGINAL"]=askdirectory(initialdir=plotConfig["RESULTS_PATH_ORIGINAL"], title='Please select a directory')
            plotConfig["RESULT_PATH"]=plotConfig["RESULTS_PATH_ORIGINAL"]
            plotOriginalResultsMain(plotConfig,startingGen=0)
        else:
            root, dirs, files =next(os.walk(plotConfig["RESULTS_PATH_ORIGINAL"]))
            for dir in dirs:
                plotConfig["RESULT_PATH"]=plotConfig["RESULTS_PATH_ORIGINAL"]+dir
                plotOriginalResultsMain(plotConfig)
            """
            for root, dirs, files in os.walk(RESULT_PATH):
                print("NEW:")
                print(dirs)
                print(len(dirs))
                print("\n")
            """
    

    if plotConfig["RESULTS_ARCHIVE"]:
        root0, dirs0, files0 =next(os.walk(plotConfig["RESULTS_PATH_ARCHIVE"]))
        print("####")
        for dir0 in dirs0:
            if dir0=="old": continue
            #if testing:
            #    if dir0!="testData": continue 
            
            if dir0!="Fox": continue

            root1, dirs1, files1 =next(os.walk(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0))
            print("newTest")
            avgHypervolumRuns =[]
            old=None
            legendNamesConfig=[]
            for dir1 in dirs1:
                print("newConfig")
                print("dir1:",dir1)
                if dir1=="old": 
                    old=dirs1.index(dir1)
                    continue
                if testing:
                    if dir1!= "256_0.3_0.2_0.1_0.01": continue 

                legendNamesConfig.append(dir1)
                if plotConfig["ONLY_RUNDATA"]:

                    meanData, allConfigRunsData = loadRunData(plotConfig, location=str(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1+"/"))
                    if dir1== "256_0.3_0.2_0.1_0.01" and not testing: #todo: use this
                    #if dir1 == "256_1.0_0.02_0.0_0.02": only for testing
                        avgHypervolumRuns+= meanData
                    else:
                        avgHypervolumRuns+= allConfigRunsData
                    continue

                #print("her:",str(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1))
                root2, dirs2, files2 =next(os.walk(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1))
                runs = []
                legendNamesMain = []
                notDone = None
                for dir2 in dirs2:
                    if dir2=="ikke ferdig": 
                        notDone = dirs2.index(dir2)
                        continue
                    print("ny kjøring :)"+dir2)
                    if dir2=="graph":continue
                    #if testing:
                    #    if not (dir2=="Results_14.03.2022_15.38.45" or dir2=="Results_14.03.2022_15.44.40") : continue

                    legendNamesMain.append(dir2)
                    oneRun = plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1+"/"+dir2
                    plotConfig["RESULT_PATH"]=oneRun
                    oneMainRunData=plotOriginalResultsMain(plotConfig)
                    runs.append(oneMainRunData)
                    print("#######################################")
                    # allGenerations, hypV, best, mean, worst, std, divCnt, divMor, lastFrontX, lastFrontY, allFronts, lastFrontLine, allFrontsLine
                    #plotConfig["PLOT_EACH_RUN"]=False
                    if plotConfig["EACH_SUB_FOLDER"]:
                        root3, dirs3, files3 =next(os.walk(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1+"/"+dir2))
                        #each folder inside a run
                        for dir3 in dirs3:
                            print("subFolder",dir3)
                            if dir3=='graphs': continue
                            
                            intsInString = re.findall(r'\d+', dir3)
                            subGen=int(intsInString[0])
                            print("subGen:", str(subGen))

                            root4, dirs4, files4 =next(os.walk(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1+"/"+dir2+"/"+dir3))
                            # 64ind_2048gen, 32ind_2048gen osv
                            subRunsInd=[]
                            subRunsNames=[]
                            legendNames=[] # trenger bare denne for å kunne skskludere 8ind_2048
                            for dir4 in dirs4:
                                #64Ind_2048 eller 32Ind_2048 eller 8ind_2048
                                if dir4=="8ind_2048gen": continue
                                
                                root5, dirs5, files5 =next(os.walk(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1+"/"+dir2+"/"+dir3+"/"+dir4))
                                # morphology2, morphology5 osv
                                subRuns=[]
                                for dir5 in dirs5:
                                    print("one subRun", dir5)
                                    #one run. morphology2 eller 5 osv
                                    oneSubRun = plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1+"/"+dir2+"/"+dir3+"/"+dir4+"/"+dir5
                                    plotConfig["RESULT_PATH"]=oneSubRun
                                    oneSubRunData=plotOriginalResultsMain(plotConfig, startingGen=subGen+1, onlyHypervolume=False)
                                    subRuns.append(oneSubRunData)
                                    
                                legendNames.append(dirs5+["Normal_co"])

                                #adding the original run to each list of subRun
                                subRuns.append(oneMainRunData)
                                
                                subRunsNames.append(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1+"/"+dir2+"/"+dir3+"/"+dir4)
                                subRunsInd.append(subRuns)
                                
                            
                            for i in range(len(subRunsInd)):
                                plotMulti(subRunsInd[i], legendNames[i], location=str(subRunsNames[i]), alsoMean=True, fronts=True) 
                            print("plot multi is done")
                #if testing:
                #    sys.exit("Da tenker jeg vi gir oss der")

                #here: plot multiple runs with same config
                #hypervolume over all:
                print(dirs2)
                if notDone!=None:
                    dirs2.pop(notDone)
                print(dirs2)
                if dirs2:
                    path=plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1+"/"
                    meanData, allConfigRunsData = plotMulti(runs, legendNamesMain, location=path,fronts=True) # todo: legg til alle kjøringer, men ikke de 25 første. plotMulti må returnere all, men bare avg av første. Sett fargen til svart.
                    if dir1== "256_0.3_0.2_0.1_0.01":
                        avgHypervolumRuns+= meanData
                    else:
                        avgHypervolumRuns+= allConfigRunsData
                    #plotMultiBoxplotDiversity(runs, dirs2, location=str(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1+"/"))
                    

                    if plotConfig["OVERWRITE_RUNDATA"]:
                        print("Saving data to json file: runData.json at",path)
                        saveDataJson(runs, path+"runData.json")
                ##allFrontsLine over all

                #divCnt and divMor over all
            # etter loadRun: går rett hit :)
            #here: plot over mutiple configs?
            if len(avgHypervolumRuns)!=0:
                print(dirs1)
                if old!=None:
                    dirs1.pop(old)
                print(dirs1)
                if dirs1:
                    plotMultiConfig(avgHypervolumRuns, legendNamesConfig, location=str(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"))


