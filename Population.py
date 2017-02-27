import random
import math
import Solution

class Population:

    def __init__(self,customers, depots, m, population_size):

        self.solutions = []
        self.N = population_size
        self.eng = None         #Matlab-engine for plot
        for i in range(self.N):
            self.solutions.append(Solution.Solution(customers,depots,m))

        self.sort_solutions()

        self.best_solution = self.solutions[0]

    def set_eng(self,eng):
        self.eng = eng

    def sort_solutions(self):
        self.solutions.sort(key=lambda x: x.duration)


    def selection(self):
        #Step 1
        random.shuffle(self.solutions)

        for sol in self.solutions:
            print sol.fitness()

        offspring = []
        i = 0
        while(i<self.N):
            #Step 2
            p_1 = NPGA_Tournament(self.solutions,offspring,i)

            #Step 3
            i += 2
            p_2 = NPGA_Tournament(self.solutions,offspring,i)

            #Step 4, crossover p_1,p_2 = c_1,c_2 mutate c_1,c_2

            #Step 5, add c_1,c_2 to offspring

            #Step 6
            i +=1
            if(len(offspring)==self.N/2):
                print "Shuffling!!!!!!!"
                random.shuffle(self.solutions)
                i=0
            else:
                print len(offspring), self.N/2


def NPGA_Tournament(parents,offspring,i):
    sub_pop = random.sample(parents, 2)
    print parents
    sol_1,sol_2 = parents[i],parents[i+1]
    print sol_1,sol_2
    print sub_pop
    winner_1 = True
    winner_2 = True

    for sub_sol in sub_pop:
        if((sub_sol.duration< sol_1.duration) or (sub_sol.vehicles< sol_1.vehicles)):
            winner_1 = False

        if ((sub_sol.duration < sol_2.duration) or (sub_sol.vehicles < sol_2.vehicles)):
            winner_2 = False

    #Scenario 1
    if(winner_1):
        if not (winner_2):
            return sol_1

    elif(winner_2):
        if not (winner_1):
            return sol_2
    #Scenario 2
    #Check with offspring Q
    if(len(offspring)>2):
        nc_1, nc_2 = get_niche_counts(sol_1,sol_2,offspring)
        if (nc_1 < nc_2):
            return sol_1
        else:
            return sol_2
    else:
        return random.choice([sol_1,sol_2])


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


