import cost_function
import distance_correlation
import grid_search as gs
import multiprocess_local_search as ls
import multiprocess_local_search2 as ls2
import numpy as np
import bati
import distance_correlation
from variables import *


##### Restriction du domaine par path_finding
distance_field=np.load('distance_field.npy')
corr_mat = distance_correlation.correlation(distance_field,SOURCE_PATH)

x_min = 100       # Le domaine exploré sera compris entre x_min,x_max y_min et y_max.
x_max = 0
y_min = 100
y_max = 0

for x in range(len(corr_mat)):
    for y in range(len(corr_mat[0])):
        if bati.test_point_inside(x,y)==0 and corr_mat[x][y]>threshold:
            x_min = min(x,x_min)
            x_max = max(x,x_max)
            y_min = min(y,y_min)
            y_max = max(y,y_max)
domain = (x_min,x_max,y_min,y_max)
print(f'searching the domain : {domain}')

##### grid-search

grid_p, grid_c = gs.grid_search(SOURCE_PATH,domain,m_heur,pas_gs) # renvoie une liste de point/coût

##### Définitions des points de départ de la recherche locale
nb_point = min(len(grid_p),3)
starting_points = []  # On selectionne les points prometteurs
for k in range (nb_point):
    i = np.argmin(np.array(grid_c))
    starting_points.append(grid_p.pop(i))
    grid_c.pop(i)
print(f'continuing with points {starting_points}')
##### Etape finale de recherche locale


# Le pas pour créer le voisinage est un argument d'entrée
#Premiere recherche locale pas=0.2m
#Deuxième recherche à partir du meilleur point avec pas 0.1m

ls_results1 = ls2.batch_local_search(SOURCE_PATH, starting_points, m_heur,0.2)
opt_point=min(ls_results1,key=lambda x:x[1])
ls_results2= ls2.batch_local_search(SOURCE_PATH,[[opt_point[0][0],opt_point[0][1]]],opt_point[0][2],0.1)

with open('result_{}_{}_{}'.format(SOURCE_PATH.replace('/', ''), pas_sim_gs,pas_sim), 'a') as result:
    #result.write('best position after 2nd local search : '+ str(min(ls_results2, key = lambda x:x[1])) + '\n')
    result.write('estimated source position after 2nd search' + str(ls_results2) + '\n')
    result.write('estimated source position : '+ str(min(ls_results1, key = lambda x:x[1])) + '\n')
    result.write(str(ls_results1) + '\n')
