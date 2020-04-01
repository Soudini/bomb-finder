import cost_function
import simulation_launcher as launch
def grid_search(SOURCE_PATH,domain,m,pas):
    L,l = domain.dimension()
    nx = L/pas
    ny = l/pas

    grid = []

    for i in range (nx):
        for j in range (ny):
            p,c = cost_function.costfunction1(SOURCE_PATH,launch.launch_simulation(domain.X+nx*pas,domain.Y+ny*pas,m,1))
            grid.append((p,c))
    return grid
