import cost_function
import simulation_launcher as launch
import bati

def grid_search(SOURCE_PATH,domain,m,pas):

    pas_sim_gs = 0.5

    L,l = domain[1]-domain[0], domain[3]-domain[2]
    nx = L/pas
    ny = l/pas

    grid_p = []
    grid_c = []
    sims = []

    for i in range (nx):
        for j in range (ny):
            if bati.test_point_inside(domain[0]+i*pas, domain[2]+j*pas)==0:
                sims.append({'XC':domain[0]+i*pas,'YC':domain[2]+j*pas,'M_TNT':m,'PAS':pas_sim_gs})
    SIM_PATHS = launch.batch_launch_simulation(sims)

    for k in range (len(SIM_PATHS)):
        c = cost_function.cost_function1(SOURCE_PATH, SIM_PATHS[k]+'/POST1D/TE')
        p = (float(SIM_PATHS[k].split('_')[5]),float(SIM_PATHS[k].split('_')[6]))
        grid_p.append(p)
        grid_c.append(c)

    return grid_p,grid_c
