import matlab.engine
eng = matlab.engine.start_matlab("-desktop")

import Customer
import Depot
import Solution
import matlab_scripts as mat



f = open('Data\Data Files\p01','r')
data= f.readline().split()
m = int(data[0])
n = int(data[1])
t = int(data[2])

depots = []
# get max duration(D) and max load per vehicle(Q) for each depot
for i in range(t):
    DQ = f.readline().split()
    depots.append( (int(DQ[0]), int(DQ[1])) )


customers = []
#get customer number(i), position(x,y), duration(d) and demand(q)
for j in range(n):
    info = f.readline().split()
    i = int(info[0])
    x = int(info[1])
    y = int(info[2])
    d = int(info[3])
    q = int(info[4])
    customers.append( Customer.Customer(i,x,y,d,q) )

#get depot position(x,y), max duration(D), max load per vehicle(Q)
for i in range(t):
    info = f.readline().split()
    x = int(info[1])
    y = int(info[2])
    D = depots[i][0]
    Q = depots[i][1]
    depots[i]= Depot.Depot(x,y,D,Q,m)

sol_1 = Solution.Solution(customers, depots, m)



fig = mat.make_fig(eng)

mat.plot_depot(eng,depots)
mat.plot_customers(eng,customers)

sol_1.plot_sol(eng)

eng.saveas(fig,'plot.fig',nargout=0)


