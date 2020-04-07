import simulation_launcher as launch
import bati
import random
import numpy as np
import cost_function as costf
from variables import *

pas_neighb = 0.1        # Pas entre voisins
size_neighb_max = 2     # Taille max d'un voisinage
k_max = 100             # Nombre d'itérations
T_0 = 100               # Température initiale

def neighborhood(point, k):              # Définition du voisinage d'un point à l'itération k
    neighbours = []
    size_neighb = size_neighb_max * (1 - k/k_max) + pas_neighb      # Réduction de la taille du voisinage selon l'itération
    n = int(size_neighb/pas_neighb)
    x = point[0]
    y = point[1]
    for i in range(2*n+1):
        for j in range(2*n+1):
            neighbours.append((x-size_neighb+i*pas_neighb, y-size_neighb+j*pas_neighb))
    return neighbours


def simulated_annealing_search(SOURCE_PATH,point,m):

    current_best      = point
    batch             = []
    if bati.test_point_inside(point[0], point[1]) == 0:
        batch.append({'XC': point[0], 'YC': point[1], 'M_TNT': m, 'PAS': pas_neighb})
    SIM_PATHS = launch.batch_launch_simulation(batch)
    current_best_cost = costf.cost_function1(SOURCE_PATH, SIM_PATHS[0] + '/POST1D/TE')
    current_point     = point
    current_cost      = current_best_cost
    neighbours        = neighborhood(point, 0)
    T                 = T_0
    k                 = 0
    print(f'starting simulated annealing for {point}')

    while k<k_max:

        batch = []
        new_point = random.choice(neighbours)
        while bati.test_point_inside(new_point[0], new_point[1]) != 0:
            new_point = random.choice(neighbours)
        batch.append({'XC': new_point[0], 'YC': new_point[1], 'M_TNT': m, 'PAS': pas_neighb})
        SIM_PATHS = launch.batch_launch_simulation(batch)
        new_cost = costf.cost_function1(SOURCE_PATH, SIM_PATHS[0] + '/POST1D/TE')

        if new_cost < current_cost or random.random() < np.exp(-(new_cost-current_cost)/T):
            current_point = new_point
            current_cost = new_cost
            neighbours = neighborhood(current_point, k)
            if current_cost < current_best_cost:
                current_best = current_point
                current_best_cost = current_cost
        T = T_0*(1-k/k_max)
        k = k+1

    return current_best, current_best_cost


