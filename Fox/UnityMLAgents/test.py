import numpy as np
import matplotlib.pyplot as plt


config = {
"POPULATION_SIZE" :4, # 64
"N_GENERATIONS" : 250, # 1064
# num params
"NUM_CONTROL_PARAMS" : 3,
}
pop = []


def diversityMeasure(pop, config):
    """
    simple diversity measure between control/morph parameters in this generation
    Sum the euclidean distance between all control/morph parameters
    """

    # makes numpy array with parameters
    cntNumpy = np.zeros((config["POPULATION_SIZE"],config["NUM_CONTROL_PARAMS"]))
    for i in range(config["POPULATION_SIZE"]):
        cntNumpy[i]=pop[i]

    totalDistCnt=0
    numCalulations=0
    for i in range(config["POPULATION_SIZE"]):
        for j in range(config["POPULATION_SIZE"]):
            if i!=j:
                numCalulations+=1
                totalDistCnt+=np.linalg.norm(cntNumpy[i]-cntNumpy[j])

    return totalDistCnt


for i in range(config["POPULATION_SIZE"]):
    a = [0]*config["NUM_CONTROL_PARAMS"]
    pop.append(a)

pop[0]= [0.5,0.5,0]
print(pop)
print(diversityMeasure(pop,config))

print("#########")

pop[0]= [0.8,0,0]
print(pop)
print(diversityMeasure(pop,config))