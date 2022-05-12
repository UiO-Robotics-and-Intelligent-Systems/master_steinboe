import time
import random
import numpy as np

random.seed(69)

popSize=64
listSize=10
def dist(a,b):
    return np.linalg.norm(a-b)


pop1 = np.random.randint(30,size=(popSize, listSize))
pop1=pop1.tolist()
totalDist=0
e=0
s1=time.time()
pop=np.array(pop1)
print(pop.shape)

#print(type(pop), pop.shape)
for i in range(popSize):
    for j in range(i,popSize):
        if i!=j:
            e+=1
            totalDist+=dist(pop[i],pop[j])
print("time:",time.time()-s1)
d=totalDist/e
print(d)

