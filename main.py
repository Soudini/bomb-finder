import multiprocessing as mp
import numpy as np
from bati import apply_within_range_test_point_inside, apply_within_range_get_shortest_path_length
import matplotlib.pyplot as plt

def generate_field_matrix():

    pool = mp.Pool(mp.cpu_count())

    slices = pool.map(apply_within_range_test_point_inside, [(i, mp.cpu_count()) for i in range(mp.cpu_count())])
    mat = np.concatenate(slices, axis = 0)

    pool.close()    

    np.save('field', mat)

def generate_distance_field():
    pool = mp.Pool(mp.cpu_count())

    slices = pool.map(apply_within_range_get_shortest_path_length, [(i, mp.cpu_count()) for i in range(mp.cpu_count())])
    
    result = []
    for s in slices:
        result += s

    pool.close()    

# generate_distance_field()
# plt.matshow(np.load('field.npy'))
# plt.show()