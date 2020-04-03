import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon, LineString
from import_data import get_stations_positions
import matplotlib.pyplot as plt
import networkx as nx
from variables import *



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
