import cost_function
import distance_correlation
import grid_search as gs
import multiprocess_local_search as ls
import numpy as np
import bati
import distance_correlation
import estimate_domain_heur as dom
import estimate_m as est_m
from variables import *


##### Restriction du domaine par heuristique

distance_field=np.load('distance_field.npy')
corr_mat = distance_correlation.correlation(distance_field,SOURCE_PATH)

domain = dom.get_domain(corr_mat)   #Estimation du domaine spatial par path finding
print(f'searching the domain : {domain}')

m_heur = est_m.get_m_heur(corr_mat) #Estimation de la masse 
print(f'Estimated TNT mass : {m_heur}')

##### grid-search

grid_p, grid_c = gs.grid_search(SOURCE_PATH,domain,m_heur,pas_gs) # renvoie une liste de point/cout

##### Definitions des points de départ de la recherche locale
nb_point = min(len(grid_p),3)
starting_points = []            # On selectionne les points prometteurs

for k in range (nb_point):
    i = np.argmin(np.array(grid_c))
    starting_points.append(grid_p.pop(i))
    grid_c.pop(i)

print(f'continuing with points {starting_points}')
##### Etape finale de recherche locale

ls_results = ls.batch_local_search(SOURCE_PATH, starting_points, m_heur)

with open('result_{}_{}_{}'.format(SOURCE_PATH.replace('/', ''), pas_sim_gs,pas_sim), 'a') as result:
    result.write('estimated source position : '+ str(min(ls_results, key = lambda x:x[1])) + '\n')
    result.write(str(ls_results) + '\n')
