import matlab.engine


def make_fig(eng):
    fig = eng.figure()
    eng.hold("on", nargout=0)
    eng.box("on", nargout=0)
    eng.grid("on", nargout=0)
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