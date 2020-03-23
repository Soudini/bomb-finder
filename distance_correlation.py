import numpy as np

from import_data import import_data

def correlation(distance_field):
    stations = import_data()
    initial_detection_times = np.array([stations[s].initial_time for s in stations])
    
    normalized_initial_detection_times = initial_detection_times / np.linalg.norm(initial_detection_times)
    normalized_distance_field = distance_field / np.linalg.norm(distance_field, axis = 2, keepdims=True)

    return np.tensordot(normalized_distance_field, normalized_initial_detection_times, axis = [2,0])