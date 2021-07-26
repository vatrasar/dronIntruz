import typing

from GameState import GameState
from Game_Map import GameMap
from Map.FluidCel import FluidCell


from Settings import Settings
from UAV import Uav
from tools.geometric_tools import get_2d_distance


def get_best_points_in_range(game_map, settings, game_state, uav):
    best_cell_in_range = game_map.fluid_map[0][0]

    for row in game_map.fluid_map:
        for cell in row:
            if best_cell_in_range.points < cell.points and cell.is_visited == True:
                best_cell_in_range = cell

    if best_cell_in_range.points == settings.minimal_points or not (is_back_from_postion(best_cell_in_range, uav, game_state, settings)):
        return None
    # if best_cell_in_range.points == settings.minimal_points:
    #     return None

    return best_cell_in_range

def is_back_from_postion(best_cell_in_range,uav,game_state:GameState,settings:Settings):
    # if (is_last_path_ok(uav.last_path, game_state, settings)):
    #     return uav.last_path
    game_map: GameMap = build_discrete_map(game_state, settings, uav)
    floading_algo_back(game_map, game_state, settings,best_cell_in_range.position,1,best_cell_in_range.uav_arrive_time)
    if (game_map.has_points_on_path()):
        best_cell = game_map.get_best_points_in_range_back(game_state,settings,uav)
        if best_cell==None:
            return False

        path = create_path(best_cell)
        game_map.show_path(path)
        return True
    else:  # no path to target
        return False
    # get best


def build_discrete_map(game_state:GameState,settings:Settings,uav):
    game_map=GameMap(settings)
    game_map.update_map(game_state,settings,uav)
    return game_map
def build_simple_discrete_map(game_state, settings, uav):
    game_map = GameMap(settings)
    game_map.update_simple_map(game_state, uav)
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
        if not(game_state.is_point_save(cell.uav_arrive_time,game_state,cell,settings)):
            return False

    return True




def search_p_a_attack(game_state:GameState,settings,uav:Uav):
    if(is_last_path_ok(uav.last_path,game_state,settings)):
        return uav.last_path

    game_map:GameMap=build_discrete_map(game_state, settings,uav)
    floading_algo_attack(game_map, game_state, settings, uav)
    if(game_map.has_points_on_path()):
        best_cell=get_best_points_in_range(game_map,settings,game_state,uav)
        if best_cell==None:
            return []
        path=create_path(best_cell)
        game_map.show_path(path)
        return path
    else:#no path to target
        return []
    #get best


def floading_algo_back(game_map:GameMap, game_state, settings, init_drone_postion,temp_ratio,init_time):
    floadin_queue = []
    old_cell = game_map.get_floading_point(init_drone_postion)
    old_cell.uav_arrive_time = init_time
    floadin_queue.append(old_cell)

    first_cell = old_cell
    # fluid marks
    while (len(floadin_queue) > 0):

        old_cell = floadin_queue[0]
        floadin_queue.remove(old_cell)
        old_cell.is_queue=False

        neighbours_list: typing.List[FluidCell] = game_map.get_back_avaiable_neighbours(old_cell,init_drone_postion,game_state,settings,first_cell,temp_ratio)

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

            if (not(game_state.is_point_save(arrive_time,game_state,neighbour,settings))):
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
            is_point_avaiable = game_state.is_point_save(arrive_time, game_state,  neighbour, settings)

            if is_point_avaiable and is_parrent and neighbour.is_queue==False:
                if neighbour.points==0:
                    parents_list.append(neighbour)
                neighbour.set_uav_arrive_time(arrive_time)
                neighbour.set_parrent(new_parrent)
                neighbour.is_queue=True



        floadin_queue.extend(parents_list)





def search_p_a_back(game_state:GameState,settings,uav:Uav) -> list:
    if (is_last_path_ok(uav.last_path, game_state, settings)):
        return uav.last_path
    game_map: GameMap = build_discrete_map(game_state, settings, uav)
    floading_algo_back(game_map, game_state, settings, uav.position,1,0)
    if (game_map.has_points_on_path()):
        best_cell = game_map.get_best_points_in_range_back(game_state,settings,uav)
        if best_cell==None:
            return []

        path = create_path(best_cell)
        game_map.show_path(path)
        return path
    else:  # no path to target
        return []
    # get best


def select_temp_path_back(game_state:GameState,settings,uav:Uav) -> list:
    if (is_last_path_ok(uav.last_path, game_state, settings)):
        return uav.last_path
    game_map: GameMap = build_discrete_map(game_state, settings, uav)
    floading_algo_back(game_map, game_state, settings, uav.position,0.6,0)
    if (game_map.has_points_on_path()):
        best_cell = game_map.get_best_points_in_range_back(game_state, settings, uav)
        if best_cell == None:
            return []

        path = create_path(best_cell)
        game_map.show_path(path)
        return path
    else:  # no path to target
        return []