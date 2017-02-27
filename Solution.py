import random
import matlab_scripts
import copy


class Solution: #should be called Solution

    def __init__(self,customers,depots,m):
        #check if hard/shallow copy
        self.customers = copy.deepcopy(customers)
        self.depots = copy.deepcopy(depots)
        # set a feasible grouping of customers
        while True:
            feasible = True
            customer_depot_group = [random.randrange(len(self.depots)) for i in range(len(self.customers))]
            # Set vehicle accordingly, each customer has a depot. Should also have a vehicle.

            for i, depot in enumerate(self.depots):
                depot.customer_list = [self.customers[j] for j in range(len(customer_depot_group)) if
                                       customer_depot_group[j] == i]
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
        alpha = 100
        beta = 0.001
        fitness = alpha*self.vehicles + beta*self.duration
        return fitness

    def duration_and_vehicles(self):

        vehicles = 0
        total_distance = 0
        customer_duration = 0
        for depot in self.depots:
            for vehicle_num, route in depot.vehicle_dict.items():
                if route != []:
                    vehicles = vehicles +1

                    route_len = len(route)
                    route_distance = distance(depot,route[0])
                    if (route_len > 1):
                        for i in range(route_len - 1):
                            route_distance += distance( route[i], route[i+1])
                            customer_duration += route[i].d
                    route_distance += distance(route[route_len-1], depot)
                    total_distance += route_distance

        return total_distance+customer_duration,vehicles

    def remove_customers(self,customers):
        for veh,route in self.depots.items():
            for customer in customers:
                for stop in route:
                    if customer.x == stop.x and customer.y == stop.y:
                        route.remove(stop)
                        break

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


