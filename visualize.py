
from import_data import import_data, SOURCE_POSITION
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from bati import polygon_buildings

def show_pressure_records():
    for station in stations:
        plt.plot(stations[station].time, stations[station].value, label=stations[station].name)

    plt.legend()


def show_stations_placements():
    ax = plt.gca()
    ax.scatter(*SOURCE_POSITION, label = 'source')
    circles = []
    for station in stations:
            point = ax.scatter(stations[station].x, stations[station].y, label=stations[station].name)
    for polygon in polygon_buildings:
        plt.plot(*polygon.exterior.xy)
    

def show_animation(save = 0):
    fig = plt.figure()
    ax = plt.gca()
    ax.scatter(*SOURCE_POSITION, label = 'source')
    circles = []
    for station in stations:
            print(station)
            circle = plt.Circle((stations[station].x, stations[station].y), radius = stations[station].initial_time * 340, fill = False)
            ax.add_patch(circle)
            point = ax.scatter(stations[station].x, stations[station].y, label=stations[station].name)
            circles.append(circle)

    def animate(delta):
        print(delta)
        for index, circle in enumerate(circles):
            circle.set_radius(stations['ST'+str(index)].initial_time * 340 + delta-10)
        return circles

    plt.legend()
    ani = animation.FuncAnimation(fig, animate, frames=60, blit=True, interval=200, repeat=False)
    if save:
        ani.save('prop_from_source.mp4')
