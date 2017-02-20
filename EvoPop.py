import random

class EvoPop:

    def __init__(self,customers,depots,m):
        #check if hard/shallow copy
        self.customers = customers
        self.depots = depots
        #set a feasible grouping of customers
        while True:
            feasible =  True
            customer_depot = [random.randrange(len(depots)) for i in range(len(customers))]

            for i,depot in enumerate(depots):

                depot.customer_list= [customers[j] for j in range(len(customer_depot)) if customer_depot[j] == i ]
                demand = [c.q for c in depot.customer_list]

                if(sum(demand) > m*depot.Q):
                    print demand
                    print sum(demand)
                    feasible = False

            if feasible: #all depots within weightlimit, IF ONE CAN HAVE ONLY ONE ROUTE PER VEHICLE
               break
            else:
                print "New try!"


    def MVTS(self):
        routes = []
        for depot in self.depots:
            routes.append(optimized_travelling_salesman(depot.customer_list,depot))

        return routes



def distance(c_1, c_2):

    return ((c_1.x - c_2.x) ** 2 + (c_1.y - c_2.y) ** 2) ** 0.5

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
