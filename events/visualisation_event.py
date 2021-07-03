import math
from random import Random

from Enums import UavStatus, HandStatus
from GameState import GameState
from events import Event, Event_list

from GameObjects import Point
from GameState import GameState
from Settings import Settings
from events import Event_list
import matplotlib.pyplot as plt
import numpy as np
import time
from tools.geometric_tools import get_2d_distance, get_2d_vector_from_polar


class Visualization_event(Event):
    def handle_event(self,event_list:Event_list,game_state:GameState,settings,rand:Random):
        event_list.delete_event(self)
        map_range = settings.tier1_distance_from_intruder + settings.tier1_distance_from_intruder * 0.2

        uav_size = settings.uav_size
        intruder_size = settings.intuder_size
        resolution = 0.1


        elements_to_draw = []
        uav_x = []
        uav_y = []
        # draw UAVs
        for uav in game_state.uav_list:
            if(uav.status!=UavStatus.TIER_2):
                uav_x.append(uav.position.x)
                uav_y.append(uav.position.y)
                self.darw_object(  resolution, uav, uav_size, uav_x, uav_y)
        elements_to_draw.append((uav_x, uav_y, "r"))


        # draw intuder
        intruder_x,intruder_y=[],[]
        intruder_x.append(game_state.intruder.position.x)
        intruder_y.append(game_state.intruder.position.y)
        self.darw_object(  resolution, game_state.intruder,intruder_size , intruder_x,intruder_y)
        elements_to_draw.append((intruder_x, intruder_y, "g"))


        #draw hands
        hands_x,hands_y=[],[]
        for hand in game_state.hands_list:
            if hand.status!=HandStatus.TIER_0:
                hands_x.append(hand.position.x)
                hands_y.append(hand.position.y)
                self.darw_object(resolution, hand,settings.hand_size , hands_x,hands_y)
        elements_to_draw.append((hands_x, hands_y, "b"))



        #draw hands ranges
        for hand in game_state.hands_list:
            tier_0_positon=hand.get_hand_tier0_position(settings)
            step=1
            point_x,point_y=[],[]
            for i in range(0,360):
                angle=math.radians(i*step)
                pose_point=get_2d_vector_from_polar(angle, settings.r_of_LR)
                pose_point[0]=pose_point[0]+tier_0_positon.x
                pose_point[1]=pose_point[1]+tier_0_positon.y

                point_x.append(pose_point[0])
                point_y.append(pose_point[1])
            elements_to_draw.append((point_x, point_y, "m"))


        #draw tier1 range

        tier_1_positon=game_state.intruder.position
        step=1
        point_x,point_y=[],[]
        for i in range(0,360):
            angle=math.radians(i*step)
            pose_point=get_2d_vector_from_polar(angle, settings.tier1_distance_from_intruder)
            pose_point[0]=pose_point[0]
            pose_point[1]=pose_point[1]

            point_x.append(pose_point[0])
            point_y.append(pose_point[1])
        elements_to_draw.append((point_x, point_y, "y"))



        if (game_state.visualize_first):
            # game_state.fig, game_state.axs = plt.subplots()
            # game_state.axs.set_box_aspect(1)
            plt.ion()
            game_state.visualize_first = False
            # plt.draw()
        # game_state.axs.set_box_aspect(1)


        for to_draw in elements_to_draw:
            x = to_draw[0]
            y = to_draw[1]
            plt.scatter(x, y, marker="s", color=to_draw[2], s=4, )



        plt.title("czas: %.2f s"%(game_state.t_curr))
        plt.axis([-map_range*1.3, map_range*1.3, -map_range, map_range])



        #plt.pause(0.3)
        plt.draw()
        plt.pause(0.3)
        plan_visualize(event_list,settings,game_state)
        # time.sleep(0.3)
        plt.clf()


    def darw_object(self,resolution, object, object_size, object_x, object_y):

        number_of_points = round(object_size/ resolution) + 1
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




def plan_visualize(event_list:Event_list,setting:Settings,game_state:GameState):
    new_event=Visualization_event(game_state.t_curr+setting.visualzation_update_interval,Point(0,0),game_state.intruder,None,game_state.t_curr)
    event_list.append_event(new_event,game_state.intruder,UavStatus.WAIT)
