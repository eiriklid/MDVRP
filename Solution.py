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
                #get distance to each depot
                for depot in self.depots:
                    dist.append( (distance(depot,customer),depot) )
                dist.sort()
                #choose closest depot
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

        self.update_duration_and_vehicle()
    def fitness(self):
        self.update_duration_and_vehicle()
        alpha = 10000
        beta = 1
        fitness = alpha*float(self.vehicles) + beta*self.duration + 100*float(self.infeasible_count())
        return fitness

    def duration_and_vehicles(self):

        vehicles = 0
        duration = 0
        for depot in self.depots:
            for vehicle_num, route in depot.vehicle_dict.items():
                if route != []:
                    vehicles += 1
                    duration += depot.route_length(route)


        return duration,vehicles

    def update_duration_and_vehicle(self):
        self.duration, self.vehicles = self.duration_and_vehicles()

    def remove_customer(self,customer):
            removed = False
            for depot in self.depots:
                if not removed:
                    for veh,route in depot.vehicle_dict.items():
                        for stop in route:
                            if customer.x == stop.x and customer.y == stop.y:
                                route.remove(stop)
                                removed = True
                                break
                        if removed:
                            break

            if not removed:
                print "Not removed", customer


    def insert_customers(self,customers,depot):
        if depot in self.depots:
            for customer in customers:
                cost = depot.get_insertion_costs(customer)

                cost.sort()

                k = random.random()

                if(k <=0.8):
                    placed = False
                    for placement in cost:
                        #placement is a tuple with cost,index,vehicle and feasibility
                        if(placement[3]):
                            placed = True
                            depot.insert_in_route(customer,placement[2],placement[1])
                            break
                    if not placed:
                        depot.make_new_route(customer)

                else:
                    try:
                        depot.insert_in_route(customer, cost[0][2], cost[0][1])
                    except IndexError:
                        print
                        print "cost-error:",cost, "depot",depot
                        for error_depot in self.depots:
                            for veh, route in error_depot.vehicle_dict.items():
                                print veh, route


        else:
            print "Oh shit!"


    def infeasible_count(self):
        infeasibles = 0
        customers = []
        for depot in self.depots:
            infeasibles += len(depot.infeasible_routes())

        return infeasibles

    def plot_sol(self,eng):
        for i,depot in enumerate(self.depots):
            #print "Depot:",i
            matlab_scripts.plot_routes(eng,depot)

    def make_file(self,name):
        self.update_duration_and_vehicle()
        f = open(name,'w')
        f.write("{0:.2f}".format(self.duration)+ '\n')
        for j,depot in enumerate(self.depots):
            for veh, route in depot.vehicle_dict.items():
                customers = [0]
                for customer in route:
                    customers.append(customer.i)
                customers.append(0)
                c_str = '\t'.join([str(x) for x in customers])
                f.write(str(j+1)+"\t"+str(veh)+ "\t{0:.2f}\t".format(depot.route_length(route)) + str(depot.route_load(route))+'\t '+ c_str+ '\n')





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


