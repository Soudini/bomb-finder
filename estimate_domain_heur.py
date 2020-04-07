import bati
from variables import *

def get_domain(corr_mat):

    x_min = X_MAX       # Le domaine explore sera compris entre x_min,x_max y_min et y_max.
    x_max = 0
    y_min = Y_MAX
    y_max = 0

    for x in range(len(corr_mat)):        #On selectionne le plus petit carre contennant toutes les correlations superieures au threshosld
        for y in range(len(corr_mat[0])):
            if bati.test_point_inside(x,y)==0 and corr_mat[x][y]>threshold:
                x_min = min(x/RESOLUTION,x_min)
                x_max = max(x/RESOLUTION,x_max)
                y_min = min(y/RESOLUTION,y_min)
                y_max = max(y/RESOLUTION,y_max)
    domain = (x_min,x_max,y_min,y_max)

    return domain