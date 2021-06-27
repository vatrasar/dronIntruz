import math

from GameObjects import Point
from GameState import GameState
from Settings import Settings
from events import Event_list
import matplotlib.pyplot as plt
import numpy as np

from tools.geometric_tools import get_2d_distance


def plan_visualize(events_list:Event_list,game_state:GameState,settings:Settings):


    map_range=settings.tier1_distance_from_intruder+settings.tier1_distance_from_intruder*0.2


    uav_size=0.5
    resolution=0.1
    number_of_points=round(uav_size/resolution)+1

    elements_to_draw=[]
    uav_x=[]
    uav_y=[]
    #draw UAVs
    for uav in game_state.uav_list:
        uav_x.append(uav.position.x)
        uav_y.append(uav.position.y)

        darw_object(game_state, number_of_points, resolution, uav, uav_size, uav_x, uav_y)





    #draw intuder

    fig, axs = plt.subplots()
    elements_to_draw.append((uav_x,uav_y))
    for pari_to_draw in elements_to_draw:
        x=pari_to_draw[0]
        y=pari_to_draw[1]
        axs.scatter(x, y,marker="s", color='r',s=4,)

    axs.set_box_aspect(1)
    plt.axis([-map_range, map_range, -map_range, map_range])
    plt.show()


def darw_object(game_state, number_of_points, resolution, object, object_size, object_x, object_y,):
    for i in range(0, number_of_points):
        for p in range(0, number_of_points):

            point = Point(i * resolution + object.position.x, p * resolution + object.position.y)
            if (get_2d_distance(point, object.position) <= object_size):
                object_x.append(i * resolution + object.position.x)
                object_y.append(p * resolution + object.position.y)

            point = Point(object.position.x - i * resolution, object.position.y - p * resolution)
            if (get_2d_distance(point, object.position) <= object_size):
                object_x.append(object.position.x - i * resolution)
                object_y.append(object.position.y - p * resolution)

            point = Point(i * resolution + object.position.x, object.position.y - p * resolution)
            if (get_2d_distance(point, object.position) <= object_size):
                object_x.append(i * resolution + object.position.x)
                object_y.append(object.position.y - p * resolution)

            point = Point(object.position.x - i * resolution, p * resolution + object.position.y)
            if (get_2d_distance(point, object.position) <= object_size):
                object_x.append(object.position.x - i * resolution)
                object_y.append(p * resolution + object.position.y)

