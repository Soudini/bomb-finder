import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon, LineString
import matplotlib.pyplot as plt
import networkx as nx

from bati import interesting_points, polygon_buildings, Y_MAX, X_MAX, RESOLUTION

#-------------------------------------------------UTILS-------------------------------------------------
def get_visible_points(point1, polygons):
    for point2 in interesting_points:
        return is_visible(point1, point2, polygons)
                
def is_visible(point1, point2, polygons = polygon_buildings):
    return int(not(any([LineString((point1, point2)).crosses(polygon) or polygon.contains(LineString((point1, point2))) for polygon in polygons])))*LineString((point1, point2)).length

def get_adjacency_matrix(points):
    adjacency_matrix = np.zeros((len(points), len(points)))
    for (i,j), value in np.ndenumerate(adjacency_matrix):
        if i > j:
            buff = is_visible(points[i], points[j], polygon_buildings)
            adjacency_matrix[i,j] = buff
            adjacency_matrix[j,i] = buff
    return adjacency_matrix

def get_graph(A, points):
    G = nx.from_numpy_matrix(A)
    for i in range(len(G.nodes)):
        G.nodes[i]['pos'] = points[i].coords[:][0]

    return G

def add_point_to_adjacency_matrix(A, interesting_points, point):
    i,j = A.shape
    new_A = np.zeros((i +1, j +1))
    new_A[:i, :j] = A
    for index, interesting_point in enumerate(interesting_points):
        buff = is_visible(point, interesting_point)
        new_A[-1, index] = buff
        new_A[index, -1] = buff
    
    return new_A, interesting_points + [point]

def get_shortest_path_length(point, station):
    new_A, new_interesting_points = add_point_to_adjacency_matrix(base_A, interesting_points, point)
    G = get_graph(new_A, new_interesting_points)
    try :
        return nx.dijkstra_path_length(G, station, len(new_interesting_points) - 1)
    except Exception:
        return None

def apply_within_range_get_shortest_path_length(args):
    index, size_pool = args
    results = {}
    for i in range(index * X_MAX*RESOLUTION//size_pool, (index + 1) * X_MAX*RESOLUTION//size_pool):
        print(f"process {index}, doing row {i}")
        for j in range(Y_MAX * RESOLUTION):
            point = Point((i / RESOLUTION, j / RESOLUTION))
            for k in range(5):
                results[(i,j,k)] = get_shortest_path_length(point, k)
    print(f"process {index} done !!")
    
    return results


base_A = get_adjacency_matrix(interesting_points)

# print(G.nodes)
# nx.draw(get_graph(base_A, interesting_points), [point.coords[:][0] for point in interesting_points])
# plt.show()

def get_estimated_source_position():

    try:
        distance_field = np.load('distance_field.npy')
    except Exception as e:
        from multiprocess_runner import generate_distance_field
        print(e)
        print('distance field not found, generating it')
        distance_field = generate_distance_field()



    from distance_correlation import correlation

    correlation_matrix = correlation(distance_field)
    return np.unravel_index(np.nanargmax(correlation_matrix), shape=correlation_matrix.shape)