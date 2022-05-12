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
from loess.loess_1d import loess_1d
from statsmodels.nonparametric.smoothers_lowess import lowess as  sm_lowess


random.seed(98765432) # only for colors

testing = False #todo: fjern
plotConfig ={
    "ONLY_RUNDATA" : True,
    "OVERWRITE_RUNDATA":False,
    
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

    "STABILITY_LIM" : -7.5,
    "DISTANCE_LIM" : None,

    "GENERATIONS" : 4096, # TODO! 
    "POP_SIZE" : 256,
}

if testing:
    plotConfig["GENERATIONS"]=100   

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


print(plotConfig["COLOR_ARRAY"])

print(plotConfig["COLOR_ARRAY"].shape)



if platform.system()=='Windows': 
    plotConfig["RESULTS_PATH_ORIGINAL"]="C:/Users/stein/Documents/Unity/results/"
    plotConfig["RESULTS_PATH_ARCHIVE"]="C:/Users/stein/Documents/Unity/resultsArchive/"
elif platform.system()=='Linux':
    plotConfig["RESULTS_PATH_ORIGINAL"] = "/uio/hume/student-u01/steinboe/Documents/master/MasterThesis/results"
else:
    sys.exit("what?")



def saveAndClose(location, show=False):

    plt.savefig(location,dpi=300)
    #if show:
    #    plt.show()
    plt.close()
    plt.figure() # do I need this?



def sortData(runData, plotConfig, dMax=100000, dMin=0, sMax=100000, sMin=0):
        # ind_i = data[run_index][individual_i]  ind_i[0]=list of cntParams, ind_i[1]=morph params, ind_i[2]=fitness [distance, stability]
    
    morParams = plotConfig["NUM_MORPHOLOGY_PARAMS"]
    cntParams = plotConfig["NUM_CONTROL_PARAMS"]
    runs = len(runData)
    plotConfig["NUM_RUNS"]=runs
    popSize=plotConfig["POP_SIZE"]

    dataMorP=[]
    dataCntP=[]
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

            for mor_i in range(morParams):
                morParamV=ind[1][mor_i]
                dataMorP[mor_i].append([morParamV,fitDist])
                #dataMorP[mor_i,run_i,ind_i]=[morParamV, fitDist]

            for cnt_i in range(cntParams):
                cntParamV=ind[0][cnt_i]
                dataCntP[cnt_i].append([cntParamV,fitDist])
                #dataCntP[cnt_i,run_i,ind_i]=[cntParamV, fitDist]


    dataMorP=np.asarray(dataMorP) #dataMorP.reshape(morParams,runs*popSize,2)
    dataCntP=np.asarray(dataCntP) #dataCntP.reshape(cntParams,runs*popSize,2)

    print(dataMorP.shape)
    print(dataCntP.shape)

    return dataMorP, dataCntP, plotConfig


def plotMultiScatterParams(dataMorP, dataCntP, plotConfig, location):

    print("plotMultiScatter")
    morParams = plotConfig["NUM_MORPHOLOGY_PARAMS"]
    cntParams = plotConfig["NUM_CONTROL_PARAMS"]

    for mor_i in range(morParams): #one plot, save
        plt.scatter(dataMorP[mor_i,:,0],dataMorP[mor_i,:,1],alpha=0.1,s=20, edgecolors='none',c='b')

        #save and stuff
        name="Morphology param "+str(mor_i)+" for last generation over all runs"
        plt.xlim((-1.1,1.1))
        plt.ylim((-2,60))
        plt.xlabel("Parameter value")
        plt.ylabel("Fitness(distance)")
        plt.title(name)
        saveAndClose(location+name, show=plotConfig["VIEW_GRAPH"])

    for cnt_i in range(cntParams): #one plot, save
        plt.scatter(dataCntP[cnt_i,:,0],dataCntP[cnt_i,:,1],alpha=0.1,s=20, edgecolors='none',c='b')

        #save and stuff
        name="Control param "+str(cnt_i)+" for last generation over all runs"
        plt.xlim((-1.1,1.1))
        plt.ylim((-2,60))
        plt.xlabel("Parameter value")
        plt.ylabel("Fitness(distance)")
        plt.title(name)
        saveAndClose(location+name, show=plotConfig["VIEW_GRAPH"])

