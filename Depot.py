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

    def init_route(self):

        for customer in self.customer_list:
            vehicle = random.randint(1,self.m) #add customer to route
            if vehicle in self.vehicle_dict:
                self.vehicle_dict[vehicle].append(customer)
            else:
                self.vehicle_dict[vehicle] = [customer]





