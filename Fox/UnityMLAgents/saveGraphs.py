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
random.seed=35607117 # only for colors

testing = True #todo: fjern
plotConfig ={
    "CHOOSE_DIR": False,
    "VIEW_GRAPH" :False,
    "RESULTS_ORIGINAL": False,  
    "RESULTS_ARCHIVE" : True,
    "EACH_RESULT_ARCIVE" : True,
    "DIVERSITY2" : False,
    "SUBTRAININGS" :True,
    "PLOT_EACH_RUN":True,
}

plotConfig["RESULTS_ARCHIVE_SUB"]=["Testing 1.1, Testing 1.0"]

if platform.system()=='Windows': 
    plotConfig["RESULTS_PATH_ORIGINAL"]="C:/Users/stein/Documents/Unity/results/"
    plotConfig["RESULTS_PATH_ARCHIVE"]="C:/Users/stein/Documents/Unity/resultsArchive/"
elif platform.system()=='Linux':
    plotConfig["RESULTS_PATH_ORIGINAL"] = "/uio/hume/student-u01/steinboe/Documents/master/MasterThesis/results"
else:
    sys.exit("what?")


def findLastGen(NumGen, resultPath):
    """
    Input the number (int) of generation set in training, and result path
    returns the actual number (int) of generations before ending
    (Note: same func as in visualiseSolution, but does not work correctly when imported)
    """
    print(NumGen)
    lastGen=NumGen
    for i in range(NumGen):
        theFile = resultPath+'gen'+str(lastGen)+'.json'
        try:
            open(theFile)
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
                theGenDir = json.load(open(theFile))
                break
            except FileNotFoundError:
                print("Generation ",endGen, "not found. Getting ", endGen-1, "instead")
                endGen-=1

        if theGenDir==None:
            sys.exit("Could not find generation "+str(g))
        data.append(getSolutions(theGenDir,solutions))

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

def createGraph(xData, yData):
    plt.plot(xData, yData)

def saveAndClose(location, show=False):

    plt.savefig(location)
    #if show:
    #    plt.show()
    plt.close()
    plt.figure()

def bestMeanWorst(allGenerations, generationInfo, folder, plotConfig):
    ### Best, mean and worst for one training ###
    print("Making best mean worst graph")
    name="Distance, Best-, mean- and worst fitness measure"
    bestFits=extractGenInfo(generationInfo, dataName="bestFitDist")
    mean=extractGenInfo(generationInfo, dataName="meanDist")
    worstFits=extractGenInfo(generationInfo, dataName="worstFitDist")
    if plotConfig["PLOT_EACH_RUN"]:
        plt.plot(allGenerations, bestFits)
        plt.plot(allGenerations, mean)
        plt.plot(allGenerations, worstFits)
        plt.legend(["bestFitDist", "meanDist", "worstFitDist"])
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.ylim(0,55)
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
        plt.plot(allGenerations, stds)
        plt.plot(allGenerations, stds)
        plt.legend(["stdDist", "stdStability"])
        plt.xlabel("Generation")
        plt.ylabel("")
        plt.ylim(1,4)
        plt.title(name)
        saveAndClose(plotConfig["RESULT_PATH"]+folder+name, show=plotConfig["VIEW_GRAPH"])
    ############################################################
    return stds

def diversity2(data, allGenerations, folder, step=100):
    print("Making diversity2, with step:",step)


    morParams = len(data[0][1][0][1])
    cntParams = len(data[0][1][0][0])

    colorsCnt=np.zeros((cntParams,3))
    colorsMor=np.zeros((morParams,3))
    
    for i in range(cntParams):
        colorsCnt[i]=np.array([random.random(), random.random(), random.random()])
    for i in range(morParams):
        colorsMor[i]=np.array([random.random(), random.random(), random.random()])
    for g in range(0,len(allGenerations)+1,step):
        if g==len(allGenerations): g=len(allGenerations)-1
        nameMorph = "Diversity in morphology params, gen"+str(g)
        nameCnt = "Diversity in control params, gen"+str(g)
        individualInfo = data[g][1]
        for i in range(len(individualInfo)):
            cnt= individualInfo[i][0]
            height=[i]*len(cnt)
        
            plt.scatter(cnt,height,c=colorsCnt)
        
        plt.xlim((-1,1))
        plt.xlabel("Parameter value")
        plt.ylabel("Individuals")
        plt.title(nameCnt)
        saveAndClose(plotConfig["RESULT_PATH"]+folder+nameCnt, show=plotConfig["VIEW_GRAPH"])


        for i in range(len(individualInfo)):
            mor= individualInfo[i][1]
            height=[i]*len(mor)
            plt.scatter(mor,height, c=colorsMor)

        plt.xlim((-1,1))
        plt.xlabel("Parameter value")
        plt.ylabel("Individuals")
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
        plt.plot(allGenerations, divCnt)
        plt.plot(allGenerations, divMor)
        plt.legend(["divCnt", "divMor"])
        plt.xlabel("Generation")
        plt.ylabel("")
        plt.title(name)
        saveAndClose(plotConfig["RESULT_PATH"]+folder+name, show=plotConfig["VIEW_GRAPH"])
    return divCnt, divMor


