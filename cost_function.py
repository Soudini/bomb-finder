import import_data as importd
import matplotlib.pyplot as plt
import math 

###Preconditionnement function for clean data
def preconditionnement(stations1, stations2):

    key_list = [key for key in stations1.keys()]
    station_1 = stations1[key_list[0]]
    station_2 = stations2[key_list[0]]

    initial_time_1 = [station.initial_time for station in stations1.values()]
    initial_time_2 = [station.initial_time for station in stations2.values()]
    init_t = min(initial_time_1)                                            
    delta_t = init_t - min(initial_time_2)                                     # On décale la simu2 de delta_t pour faire correspondre les instants initiaux
    max_t = min(init_t + 0.1, station_1.time[-1], station_2.time[-1]+delta_t)
    fact = 100/(max_t - init_t)
    
    kept_values1 = dict((key_station,[]) for key_station in stations1)
    kept_values2 = dict((key_station,[]) for key_station in stations2)
    times = []

    j = 0        #indice pour parcourir la liste des temps 2 qui est différente de la liste des temps 1

    for i in range(len(station_1.time)):   
        if station_1.time[i]>=init_t and station_1.time[i]<=max_t:
            times.append(station_1.time[i])

            for key_station in stations1.keys():                                    # enregistrement valeurs 1
                kept_values1[key_station].append(stations1[key_station].value[i])
            
            while (station_2.time[j]+delta_t) < station_1.time[i] :   #recherche de l'indice équivalent dans l'autre simulation
                j+=1
            for key_station in stations2.keys():                                    # enregistrement valeurs 2 par approximation affine
                try :
                    value = (station_1.time[i] - (station_2.time[j-1]+delta_t))/(station_2.time[j] - station_2.time[j-1])*(stations2[key_station].value[j] - stations2[key_station].value[j-1])
                    value += stations2[key_station].value[j-1]
                    kept_values2[key_station].append(value)
                except : 
                    kept_values2[key_station].append(stations2[key_station].value[j-1])
            
    return kept_values1, kept_values2, times, fact


#####################################################################################################
# Cost functions:
# 0: using initial detection
# 1: using L1 distance
# 2: using L2 distance
#####################################################################################################

alpha = 20      #hyperparamètre à tuner
beta = 10**-5

def cost_function0(DATA_FOLDER1,DATA_FOLDER2):

    stations1 = importd.import_data(DATA_FOLDER1)
    stations2 = importd.import_data(DATA_FOLDER2)
    cost = 0

    if stations1.keys() == stations2.keys():
        for keys in stations1.keys():
            cost += abs(stations1[keys].initial_time - stations2[keys].initial_time)*alpha + abs(stations1[keys].first_peak_value - stations2[keys].first_peak_value)*beta

        return cost
    print("incompatible data")

def cost_function1(DATA_FOLDER1,DATA_FOLDER2):

    stations1 = importd.import_data(DATA_FOLDER1)
    stations2 = importd.import_data(DATA_FOLDER2)
    values1, values2, times, fact = preconditionnement(stations1, stations2)
    cost = 0

    if stations1.keys() == stations2.keys():
        for key in values1.keys():
            for j in range (len(times)-1):
                cost += abs(values1[key][j]-values2[key][j])*(times[j+1]-times[j])  #carrés à droite

        return cost*fact*10**-4
    print("incompatible data")

def cost_function2(DATA_FOLDER1,DATA_FOLDER2):

    stations1 = importd.import_data(DATA_FOLDER1)
    stations2 = importd.import_data(DATA_FOLDER2)

    values1, values2, times, fact = preconditionnement(stations1, stations2)
    cost = 0

    if stations1.keys() == stations2.keys():
        for key in values1.keys():
            for j in range (len(times)-1):
                cost += ((values1[key][j]-values2[key][j])**2)*(times[j+1]-times[j])*10**-8  #carrés à droite

        return math.sqrt(cost)*fact
    print("incompatible data")
