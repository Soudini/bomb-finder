import os
import re

DATA_FOLDER = "./TE0"
SOURCE_POSITION = (40,65)

class Station():
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.time = []
        self.value = []
        self.__initial_time = None
        self.__initial_time_index = None
        self.__first_peak_value = None
    @property
    def initial_time(self):
        if not(self.__initial_time):
            threshold = self.value[0]
            for index, value in enumerate(self.value):
                if value > threshold+10:
                    self.__initial_time = self.time[index]
                    self.__initial_time_index = index
                    break
        return self.__initial_time
    @property
    def initial_time_index(self):
        if not(self.__initial_time_index):
            threshold = self.value[0]
            for index, value in enumerate(self.value):
                if value > threshold+10:
                    self.__initial_time_index = index
                    break
        return self.__initial_time_index
    @property
    def first_peak_value(self):
        if not(self.__first_peak_value):
            threshold = self.value[0]
            for index, value in enumerate(self.value):
                if value>=threshold+10 and value < self.value[index-1]:
                    self.__first_peak_value = self.value[index-1]
                    break
        return self.__first_peak_value

def import_data(DATA_FOLDER='./TE'):
    stations = {}
    files = os.listdir(DATA_FOLDER)
    files.sort()
    for filename in files:
        with open(DATA_FOLDER + '/' + filename) as file:
            match = re.findall('ST[0-9]+', filename)
            if match:
                name = match[0]
                for line in file.readlines()[1:]:
                    stations[name].time.append(float(line.split(' ')[0]))
                    stations[name].value.append(float(line.split(' ')[1]))

            else :
                for station_name, x, y in re.findall('(ST[0-9]+)(.+) (.+)', file.read()):
                    stations[station_name] = Station(station_name,float(x),float(y))
                    
    return stations

def get_stations_positions():
    ret = []
    with open(DATA_FOLDER + '/STATION_NOM') as file:
        for station_name, x, y in re.findall('(ST[0-9]+)(.+) (.+)', file.read()):
             ret.append((float(x),float(y)))
    return ret