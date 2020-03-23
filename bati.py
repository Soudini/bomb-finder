import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon, LineString
from import_data import get_stations_positions
import matplotlib.pyplot as plt
import networkx as nx
X_MAX = 100
Y_MAX = 100
RESOLUTION = 1



# LE BATI
buildings = []
####### Batiment 1
x0 = 10.08 ; y0 = 10.223
x1 = 30.08 ; y1 = 10.223
x2 = 30.08 ; y2 = 15.223
x3 = 17.08 ; y3 = 15.223
x4 = 17.08 ; y4 = 25.223
x5 = 10.08 ; y5 = 25.223

buildings.append([ (x0, y0), (x1, y1) , (x2, y2), (x3,y3), (x4, y4), (x5, y5) ])

####### Batiment 2
x0 = 50.08 ; y0 = 12.223
x1 = 65.08 ; y1 = 12.223
x2 = 65.08 ; y2 = 27.223
x3 = 50.08 ; y3 = 27.223

buildings.append([ (x0, y0), (x1, y1) , (x2, y2), (x3,y3) ])
####### Batiment 3
x0 = 80.08 ; y0 = 32.223
x1 = 87.08 ; y1 = 32.223
x2 = 87.08 ; y2 = 57.223
x3 = 80.08 ; y3 = 57.223

buildings.append([ (x0, y0), (x1, y1) , (x2, y2), (x3,y3) ])

####### Batiment 4
x0 = 12.08 ; y0 = 78.223
x1 = 42.08 ; y1 = 78.223
x2 = 42.08 ; y2 = 92.223
x3 = 12.08 ; y3 = 92.223

buildings.append([ (x0, y0), (x1, y1) , (x2, y2), (x3,y3) ])

####### Batiment 5
x0 = 75   ; y0 = 70
x1 = 85   ; y1 = 80
x2 = 90   ; y2 = 75
x3 = 96   ; y3 = 81
x4 = 0.5*167 ; y4 = 0.5*187
x5 = 0.5*135 ; y5 = 0.5*155

buildings.append([ (x0, y0), (x1, y1) , (x2, y2), (x3,y3), (x4, y4), (x5, y5) ])

####### Batiment 6
x0 = 20.08 ; y0 = 40.223
x1 = 40.08 ; y1 = 40.223
x2 = 40.08 ; y2 = 45.223
x3 = 25.08 ; y3 = 45.223
x4 = 25.08 ; y4 = 55.223
x5 = 35.08 ; y5 = 55.223
x6 = 35.08 ; y6 = 70.223
x7 = 20.08 ; y7 = 70.223


buildings.append([ (x0, y0), (x1, y1) , (x2, y2), (x3,y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7) ])

stations_positions = get_stations_positions()

polygon_buildings = [Polygon(building) for building in buildings[:]]
interesting_points = stations_positions + [point for building in buildings for point in building ]
interesting_points = [Point(point) for point in interesting_points]

def test_point_inside(i,j):
    point = Point((i,j))
    test = any([polygon.contains(point) for polygon in polygon_buildings])
    return int(test)

def apply_within_range_test_point_inside(args):
    index, size_pool = args
    slice_size = X_MAX*RESOLUTION//size_pool
    field = np.zeros((slice_size, Y_MAX*RESOLUTION))
    for (i,j), value in np.ndenumerate(field):
        test = test_point_inside(i/RESOLUTION + index * X_MAX / size_pool,j / RESOLUTION)
        field[i,j] = test 
    return field

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
                results[(i-index * X_MAX*RESOLUTION//size_pool,j,k)] = get_shortest_path_length(point, k)
    print(f"process {index} done !!")
    
    return results


base_A = get_adjacency_matrix(interesting_points)




# print(G.nodes)
nx.draw(get_graph(base_A, interesting_points), [point.coords[:][0] for point in interesting_points])
plt.show()