def plotKernalDensityEstimate(data, name, plotConfig, location):
    print("plotKernalDensityEstimate")
    
    for i in range(len(data)):
        x = (data[i][:,0]+1)/2     # -1-1 -> 0-2 -> 0-1 
        y = data[i][:,1]/100 # 0-70 -> 0-1(0.7)
        #dataMorP and dataCntP in on shape: (x,2)
        xmin, xmax = -0.08, 1.08 # todo
        ymin, ymax = -0.08, 0.60
        
        # Peform the kernel density estimate
        xx, yy = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
        positions = np.vstack([xx.ravel(), yy.ravel()])
        values = np.vstack([x, y])
        kernel = st.gaussian_kde(values)
        f = np.reshape(kernel(positions).T, xx.shape)

        plt.close()
        fig = plt.figure()
        ax = fig.gca()
        #ax.set_xlim(xmin, xmax)
        #ax.set_ylim(ymin, ymax)

        # Contourf plot
        #cfset = ax.contourf(xx, yy, f, cmap='Reds')
        ## Or kernel density estimate plot instead of the contourf plot
        ax.imshow(np.rot90(f), cmap='Reds', extent=[xmin, xmax, ymin, ymax])

        # Contour plot
        cset = ax.contour(xx, yy, f, colors='k',linewidths=0.5)
        # Label plot
        ax.clabel(cset, inline=1, fontsize=7)
        ax.set_xlabel("Parameter value (-1 to 1) -> (0 to 1)")
        ax.set_ylabel("Fitness (distance) *10^-3")
        plt.title(name+str(i))
        #plt.figure()
        #plt.xlim(xmin, xmax)
        #plt.ylim(ymin, ymax)
        plt.scatter(x,y,alpha=0.1,s=20, edgecolors='none',c='b')
        saveAndClose(location+name+str(i), show=plotConfig["VIEW_GRAPH"])

def plotLoess(data, name, plotConfig, location):
    print("plotting loess")
    for i in range(len(data)):
        x = data[i][:,0]   
        y = data[i][:,1]
    
        plt.scatter(x,y,alpha=0.1,s=20, edgecolors='none',c='b')

        #save and stuff
        plt.xlim((-1.1,1.1))
        plt.ylim((-2,60))
        plt.xlabel("Parameter value")
        plt.ylabel("Fitness(distance)")
        plt.title(name+str(i))

        # loess
        ## Sort only for plotting smooth lines
        #j = np.argsort(y)
        #x, y = x[j], y[j]

        ## lower franc = more accurate/more detailed. Higher franc = roligere
        #yout, xout, weights = loess_1d(y, x, frac=0.5, degree=1) #
        #plt.plot(xout,yout, label='LOESS')

        # sm_loess # bytt x og y for å bytte retning (både input og output)
        sm_y, sm_x = sm_lowess(x, y,  frac=0.2, it=5, return_sorted = True).T
        plt.plot(sm_x, sm_y, color='tomato',label="sm_lowess", linewidth=0.8)

        plt.legend()

        saveAndClose(location+name+str(i), show=plotConfig["VIEW_GRAPH"])
        
def loadRunData(plotConfig, location):
    print("Run data only. Opening runData.json at",location)
    f=open(location+'runData.json')
    s=time.time()
    data = json.load(f)
    print("time to open:",time.time()-s)

    #dataMorP, dataCntP, plotConfig = sortData(data,plotConfig, sMax=-7.5)

    #plotMultiScatterParams(dataMorP, dataCntP, plotConfig,location)
    
    dataMorP, dataCntP, plotConfig = sortData(data,plotConfig, sMax=-7.5, dMin=5)


    #name = "Kernal density estimatation for morphology param"
    #plotKernalDensityEstimate(dataMorP, name, plotConfig, location)
    #name = "Kernal density estimatation for controll param"
    #plotKernalDensityEstimate(dataCntP, name, plotConfig,location)

    name = "Loess on morphology param"
    plotLoess(dataMorP,name,plotConfig,location)
    #name = "Loess on controll param"
    #plotLoess(dataCntP,name,plotConfig, location)



if __name__ == "__main__":
    

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
                    if dir1!= "256_1.0_0.02_0.0_0.02": continue 

                legendNamesConfig.append(dir1)
                if plotConfig["ONLY_RUNDATA"]:
                    loadRunData(plotConfig, location=str(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1+"/"))
                    continue

