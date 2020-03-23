import os
import re


DATA_FOLDER = './TE'
SOURCE_POSITION = (40,65)
class Station():
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.time = []
        self.value = []
        self.__initial_time = None

    @property
    def initial_time(self):
        if not(self.__initial_time):
            threshold = self.value[0]
            for index, value in enumerate(self.value):
                if value > threshold:
                    self.__initial_time = self.time[index]
                    break
        return self.__initial_time

def import_data():
    stations = {}
    files = os.listdir(DATA_FOLDER)
    files.sort()
    for filename in files:
        with open(DATA_FOLDER + '/' + filename) as file:
            print(f'importing {filename}')
            match = re.findall('ST[0-9]+', filename)
            if match:
                name = match[0]
                for line in file.readlines()[1:]:
                    stations[name].time.append(float(line.split(' ')[0]))
                    stations[name].value.append(float(line.split(' ')[1]))

            else :
                for station_name, x, y in re.findall('(ST[0-9]+)(.+) (.+)', file.read()):
                    stations[station_name] = Station(station_name,float(x),float(y))

    print('import finished')
    return stations

def get_stations_positions():
    ret = []
    with open(DATA_FOLDER + '/STATION_NOM') as file:
        for station_name, x, y in re.findall('(ST[0-9]+)(.+) (.+)', file.read()):
             ret.append((float(x),float(y)))
    return ret