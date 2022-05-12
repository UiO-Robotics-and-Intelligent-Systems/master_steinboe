from deap import creator
from deap import base

from Individual import WaveIndividual

creator.create("FitnessMin", base.Fitness, weights=(1.0,1.0)) # Maximization and minimization are taken care off by a multiplication between the weights and the fitness values.
creator.create("Individual", WaveIndividual, fitness=creator.FitnessMin)