import random
import math
import Solution
import copy

class Population:

    def __init__(self,customers, depots, m,t, population_size):
        self.solutions = []
        self.N = population_size
        self.eng = None         #Matlab-engine for plot
        for i in range(self.N):
            self.solutions.append(Solution.Solution(customers,depots,m,t))

        self.sort_solutions()

        self.best_solution = self.solutions[0]
        self.best_duration = self.best_solution.duration_and_vehicles()

    def set_eng(self,eng):
        self.eng = eng

    def sort_solutions(self):
        self.solutions.sort(key=lambda x: x.duration)


    def selection(self):
        #Step 1
        random.shuffle(self.solutions)


        offspring = []
        i = 0
        while (True):
            #print "i",i
            #Step 2
            p_1 = NPGA_Tournament(self.solutions,offspring,i)

            #Step 3
            i += 2
            p_2 = NPGA_Tournament(self.solutions,offspring,i)


            #Step 4, crossover p_1,p_2 = c_1,c_2 mutate c_1,c_2
            c_1,c_2 = self.crossover(p_1,p_2)


            #Step 5, add c_1,c_2 to offspring
            offspring.append(c_1)
            offspring.append(c_2)

            #Step 6
            i +=1
            if(i < self.N-1):

                if(len(offspring)==self.N/2):
                    #print "Shuffling!!!!!!!"
                    random.shuffle(self.solutions)
                    i=0

            if(len(offspring)==self.N):
                #print "BREAK!"
                break

        #for child in offspring:
        #   print child.duration_and_vehicles()

        self.solutions = self.solutions +offspring

        self.sort_solutions()
        for sol in self.solutions:
            for depot in sol.depots:
                depot.clean()
            if(sol.infeasible_count()==0):
                pop_best_dur,veh = sol.duration_and_vehicles()

                if(pop_best_dur< self.best_duration):
                    print "Best:", pop_best_dur
                    self.best_solution = sol
                    self.best_duration = pop_best_dur
                break



        self.solutions = self.solutions[:self.N]


    def crossover(self,p_1,p_2):
        c_1, c_2 = copy.deepcopy(p_1), copy.deepcopy(p_2)

        #Find depot
        depot_c_1 = random.choice(c_1.depots)
        depot_c_2 = None
        for depot in c_2.depots:
            if(depot.x == depot_c_1.x ) and (depot.y == depot_c_1.y ):
                depot_c_2 = depot
                break

        if (depot_c_2 == None):
            print "Failed to find p_2s depot"
            return None,None

        #make space for crossover
        if (depot_c_1.vehicle_dict.keys() != []) and (depot_c_2.vehicle_dict.keys() != []):
            vehicle_1 = random.choice(depot_c_1.vehicle_dict.keys())
            route_1 = depot_c_1.vehicle_dict[vehicle_1]


            vehicle_2 = random.choice(depot_c_2.vehicle_dict.keys())
            route_2 = depot_c_2.vehicle_dict[vehicle_2]


            #insert crossover
            c_1.move_customers(route_2,depot_c_1)
            c_2.move_customers(route_1,depot_c_2)

        return c_1,c_2

def NPGA_Tournament(parents,offspring,i):
    sub_pop = random.sample(parents, 2)
    #print "i",i,"par_len",len(parents)

    #print parents
    try:
        sol_1,sol_2 = parents[i],parents[i+1]
    except IndexError:
        print "wrong in NPGA Tournament",i
    #print sol_1,sol_2
    #print sub_pop
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
    pool.sort(key=lambda x: x.fitness())

    #Cange to hamming distance?
    f_min = pool[0].fitness()
    f_max = pool[-1].fitness()

    if (f_min == f_max):
        print "Noooo!"

    f_1 = p_1.fitness()
    f_2 = p_2.fitness()
    sigma_share = 0.5
    for child in pool:
        try:
            distance_1 = math.sqrt( ((f_1-child.fitness()) / (f_max-f_min))**2 ) #May need to change this
            distance_2 = math.sqrt( ((f_2-child.fitness()) / (f_max-f_min))**2 ) #May need to change this
        except ZeroDivisionError:
            #all elements in pool have same fitness

            #print "Zero-div",len(pool),pool[0].fitness(),pool[-1].fitness()
            #print pool[0].duration_and_vehicles(),pool[-1].duration_and_vehicles(), p_1.duration_and_vehicles()
            distance_1 = 0
            distance_2 = 0

        sh_1, sh_2= 0,0

        if(distance_1< sigma_share ):
            sh_1 = 1 -(distance_1/sigma_share)

        if (distance_2 < sigma_share):
            sh_2 = 1 - (distance_2 / sigma_share)

        nc_1 += sh_1
        nc_2 += sh_2


    return nc_1,nc_2


