import multiprocessing as mp
from time import sleep
import numpy as np

import bati 
import cost_function as costf
import simulation_launcher as launch
from variables import *

neighborhood = [(pas_search,0),(-pas_search,0),(0,pas_search),(0,-pas_search)] # croix de distance 1 

def local_search(SOURCE_PATH,point,m, return_list):
    current_min = point
    current_mincost = np.inf
    print(f'starting local search for {point}')

    iteration = 0
    while iteration < max_iter_space and  (current_min[1]-point[1])**2 + (current_min[0]-point[0])**2 < pas_gs**2:
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

    print('Start looking for TNT min')

    iteration = 0                  #### recherche de la meilleur masse pour le meilleur point trouvé.
    m_opt = m
    while iteration < max_iter_tnt:
        batch = []                                        #Construction du batch de simulation pour l'étape        
        batch.append({'XC':current_min[0],'YC':current_min[1],'M_TNT':m_opt+pas_tnt,'PAS':pas_sim_tnt})
        batch.append({'XC':current_min[0],'YC':current_min[1],'M_TNT':m_opt-pas_tnt,'PAS':pas_sim_tnt})
        SIM_PATHS = launch.batch_launch_simulation(batch) #liste des paths résultats des simus

        next_c = []
        next_m = []
        for path in SIM_PATHS:  # recherche du meilleur de l'étape 
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
    current_min = (current_min[0],current_min[1],m_opt)

    print(f'finished local search for {point}')
    
    return_list.append(( current_min, current_mincost ))

def batch_local_search(SOURCE_PATH, points, m_heur):
    manager = mp.Manager()
    return_list = manager.list()
    processes = []
    for point in points:
        print(f'starting local search for {point}')
        p = mp.Process(target=local_search, args=(SOURCE_PATH, point, m_heur, return_list))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    return return_list

    

