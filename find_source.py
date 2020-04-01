import cost_function
import distance_correlation

SOURCE_PATH = './TE0'

##### Restriction du domaine par path_finding
domain = distance_correlation(SOURCE_PATH)

##### Potentielle grid-search
pas_gs = 0.5
grid = grid_search(SOURCE_PATH,,domain,m,pas) # renvoie une liste de point/coût

##### Définitions des points de départ de la recherche locale

starting_points = find_starting_points(grid)  # On selectionne les points prometteurs

##### Etape finale de recherche locale
cost = []
points = []

for point in starting_points:
    p,c = local_search(point)
    points.append(p)
    cost.append(c)

res = (point[argmin(cost)],min(cost))

print(res)