def paretoFronts(allGenerations, generationInfo, folder, plotConfig, lines=False):
    print("Making pareto fronts graph")
    name = "Pareto fronts over generations, lines="+str(lines)
    fronts=extractGenInfo(generationInfo, dataName="ParetoFront")
    colors = cm.rainbow(np.linspace(0, 1, len(fronts)))
    for gen in range(len(fronts)):
        x1=[p[0] for p in fronts[gen]]
        y1=[p[1] for p in fronts[gen]]
        if plotConfig["PLOT_EACH_RUN"]:
            if lines:
                plt.plot(x1,y1, color=colors[gen])#
            else:
                plt.plot(x1,y1,'o', color=colors[gen])#
    if plotConfig["PLOT_EACH_RUN"]:
        plt.xlabel("Distance")
        plt.ylabel("Stability")    
        plt.title(name)
        plt.ylim(-20,0)
        plt.xlim(0,60)
        saveAndClose(plotConfig["RESULT_PATH"]+folder+name, show=plotConfig["VIEW_GRAPH"])
    return x1,y1, fronts #last front, and all

def plotMultiFronts(runs, dirNames, location, lines=True):
    """
    frontRuns - list of runs. Each run is a list of fronts.

    Should plot last front for each run i frontRuns
    """
    dataIndex=10 # for fronts
    frontRuns = [x[dataIndex] for x in runs]
    lastGens= [x[0][-1] for x in runs]
    startGens=[x[0][0] for x in runs]
    print("lastGens:", lastGens)
    #todo: need to plot with generation also (In case some have come further)
    name = "Pareto fronts over multiple subRuns, lines="+str(lines)

    print("Creating ", name)
    legend=[]
    for i in range(len(frontRuns)):
        lastGen = lastGens[i]#len(frontRuns[i])-1 #todo find lastgen
        startGen = startGens[i]
        lastFront = frontRuns[i][lastGen-startGen]
        legend.append(dirNames[i]+"_gen"+str(lastGen))
        x1=[p[0] for p in lastFront]
        y1=[p[1] for p in lastFront]
        if plotConfig["PLOT_EACH_RUN"]:
            if lines:
                plt.plot(x1,y1)#, color=colors[gen])#
            else:
                plt.plot(x1,y1,'o')#, color=colors[gen])#
    
    plt.legend(legend)
    plt.xlabel("Distance")
    plt.ylabel("Stability")    
    plt.title(name)
    plt.ylim(-20,0)
    plt.xlim(0,60)
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
        plt.title(name)
        saveAndClose(plotConfig["RESULT_PATH"]+folder+name, show=plotConfig["VIEW_GRAPH"])



def hypervolume(allGenerations, generationInfo, folder, plotConfig):
    print("Making hypervolume plot")
    name="hypervolume"
    hypervolume = extractGenInfo(generationInfo, dataName="Hypervolume")
    if plotConfig["PLOT_EACH_RUN"]:
        plt.plot(allGenerations, hypervolume)
        plt.xlabel("Generation")
        plt.ylabel("Hypervolume")
        plt.ylim(200,2800)
        plt.legend("Full training")
        plt.title(name)
    saveAndClose(plotConfig["RESULT_PATH"]+folder+name, show=plotConfig["VIEW_GRAPH"])

    return hypervolume

def plotOriginalResultsMain(plotConfig, startingGen=0, onlyHypervolume=False):    
    print("startGen:", startingGen)
    plotConfig["RESULT_PATH"]+="/"
    print("opening:",plotConfig["RESULT_PATH"]+'config.json')
    config = json.load(open(plotConfig["RESULT_PATH"]+'config.json'))
    try:
        startingGen=config["CURRENT_GENERATION"]+1
    except KeyError:
        pass
    
    lastGen=findLastGen(config["N_GENERATIONS"], plotConfig["RESULT_PATH"])

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

    if plotConfig["DIVERSITY2"]:
        diversity2(data, allGenerations, folder, step=100)





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
    else:
        best = mean = worst = std = divCnt = divMor = lastFrontX = lastFrontY = allFronts = lastFrontXLine = lastFrontYLine = allFrontsLine = None
    hypV= hypervolume(allGenerations, generationInfo, folder, plotConfig)
    
    #boxPlotStability(allGenerations, data, folder, plotConfig,config)
    return [allGenerations, hypV, best, mean, worst, std, divCnt, divMor, lastFrontX, lastFrontY, allFronts, lastFrontXLine, lastFrontYLine, allFrontsLine]

