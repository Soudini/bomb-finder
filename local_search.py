import bati 
import cost_function as costf
import simulation_launcher
import numpy as np 
import simulation_launcher as launch

pas_search = 0.2                        #pas de la recherche spatiale
pas_tnt = 0.1                           #pas de la recherche en tnt
pas_sim = 0.2                           #pas de la simu armen
max_iter_space = 50                     #nb max d'iterations
max_iter_tnt = 50                           
neighborhood = [(pas_search,0),(-pas_search,0),(0,pas_search),(0,-pas_search)] # croix de distance 1 

def local_search(SOURCE_PATH,point,m):
    current_min = point
    current_mincost = np.inf

    iteration = 0
    while iteration < max_iter_space:
        batch = []   #Construction du batch de simulation pour l'étape
        for ng in neighborhood:
            next_point = (current_min[0]+ng[0],current_min[1]+ng[1])
            if bati.test_point_inside(next_point[0],next_point[1])==0:
                batch.append({'XC':next_point[0],'YC':next_point[1],'M_TNT':m,'PAS':pas_sim})
        SIM_PATHS = launch.batch_launch_simulation(batch) #liste des paths résultats des simus

        next_c = []
        next_p = []
        for path in SIM_PATHS:  #recherche du meilleur point
            c = costf.cost_function1(SOURCE_PATH,path+'/POST1D/TE')
            p = (float(path.split('_')[5]),float(path.split('_')[6]))
            next_c.append(c)
            next_p.append(p)
        index = np.argmin(np.array(next_c))

        if current_mincost <= next_c[index]: #On vérifie si on a pas atteint un min local
            print('------------LOCAL MIN FOUND---------------')
            break

        current_min = next_p[index]
        current_mincost = next_c[index]

        iteration+=1
    
    iteration = 0                  #### recherche de la meilleur masse
    m_opt = m
    while iteration < max_iter_tnt:
        batch = []                  #Construction du batch de simulation pour l'étape        
        batch.append({'XC':current_min[0],'YC':current_min[1],'M_TNT':m_opt+pas_tnt,'PAS':pas_sim})
        batch.append({'XC':current_min[0],'YC':current_min[1],'M_TNT':m_opt-pas_tnt,'PAS':pas_sim})
        SIM_PATHS = launch.batch_launch_simulation(batch) #liste des paths résultats des simus

        next_c = []
        next_m = []
        for path in SIM_PATHS:  #recherche du meilleur point
            c = costf.cost_function1(SOURCE_PATH,path+'/POST1D/TE')
            mn = float(path.split('_')[7].split('k')[0])
            next_c.append(c)
            next_m.append(mn)
        index = np.argmin(np.array(next_c))

        if current_mincost <= next_c[index]: #On vérifie si on a pas atteint un min local
            print('------------LOCAL BEST TNT FOUND---------------')
            break

        m_opt = next_m[index]
        current_mincost = next_c[index]

        iteration+=1

    return current_min, m_opt, current_mincost






