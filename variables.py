X_MAX = 100
Y_MAX = 100
RESOLUTION = 1
N_STATION = 5

LINE_COUNT = X_MAX * RESOLUTION
ROW_COUNT = Y_MAX * RESOLUTION
SOURCE_PATH = './TE'

# ---- heuristique ----

threshold = 0.99
m_heur = 10

# ---- local search ----
pas_search = 0.2                      #pas de la recherche
pas_tnt = 0.1
pas_sim = 0.2                         #pas de la simu armen
max_iter_space = 50                   #nb max d'iterations
max_iter_tnt = 50

# ---- grid_search ----
pas_sim_gs = 0.2
pas_gs = 2
