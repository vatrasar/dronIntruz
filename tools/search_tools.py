import typing

import numpy as np

from GameObjects import Uav
from GameState import GameState
from Map.FluidCel import FluidCell
from Map.Game_Map import GameMap
from Settings import Settings
from tools.geometric_tools import get_2d_distance
from tools.velocity_tools import get_time_to_reach_point_in_streinght_line, get_position_on_line_base_on_travel_time


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


def is_last_path_ok(last_path:typing.List[FluidCell], game_state:GameState,settings):
    if len(last_path)<2:
        return False
    current_cell=last_path[1]
    last_path.remove(current_cell)
    for cell in last_path:
        cell.uav_arrive_time=cell.uav_arrive_time-current_cell.uav_arrive_time
        if not(is_point_save(cell.uav_arrive_time,game_state,cell,settings)):
            return False

    return True




def search_p_a_attack(game_state:GameState,settings,uav:Uav):
    if(is_last_path_ok(uav.last_path,game_state,settings)):
        return uav.last_path

    game_map:GameMap=build_discrete_map(game_state, settings,uav)
    floading_algo_attack(game_map, game_state, settings, uav)
    if(game_map.has_points_on_path()):
        best_cell=game_map.get_best_points_in_range()
        if best_cell.points==-1:
            return []
        path=create_path(best_cell)
        game_map.show_path(path)
        return path
    else:#no path to target
        return []
    #get best


def floading_algo_back(game_map:GameMap, game_state, settings, uav):
    floadin_queue = []
    old_cell = game_map.get_floading_point(uav.position)
    old_cell.uav_arrive_time = 0
    floadin_queue.append(old_cell)

    first_cell = old_cell
    # fluid marks
    while (len(floadin_queue) > 0):

        old_cell = floadin_queue[0]
        floadin_queue.remove(old_cell)
        old_cell.is_queue=False

        neighbours_list: typing.List[FluidCell] = game_map.get_back_avaiable_neighbours(old_cell,uav,game_state,settings,first_cell)

        parents_list=[]
        # check naighbours. set parent and arrive time
        for neighbour in neighbours_list:
            is_parrent=True
            neighbour.set_visited(True)
            new_parrent = None
            if neighbour.parrent == None or neighbour.parrent.uav_arrive_time >= old_cell.uav_arrive_time or neighbour.parrent.uav_arrive_time == -1:
                new_parrent = old_cell

            else:
                is_parrent=False
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

            if is_point_avaiable and is_parrent and neighbour.is_queue==False:
                if neighbour.points==0:
                    parents_list.append(neighbour)
                neighbour.set_uav_arrive_time(arrive_time)
                neighbour.set_parrent(new_parrent)
                neighbour.is_queue=True



        floadin_queue.extend(parents_list)

def floading_algo_attack(game_map, game_state, settings, uav):




    floadin_queue = []
    old_cell = game_map.get_floading_point(uav.position)
    old_cell.uav_arrive_time = 0
    floadin_queue.append(old_cell)

    first_cell = old_cell
    # fluid marks
    while (len(floadin_queue) > 0):

        old_cell = floadin_queue[0]
        floadin_queue.remove(old_cell)
        old_cell.is_queue=False

        neighbours_list: typing.List[FluidCell] = game_map.get_avaiable_neighbours(old_cell,uav,game_state,settings,first_cell)

        parents_list=[]
        # check naighbours. set parent and arrive time
        for neighbour in neighbours_list:
            is_parrent=True
            neighbour.set_visited(True)
            new_parrent = None
            if neighbour.parrent == None or neighbour.parrent.uav_arrive_time >= old_cell.uav_arrive_time or neighbour.parrent.uav_arrive_time == -1:
                new_parrent = old_cell

            else:
                is_parrent=False
                new_parrent = neighbour.parrent
            distance = get_2d_distance(neighbour.position, new_parrent.position)
            arrive_time = new_parrent.uav_arrive_time + distance / settings.v_of_uav
            is_point_avaiable = True
            # check hand arrive_time
            is_point_avaiable = is_point_save(arrive_time, game_state,  neighbour, settings)

            if is_point_avaiable and is_parrent and neighbour.is_queue==False:
                if neighbour.points==0:
                    parents_list.append(neighbour)
                neighbour.set_uav_arrive_time(arrive_time)
                neighbour.set_parrent(new_parrent)
                neighbour.is_queue=True



        floadin_queue.extend(parents_list)


def is_point_save(arrive_time, game_state, neighbour, settings):
    is_point_avaiable=True
    for hand in game_state.hands_list:
        time_to_reach_position_by_hand = get_time_to_reach_point_in_streinght_line(hand.position,
                                                                                   neighbour.position,
                                                                                   settings.velocity_hand)
        hand_estimated_position = get_position_on_line_base_on_travel_time(hand.position, neighbour.position,
                                                                           settings.velocity_hand, arrive_time)
        if (time_to_reach_position_by_hand < arrive_time) or get_2d_distance(hand_estimated_position,neighbour.position) < 1.3 * (settings.hand_size + settings.uav_size):
            is_point_avaiable = False
            break
    return is_point_avaiable


def search_p_a_back(game_state:GameState,settings,uav:Uav) -> list:
    if (is_last_path_ok(uav.last_path, game_state, settings)):
        return uav.last_path
    game_map: GameMap = build_discrete_map(game_state, settings, uav)
    floading_algo_back(game_map, game_state, settings, uav)
    if (game_map.has_points_on_path()):
        best_cell = game_map.get_best_points_in_range_back()
        if best_cell==None:
            return []

        path = create_path(best_cell)
        game_map.show_path(path)
        return path
    else:  # no path to target
        return []
    # get best


def select_temp_path_back() -> list:
    return []