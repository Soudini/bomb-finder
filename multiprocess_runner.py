import multiprocessing as mp
import numpy as np
from bati import apply_within_range_test_point_inside
from path_finding import apply_within_range_get_shortest_path_length
import matplotlib.pyplot as plt
from variables import *


def generate_field_matrix():

    pool = mp.Pool(mp.cpu_count())

    slices = pool.map(apply_within_range_test_point_inside, [(i, mp.cpu_count()) for i in range(mp.cpu_count())])

    pool.close()    

    mat = np.concatenate(slices, axis = 0)
    np.save('field', mat)

def generate_distance_field():
    pool = mp.Pool(mp.cpu_count())
    slices = pool.map(apply_within_range_get_shortest_path_length, [(i, mp.cpu_count()) for i in range(mp.cpu_count())])
    pool.close()    
    results = np.zeros((LINE_COUNT, ROW_COUNT, N_STATION))

    for s in slices:
        for coords in s:
            results[coords] = s[coords]
    np.save('distance_field', results)

    return results
