
class Depot:
    def __init__(self,x, y, D, Q):
        self.x = x
        self.y = y
        self.D = D  #maximum duration of a route
        self.Q = Q  #allowed maximum load of a vehicle (same for all the vehicles assigned to all depots)