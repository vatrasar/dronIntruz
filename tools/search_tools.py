import typing

import numpy as np

from GameObjects import Uav
from GameState import GameState
from Map.FluidCel import FluidCell
from Map.Game_Map import GameMap
from Settings import Settings
from tools.geometric_tools import get_2d_distance
from tools.velocity_tools import get_time_to_reach_point_in_streinght_line


def build_discrete_map(game_state:GameState,settings:Settings,uav):
    game_map=GameMap(settings)
    game_map.update_map(game_state,settings,uav)
    return game_map


def create_path(best_cell:FluidCell):
    path=[best_cell]
    current_cell=best_cell.parrent
    while current_cell!=None:
        path.append(current_cell)
        current_cell=current_cell.parrent


    path.reverse()

    return path




def search_p_a_attack(game_state:GameState,settings,uav:Uav):
    game_map:GameMap=build_discrete_map(game_state, settings,uav)
    floading_algo(game_map, game_state, settings, uav)
    if(game_map.has_points_on_path()):
        best_cell=game_map.get_best_points_in_range()
        if best_cell.points==-1:
            return []
        path=create_path(best_cell)
        return path
    else:#no path to target
        return []
    #get best


def floading_algo(game_map, game_state, settings, uav):




    floadin_queue = []
    cell = game_map.get_floading_point(uav.position)
    cell.uav_arrive_time = 0
    floadin_queue.append(cell)



    # fluid marks
    while (len(floadin_queue) > 0):
        cell = floadin_queue[0]
        floadin_queue.remove(cell)

        neighbours_list: typing.List[FluidCell] = game_map.get_avaiable_neighbours(cell,
                                                                                   settings.tier1_distance_from_intruder,
                                                                                   uav)
        avaiable_neighbours = []
        # check naighbours. set parent and arrive time
        for neighbour in neighbours_list:
            neighbour.set_visited(True)
            new_parrent = None
            if neighbour.parrent == None:
                new_parrent = cell
            elif neighbour.parrent.uav_arrive_time >= cell.uav_arrive_time or neighbour.parrent.uav_arrive_time == -1:
                new_parrent = cell
            else:
                new_parrent = neighbour.parrent
            distance = get_2d_distance(neighbour.position, new_parrent.position)
            arrive_time = new_parrent.uav_arrive_time + distance / settings.v_of_uav
            is_point_avaiable = True
            # check hand arrive_time
            for hand in game_state.hands_list:
                time_to_reach_position_by_hand = get_time_to_reach_point_in_streinght_line(hand.position,
                                                                                           neighbour.position,
                                                                                           settings.velocity_hand)
                if (time_to_reach_position_by_hand < arrive_time):
                    is_point_avaiable = False
                    break

            if is_point_avaiable:
                avaiable_neighbours.append(neighbour)
                neighbour.set_uav_arrive_time(arrive_time)
                neighbour.set_parrent(cell)

        floadin_queue.extend(neighbours_list)






def search_p_a_back() -> list:
    return []


def select_temp_path_back() -> list:
    return []