def plotMulti(runs, dirNames, location, alsoMean=True, fronts=False):
    #todo: sjekk plotConfig for hvilke plots vi skal ha. Bruker bare hypervolum i starten :)
    hypervolumeMean=None

    #todo: sjekk at alle runs[i][0] - allGenerations - er like for alle i
    # bruker den første nå:
    allGenerations = runs[0][0]

    # hyperVolume:
    name = "Multi hypervolumes or something"

    print("#### creating multi-hypervolume graph ####")
    dataIndex=1
    for i in range(len(runs)):
        #print("ruuns", runs)
        allGenerations=runs[i][0]
        plt.plot(allGenerations, runs[i][dataIndex])
    plt.title(name)
    plt.ylim(200,2800)
    print(dirNames)
    plt.legend(dirNames)
    saveAndClose(location+name, show=False)

    if alsoMean:
        # all runs need to have same number of generations!
        hyperRuns = [x[dataIndex] for x in runs]
        length=len(min(hyperRuns,key = lambda x: len(x))) ##### todo: her er du din tulling.
        name = "Average hypervolum over different runs"
        print(len(hyperRuns),length)
        hypervolumeMean=np.zeros((len(hyperRuns), length))
        for i in range(len(hyperRuns)):
            hypervolumeMean[i,:]=hyperRuns[0][0:length]
        hypervolumeMean=np.mean(hypervolumeMean, axis=0)
        allGenerations=list(range(length))
        plt.plot(allGenerations, hypervolumeMean)#np.mean(hyperRuns, axis=0))
        plt.title(name)
        plt.ylim(200,2800)
        saveAndClose(location+name, show=False)

    if fronts:
        plotMultiFronts(runs, dirNames, location, lines=True)
        plotMultiFronts(runs, dirNames, location, lines=False)



    return hypervolumeMean
    

def plotMultiConfig(data, dirNames, location):
    name="Averages hypervolum over different config runs"
    print("Making:", name)
    allGenerations = list(range(data[0].shape[0]))
    

    for i in range(len(data)):
        plt.plot(allGenerations,data[i])
    plt.legend(dirNames)
    plt.ylim(200,2800)
    plt.title(name)
    saveAndClose(location+name)

if __name__ == "__main__":

    
    root = Tk()
    #root.withdraw()
    #root.update()
    if plotConfig["RESULTS_ORIGINAL"]:
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
            if testing:
                if dir0=="0.1_0.2_0.1_0.01": continue #TODO: FJERN DENNE LINJEN

            root1, dirs1, files1 =next(os.walk(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0))
            print("newTest")
            avgHypervolumRuns =[]
            old=None
            for dir1 in dirs1:
                print("newConfig")
                print("dir1:",dir1)
                if dir1=="old": 
                    old=dirs1.index(dir1)
                    continue
                #print("her:",str(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1))
                root2, dirs2, files2 =next(os.walk(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1))
                runs = []
                notDone = None
                for dir2 in dirs2:
                    if dir2=="ikke ferdig": 
                        notDone = dirs2.index(dir2)
                        continue
                    print("ny kjøring :)"+dir2)
                    
                    #if testing:
                    #    if dir2!="Results_22.02.2022_15.33.21": continue

                    oneRun = plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1+"/"+dir2
                    plotConfig["RESULT_PATH"]=oneRun
                    if plotConfig["EACH_RESULT_ARCIVE"]:
                        oneMainRunData=plotOriginalResultsMain(plotConfig)
                        runs.append(oneMainRunData)
                        print("#######################################")
                        # allGenerations, hypV, best, mean, worst, std, divCnt, divMor, lastFrontX, lastFrontY, allFronts, lastFrontLine, allFrontsLine
                        #plotConfig["PLOT_EACH_RUN"]=False
                        root3, dirs3, files3 =next(os.walk(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1+"/"+dir2))
                        #each folder inside a run
                        for dir3 in dirs3:
                            print("subFolder",dir3)
                            if dir3=="subGen511Morph8":
                                subGen=511
                            elif dir3=="subGen1023Morph8":
                                subGen=1023
                            elif dir3=="subGen2047Morph8":
                                subGen=2047
                            elif dir3=="subGen511Morph5":
                                subGen=511
                            else: continue # for "graph"-folder

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
                                plotMulti(subRunsInd[i], legendNames[i], location=str(subRunsNames[i]), alsoMean=True, fronts=True) ### todo: her skal du fikse. Sjekk at du sender inn riktig: def plotMulti(runs, dirName, location, alsoMean=True):
                            print("plot multi is done")
                #sys.exit("Skal avsluttes")

                #here: plot multiple runs with same config
                #hypervolume over all:
                print(dirs2)
                if notDone!=None:
                    dirs2.pop(notDone)
                print(dirs2)
                if dirs2:
                    
                    avgHypervolumRuns.append(plotMulti(runs, dirs2, location=str(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1+"/")))
                ##allFrontsLine over all

                #divCnt and divMor over all

            #here: plot over mutiple configs?
            print(dirs1)
            if old!=None:
                dirs1.pop(old)
            print(dirs1)
            if dirs1:
                plotMultiConfig(avgHypervolumRuns, dirs1, location=str(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"))


