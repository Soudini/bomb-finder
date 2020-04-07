import numpy as np
import simulation_launcher as launch
import cost_function 
import copy
from variables import *

def get_m_heur(corr_mat):
    
    mat = copy.deepcopy(corr_mat)
    for k in range (len(mat)):
        for l in range(len(mat[0])):
            if np.isnan(mat[k][l]):
                mat[k][l] = -np.inf                      #On remplace les NaN (interieurs de batiment) afin de pouvoir rechercher le max

    x,y = np.unravel_index(np.argmin(-mat), mat.shape)   #On recupere l'index de la meilleure correlation
    x = x/RESOLUTION
    y = y/RESOLUTION
    
    grid_m = []
    grid_c = []
    sims = []

    
    for k in range (TNT_MIN,TNT_MAX):      #Creation du batch de simus
        sims.append({'XC':x,'YC':y,'M_TNT':k,'PAS':0.2})

    SIM_PATHS = launch.batch_launch_simulation(sims)        #lancement simus
    for path in SIM_PATHS:                                  #traitements des resultats
        c = cost_function.cost_function1(SOURCE_PATH, path+'/POST1D/TE')
        m = float(path.split('_')[7].split('k')[0])
        grid_m.append(m)
        grid_c.append(c)
    m_heur = grid_m[np.argmin(np.array(grid_c))]

    return m_heur



