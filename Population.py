import random
import math
import Solution

class Population:

    def __init__(self,customers, depots, m, population_size):

        self.solutions = []

        for i in range(population_size):
            self.solutions.append(Solution.Solution(customers,depots,m))

        self.sort_solutions()

        self.best_solution = self.solutions[0]

    def sort_solutions(self):
        self.solutions.sort(key=lambda x: x.duration)


    def selection(self):
        random.shuffle(self.solutions)


        offspring = []
        i = 0
        while(True):
            p_1 = NPGA_Tournament(self.solutions,offspring,i)
            i += 2
            p_2 = NPGA_Tournament(self.solutions,offspring,i)




def NPGA_Tournament(parents,offspring,i):
    sub_pop = random.sample(parents, 2)
    p_1,p_2 = parents[i],parents[i+1]
    winner_1 = True
    winner_2 = True

    for sub_sol in sub_pop:
        if((sub_sol.duration< p_1.duration) or (sub_sol.vehicles< p_1.vehicles)):
            winner_1 = False

        if ((sub_sol.duration < p_2.duration) or (sub_sol.vehicles < p_2.vehicles)):
            winner_2 = False

    #Scenario 1
    if(winner_1):
        if not (winner_2):
            return p_1

    elif(winner_2):
        if not (winner_1):
            return p_2
    #Scenario 2
    #Check with offspring Q
    if(len(offspring)>2):
        nc_1, nc_2 = get_niche_counts(p_1,p_2,offspring)
        if (nc_1 < nc_2):
            return p_1
        else:
            return p_2
    else:
        return random.choice([p_1,p_2])


def get_niche_counts(p_1,p_2,offspring):
    nc_1,nc_2 = 0,0
    pool = offspring + [p_1,p_2]
    print pool
    pool.sort(key=lambda x: x.fitness())

    #Cange to hamming distance?
    f_min = pool[0].fitness()
    f_max = pool[-1].fitness()
    f_1 = p_1.fitness()
    f_2 = p_2.fitness()
    sigma_share = 0.5
    for child in pool:
        distance_1 = math.sqrt( ((f_1-child.fitness()) / (f_max-f_min))**2 ) #May need to change this
        distance_2 = math.sqrt( ((f_2-child.fitness()) / (f_max-f_min))**2 ) #May need to change this

        sh_1, sh_2= 0,0

        if(distance_1< sigma_share ):
            sh_1 = 1 -(distance_1/sigma_share)

        if (distance_2 < sigma_share):
            sh_2 = 1 - (distance_2 / sigma_share)

        nc_1 += sh_1
        nc_2 += sh_2

    return nc_1,nc_2


