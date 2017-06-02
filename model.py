import pygame
import pymunk
import numpy as np
import enum
import math

import parameters
from creature import Creature
from genetic_algorithm import GeneticAlgorithm


class Model:
    def __init__(self, clock):
        self.clock = clock
        self.total_time_ms = 0
        self.simulation = SimulationModel(self)


class SimulationModel:

    class State(enum.Enum):
        POPULATED = 0
        RUNNING = 1
        EVOLVED = 2
        WAITING = 3
        QUITTING = 4

    def __init__(self, model):
        self.__model = model

        self.delta_time = 0
        self.simulation_time_ms = 0
        self.state = SimulationModel.State.POPULATED

        self.r_world = pygame.rect.Rect(0, 0, 1000, 1000)

        # pymunk
        self.space = None

        self.creatures = list()
        self.gen_algo = None

    @property
    def clock(self):
        return self.__model.clock

    def construct(self):
        self.gen_algo = GeneticAlgorithm(Creature.gene_size())
        self.__create_space()
        self.__generate_creatures()

    def apply_ga(self):
        self.gen_algo.compute(self.creatures)
        self.__create_space()
        self.__generate_creatures()

    def __create_space(self):
        del self.space
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 0.0)
        self.space.damping = 0.1  # lose 1-x% of its velocity per second

    def __generate_creatures(self):

        del self.creatures[:]

        for gene in self.gen_algo.genes:
            gene[0] = 10
            gene[1] = 180
            gene[2] = 4

        for i in range(parameters.N_POPULATION):
            pos = (np.random.randint(0, self.r_world.width), np.random.randint(0, self.r_world.height))
            angle = math.radians(np.random.randint(-180, 180))
            self.creatures.append(Creature(self.space, pos, angle, self.gen_algo.genes[i]))
