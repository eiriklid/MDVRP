import matlab.engine
eng = matlab.engine.start_matlab("-desktop")

import Customer
import Depot
import matlab_scripts as mat



f = open('Data\Data Files\p08','r')
data= f.readline().split()
m = int(data[0])
n = int(data[1])
t = int(data[2])

depots = []
for i in range(t):
    DQ = f.readline().split()
    depots.append( (int(DQ[0]), int(DQ[1])) )


customers = []
for j in range(n):
    info = f.readline().split()
    i = int(info[0])
    x = int(info[1])
    y = int(info[2])
    d = int(info[3])
    q = int(info[4])
    customers.append( Customer.Customer(i,x,y,d,q) )

for i in range(t):
    info = f.readline().split()
    x = int(info[1])
    y = int(info[2])
    D = depots[i][0]
    Q = depots[i][1]
    depots[i]= Depot.Depot(x,y,D,Q)



fig = mat.make_fig(eng)

mat.plot_depot(eng,depots)
mat.plot_customers(eng,customers)
mat.draw_line(eng,customers[0].x,customers[0].y, customers[1].x,customers[1].y, 'b')
eng.saveas(fig,'plot.fig',nargout=0)


