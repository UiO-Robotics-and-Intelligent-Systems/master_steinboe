from turtle import distance
import numpy as np
import os
import platform
import sys
import json
import time
plotConfig ={
    "HYPERVOLUME_REF" :(0,-50),
    "HYPERVOLUME_NEW_REF" :(0,-50),
    "CHOOSE_DIR": False,
    "RESULTS_ARCHIVE" : True,
    "EACH_SUB_FOLDER" : False,
    "DIVERSITY2" : True, # todo! Denne må kunne kjøres. copier data eller noe I think. eller sorter før du sender inn. Sorter for alleeee.
    "NUM_CONTROL_PARAMS" : 18,
    "NUM_MORPHOLOGY_PARAMS" : 6,

    "STABILITY_LIM" : -7.5,
    "DISTANCE_LIM" : None
}

if platform.system()=='Windows': 
    plotConfig["RESULTS_PATH_ORIGINAL"]="C:/Users/stein/Documents/Unity/results/"
    plotConfig["RESULTS_PATH_ARCHIVE"]="C:/Users/stein/Documents/Unity/resultsArchive/"
elif platform.system()=='Linux':
    plotConfig["RESULTS_PATH_ORIGINAL"] = "/uio/hume/student-u01/steinboe/Documents/master/MasterThesis/results"
else:
    sys.exit("what?")

testing=False

def area(a,b):
    c=(b[0]-a[0], b[1]-a[1])
    return c[0]*c[1]

def hypervolume(ref, pointset, distanceLim=None, stabilityLim=None):
    """
    Calculating hypervolume
    """
    sum=0
    for i in range(len(pointset)):
        #check limits
        if stabilityLim != None:
            if abs(stabilityLim)<abs(pointset[i][1]):
                #print("break, because of stabilityLim")
                break
        if distanceLim != None:
            if abs(distanceLim)<abs(pointset[i][0]):
                #print("break, because of distanceLim")
                break

        sum+=area(ref,pointset[i])
        ref=(pointset[i][0],ref[1])
    return sum


def editRun(path):
    print("editRun", path)
    root, dirs, files =next(os.walk(path))
    for file in files:
        #print(file)
        if file != "config.json":
            with open(path+file, 'r+') as f:
                data=json.load(f)
                info=data["info"]
                #eval=data["Eval"]
                #config=data["config"]
                paretoFront=info["ParetoFront"]
                #assert info["Hypervolume"] == hypervolume(plotConfig["HYPERVOLUME_REF"],paretoFront)
                
                if plotConfig["DISTANCE_LIM"]==None and plotConfig["STABILITY_LIM"]!= None:
                    # REDUCING TIME
                    if abs(plotConfig["STABILITY_LIM"])>abs(paretoFront[-1][1]):
                        info["New Hypervolume"] = info["Hypervolume"]
                    else:
                        info["New Hypervolume"]=hypervolume(plotConfig["HYPERVOLUME_NEW_REF"], paretoFront, stabilityLim=plotConfig["STABILITY_LIM"])
                else:
                    sys.exit("not implemented for this this option")


                f.seek(0)
                json.dump(data,f, indent=2)
    

 
def resultsLoop():
    start=time.time()
    if plotConfig["RESULTS_ARCHIVE"]:
        root0, dirs0, files0 =next(os.walk(plotConfig["RESULTS_PATH_ARCHIVE"]))
        for dir0 in dirs0:
            if dir0=="old": continue
            #if testing:
            if dir0!="Fox": continue #TODO: FJERN DENNE LINJEN
            root1, dirs1, files1 =next(os.walk(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0))
            print("newTest")
            for dir1 in dirs1:
                print("newConfig")
                print("dir1:",dir1)
                if dir1=="old": 
                    old=dirs1.index(dir1)
                    continue
                if testing:
                    if dir1!="256_1.0_0.06_0.1_0.02": continue

                root2, dirs2, files2 =next(os.walk(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1))
                for dir2 in dirs2:
                    if dir2=="ikke ferdig": continue
                    print("ny kjøring :)"+dir2)
                    
                    #if testing:
                    if not (dir2=="Results_27.03.2022_21.10.18" or dir2=="Results_27.03.2022_21.10.17" or dir2=="Results_27.03.2022_23.13.01"): continue

                    oneRun = plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1+"/"+dir2+"/"
                    plotConfig["RESULT_PATH"]=oneRun

                    #####################
                    editRun(oneRun)
                    print("time so far:", time.time()-start)
                    #sys.exit("en kjøring er ferdig, ble det riktig?")
                    if plotConfig["EACH_SUB_FOLDER"]:
                        root3, dirs3, files3 =next(os.walk(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1+"/"+dir2))
                        #each folder inside a run
                        for dir3 in dirs3:
                            print("subFolder",dir3)
                            if dir3=='graphs': continue

                            root4, dirs4, files4 =next(os.walk(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1+"/"+dir2+"/"+dir3))
                            for dir4 in dirs4:
                                root5, dirs5, files5 =next(os.walk(plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1+"/"+dir2+"/"+dir3+"/"+dir4))
                                for dir5 in dirs5:
                                    print("one subRun", dir5)
                                    oneSubRun = plotConfig["RESULTS_PATH_ARCHIVE"]+dir0+"/"+dir1+"/"+dir2+"/"+dir3+"/"+dir4+"/"+dir5+"/"
                                    ##############################
                                    editRun(oneSubRun)
                    

if __name__ == "__main__":
    resultsLoop()
    #editRun("C:/Users/stein/Desktop/testingThing/")