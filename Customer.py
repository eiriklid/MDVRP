

class Customer():
    def __init__(self,i, x, y, d, q):
        self.i = i
        self.x = x
        self.y = y
        self.d = d # necessary service duration required for this customer (0 = no such hard requirement)
        self.q = q # demand for this customer, load


