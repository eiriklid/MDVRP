import random

import Solution

class Population:

    def __init__(self,customers, depots, m, population_size):

        self.solutions = []

        for i in range(population_size):
            self.solutions.append(Solution.Solution(customers,depots,m))

        self.sort_solutions()

        self.best_solution = self.solutions[0]

    def sort_solutions(self):
        self.solutions.sort(key=lambda x: x.fitness_and_duration())


    def selection(self):
        random.shuffle(self.solutions)

        selected = self.solutions[:2]
        print selected

def NPGA_Tournament(sol_1, sol_2, parents):
    sub_pop = random.sample(parents, 2)

