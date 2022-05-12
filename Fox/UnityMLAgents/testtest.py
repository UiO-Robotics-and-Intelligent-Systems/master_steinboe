from email import generator
from tkinter import Toplevel
from deap import base
from deap import tools
from deap import creator
import matplotlib.pyplot as plt

class ind:
    def __init__(self,input):
        self.v=input

def f(dataset):
    x=[d[0] for d in dataset]
    y=[d[1] for d in dataset]

    return x,y

creator.create("FitnessMin", base.Fitness, weights=(-1.0,-1.0)) # Maximization and minimization are taken care off by a multiplication between the weights and the fitness values.
creator.create("Individual", ind, fitness=creator.FitnessMin)


toolbox = base.Toolbox()        
toolbox.register("parentSelection", tools.selTournamentDCD)
toolbox.register("survivalSelection", tools.selNSGA2)
popSize=4

# This is just to assign the crowding distance to the individuals # no actual selection is done. # "Having the size of individuals equals to k will have no effect other than sorting the population according to their front rank."
# self.pop = self.toolbox.survivalSelection(self.pop, len(self.pop))

oldPopANDoffspringFit=[(8.27000617980957, -13.241970293612209), (3.912163734436035, -4.379827378342773), (5.648721218109131, -5.345638153954756), (7.54389762878418, -11.800276094344966),
(8.27000617980957, -13.241970293612209), (0.41259461641311646, -4.850079051801106), (3.912163734436035, -4.379827378342773), (4.857638835906982, -11.077436068594846)]

oldPopFit= [(8.27000617980957, -13.241970293612209), (3.912163734436035, -4.379827378342773), (5.648721218109131, -5.345638153954756), (7.54389762878418, -11.800276094344966)]
offspringFit= [(8.27000617980957, -13.241970293612209), (0.41259461641311646, -4.850079051801106), (3.912163734436035, -4.379827378342773), (4.857638835906982, -11.077436068594846)]

#pop=[(8.27000617980957, -13.241970293612209), (8.27000617980957, -13.241970293612209), (3.912163734436035, -4.379827378342773), (3.912163734436035, -4.379827378342773)]

def generatorThing(x):
    return [x]


toolbox.register("generatorThing", generatorThing, 1)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.generatorThing)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


oldPop = toolbox.population(n=popSize)
for i in range(popSize):
    oldPop[i].fitness.values=oldPopFit[i]
# assigning crowdin distance
oldPop=toolbox.survivalSelection(oldPop, popSize)


#step
offspring = toolbox.parentSelection(oldPop, len(oldPop))
offspring = [toolbox.clone(ind) for ind in offspring]

for i in range(popSize):
    offspring[i].fitness.values=offspringFit[i]
#offspring=toolbox.survivalSelection(offspring, popSize)

print("oldPop:", oldPop)
print("offspring:", offspring)
print("oldPop and offspring:", oldPop+offspring)


newPop = toolbox.survivalSelection(oldPop + offspring, popSize)
newPop = toolbox.parentSelection(newPop, len(newPop))

newPopFit = [x.fitness.values for x in newPop]
print(newPopFit)


oldPopX, oldPopY = f(oldPopFit)
offspringX,offspringY=f(offspringFit)
newPopX,newPopY=f(newPopFit)

plt.plot(oldPopX, oldPopY,marker="o")
plt.plot(offspringX,offspringY, marker="1")
plt.plot(newPopX,newPopY, marker="2")
plt.legend(["oldPop","offspring","newPop"])
plt.show()

# Er det noe feil med crounding distanse i plotten du lagret? Derfor de ikke blir valgt? Lag denne file orntlig og sjekk det ut.