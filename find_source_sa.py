import numpy as np
import bati
import distance_correlation
import simulated_annealing_search.py as sas
from variables import *


##### Restriction du domaine par path_finding
distance_field=np.load('distance_field.npy')
corr_mat = distance_correlation.correlation(distance_field,SOURCE_PATH)

##### Recherche du meilleur point trouvé par le path_finding
x_max = 0
y_max = 0
c = corr_mat[0][0]
for x in range(len(corr_mat)):
    for y in range(len(corr_mat[0])):
        if bati.test_point_inside(x,y)==0 and corr_mat[x][y] > c:
            x_max = x
            y_max = y
            c = corr_mat[x][y]

##### Lancement du recuit simulé
starting_point = (x_max, y_max)
print(f'Launching Simulated Annealing search with {starting_point}')
sas_results = sas.simulated_annealing_search(SOURCE_PATH, starting_point, m_heur)

##### Ecriture des résultats dans un fichier texte
with open('result_sas_{}_{}'.format(SOURCE_PATH.replace('/', ''),pas_sim), 'a') as result:
    result.write('estimated source position : '+ str(sas_results) + '\n')
