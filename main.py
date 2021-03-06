import matlab.engine

import Customer
import Depot
import Population
import Solution
import matlab_scripts as mat
import copy


f = open('Data\Data Files\p01','r')
data= f.readline().split()
m = int(data[0])
n = int(data[1])
t = int(data[2])

depots = []
# get max duration(D) and max load per vehicle(Q) for each depot
for i in range(t):
    DQ = f.readline().split()
    depots.append( (float(DQ[0]), float(DQ[1])) )


customers = []
#get customer number(i), position(x,y), duration(d) and demand(q)
for j in range(n):
    info = f.readline().split()
    i = int(info[0])
    x = float(info[1])
    y = float(info[2])
    d = float(info[3])
    q = float(info[4])
    customers.append( Customer.Customer(i,x,y,d,q) )

#get depot position(x,y), max duration(D), max load per vehicle(Q)
for i in range(t):
    info = f.readline().split()
    x = float(info[1])
    y = float(info[2])
    D = depots[i][0]
    Q = depots[i][1]
    depots[i]= Depot.Depot(x,y,D,Q,m)

'''
sol1 = Solution.Solution(customers,depots,m,t)
sol2 = copy.deepcopy(sol1)
sol2.remove_customers(sol1.customers)

for depot in sol1.depots:
    for veh, route in depot.vehicle_dict.items():
        print veh, route
'''

pop = Population.Population(customers,depots,m,t,40)

for gen in range(25):
    if(gen%5==0):
        print gen
    pop.selection()

best_sol =pop.best_solution

best_sol.make_file('test1.txt')



eng = matlab.engine.start_matlab()
fig = mat.make_fig(eng)

mat.plot_depot(eng,depots)
mat.plot_customers(eng,customers)

dur,_ = best_sol.duration_and_vehicles()

mat.title_fitness(eng,dur)
best_sol.plot_sol(eng)


eng.saveas(fig,'plot.fig',nargout=0)
