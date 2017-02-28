import random
import matlab_scripts
import copy


class Solution: #should be called Solution

    def __init__(self,customers,depots,m,t):
        #check if hard/shallow copy
        self.customers = copy.deepcopy(customers)
        self.depots = copy.deepcopy(depots)
        # set a feasible grouping of customers
        while True:
            feasible = True


            # Set vehicle accordingly, each customer has a depot. Should also have a vehicle.
            for customer in self.customers:
                dist = []
                for depot in self.depots:
                    dist.append( (distance(depot,customer),depot) )
                dist.sort()
                dist[0][1].customer_list.append(customer)

            for i, depot in enumerate(self.depots):

                demand = [c.q for c in depot.customer_list]

                if (sum(demand) > m * depot.Q):
                    print demand
                    print sum(demand)
                    feasible = False

            if feasible:  # all depots within weightlimit, IF ONE CAN HAVE ONLY ONE ROUTE PER VEHICLE
                break
            else:
                print "New try!"

        for depot in self.depots:
            depot.init_route()

        self.duration,self.vehicles = self.duration_and_vehicles()

    def fitness(self):
        alpha = 100000
        beta = 1
        fitness = alpha*float(self.vehicles) + beta*self.duration
        return fitness

    def duration_and_vehicles(self):

        vehicles = 0
        duration = 0
        for depot in self.depots:
            for vehicle_num, route in depot.vehicle_dict.items():
                if route != []:
                    vehicles += 1
                    duration += depot.route_length(route)
                    duration += distance(depot,route[0]) #distance from depot to first customer
                    duration += distance(depot,route[-1]) #distance from depot to last customer


        return duration,vehicles

    def remove_customers(self,customers):
        for depot in self.depots:
            for veh,route in depot.vehicle_dict.items():
                for stop in route:
                    for customer in customers:
                        if customer.x == stop.x and customer.y == stop.y:
                            route.remove(stop)
                            break

    def insert_customers(self,customers,depot):
        if depot in self.depots:
            for customer in customers:
                cost = depot.get_insertion_costs(customer)

                cost.sort()

                k = random.random()

                if(k <=0.8):
                    for placement in cost:
                        #placement is a tuple with cost,index,vehicle and feasibility
                        if(placement[3]):
                            depot.insert_in_route(customer,placement[2],placement[1])
                            break
                else:
                    depot.insert_in_route(customer, cost[0][2], cost[0][1])





        else:
            print "Oh shit!"

    def plot_sol(self,eng):
        for depot in self.depots:
            matlab_scripts.plot_routes(eng,depot)




def distance(c_1, c_2):
    return ((c_1.x - c_2.x) ** 2 + (c_1.y - c_2.y) ** 2) ** 0.5

'''
def optimized_travelling_salesman(points, start):
    #http://codereview.stackexchange.com/questions/81865/travelling-salesman-using-brute-force-and-heuristics
    must_visit = points
    path = [start]
    while must_visit:
        nearest = min(must_visit, key=lambda x: distance(path[-1], x))
        path.append(nearest)
        must_visit.remove(nearest)
    path.append(start)
    return path
'''


