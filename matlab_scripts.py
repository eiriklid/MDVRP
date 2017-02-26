import matlab.engine

COLORS = ['b','r','g','c','m','y','k']


def make_fig(eng,fitness):
    fig = eng.figure()
    eng.hold("on", nargout=0)
    eng.box("on", nargout=0)
    eng.grid("on", nargout=0)
    eng.title('Fitness: ' + str(fitness), nargout=0)
    return fig

def plot_depot(eng,depots):
    for depot in depots:
        eng.scatter(depot.x, depot.y, 'filled', 'k', 'd', nargout=0)

def plot_customers(eng, customers):
    for customer in customers:
        eng.scatter(customer.x, customer.y, 'k',nargout=0)  # need to set color at some point

def draw_line(eng,x0,y0, x1,y1, color):
    x= matlab.double([x0,x1])
    y= matlab.double([y0,y1])
    eng.plot(x,y,color,nargout=0)

def plot_routes(eng,depot):
    for vehicle,route in depot.vehicle_dict.items():
        if route == []:
            print "Empty Route for veh:",vehicle
        draw_line(eng,depot.x,depot.y,route[0].x,route[0].y,COLORS[vehicle-1])
        route_len = len(route)
        if(route_len >1):
            for i in range(route_len-1):
                draw_line(eng,route[i].x,route[i].y, route[i+1].x,route[i+1].y, COLORS[vehicle-1])
        draw_line(eng,route[route_len-1].x,route[route_len-1].y,depot.x,depot.y,COLORS[vehicle-1])

