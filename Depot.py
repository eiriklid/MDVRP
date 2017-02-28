import random

class Depot:
    def __init__(self,x, y, D, Q, m):
        self.x = x
        self.y = y
        self.D = D  #maximum duration of a route
        self.Q = Q  #allowed maximum load of a vehicle (same for all the vehicles assigned to all depots)
        self.m = m  #maximum number of vehicles available in each depot
        self.customer_list = [] #dict for vehicle instead/as well?
        self.vehicle_dict = {}
        for i in range(self.m):
            self.vehicle_dict[i+1] = []


    def init_route(self):

        for customer in self.customer_list:
            vehicle = random.randint(1,self.m) #add customer to route
            if vehicle in self.vehicle_dict:
                self.vehicle_dict[vehicle].append(customer)
            else:
                print "Depot init failed"
                self.vehicle_dict[vehicle] = [customer]

    def get_insertion_costs(self,customer):
        insertion_costs = []

        for veh, route in self.vehicle_dict.items():
                insertion_costs= insertion_costs + self.insertion_cost(route,customer,veh)

        return insertion_costs

    def insertion_cost(self,route, customer,vehicle):
        costs = []
        feasible = True
        if route != []:
            if( (customer.q + self.route_load(route)) > self.Q):
                feasible = False

            costs = [0 for i in range(len(route)+1)]

            #cost to insert at the beginning
            costs[0] += distance(self,customer)
            costs[0] += distance(customer, route[0])
            costs[0] -= distance(self, route[0])

            #cost to insert in the middle
            for i in range(1,len(route)):
                costs[i] += distance(route[i-1], customer)
                costs[i] += distance(customer,route[i])
                costs[i] -= distance(route[i-1], route[i])

            #cost to insert at the end
            costs[len(route)] += distance(route[len(route)-1],customer)
            costs[len(route)] += distance(customer,self)
            costs[len(route)] -= distance(route[len(route)-1], self)

        if(self.D != 0):
            margin = self.D - self.route_length(route)
            for i, item in enumerate(costs):
                if (margin < costs[i]):
                    #print "To long route", margin, costs[i]
                    costs[i] = (item, i, vehicle, False)
                else:
                    costs[i] = (item, i, vehicle, feasible)
        else:
            for i, item in enumerate(costs):
                costs[i] = (item,i,vehicle,feasible)

        return costs

    def insert_in_route(self,customer,vehicle,i):
        self.vehicle_dict[vehicle].insert(i,customer)

    def make_new_route(self,customer):
        placed = False
        for vehicle, route in self.vehicle_dict.items():
            if route ==[]:
                self.insert_in_route(customer,vehicle,0)
                placed = True
                break

        if not placed:
            #print "Add new car"
            self.vehicle_dict[len(self.vehicle_dict)+1]= [customer]
            #print self.vehicle_dict.keys()

    def clean(self):
        empty_routes = 0
        for vehicle, route in self.vehicle_dict.items()
            if route == []:
                print "Vehicle",vehicle,"is empty"
                empty_routes+=1
                for i in range(vehicle,len(self.vehicle_dict)):
                    self.vehicle_dict[i] = self.vehicle_dict[i+1]

        for i in range(empty_routes):
            del self.vehicle_dict[len(self.vehicle_dict)]

    def route_load(self,route):
        load = 0
        for stop in route:
            load += stop.q

        return load

    def route_length(self,route):
        if route != []:
            dist = distance(self,route[0])
            for i in range(1, len(route)):
                dist += distance(route[i - 1], route[i])
                dist += route[i].d
            dist += distance(self,route[-1])
        else:
            return 0

        return dist


def distance(c_1, c_2):
    return ((c_1.x - c_2.x) ** 2 + (c_1.y - c_2.y) ** 2) ** 0.5



