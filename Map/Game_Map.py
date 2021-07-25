import math
import typing

import numpy as np


from GameState import GameState
from Map.FluidCel import FluidCell
from MovableObject import MovableObject
from Point import Point
from Settings import Settings
from UAV import Uav
from tools.geometric_tools import get_2d_distance, get_vector_angle, convert_to_360, get_transform_between_points, \
    move_point_with_vector, angle_positive, is_angle_in_range


def check_is_in_dron_search_range(cell_postion, drone_position, intruder_position,search_angle):
    transform_vecrot_to_intruder=get_transform_between_points(drone_position,intruder_position)
    temp_point=move_point_with_vector(cell_postion,transform_vecrot_to_intruder)
    intruder_tmep_point=move_point_with_vector(intruder_position,transform_vecrot_to_intruder)
    angle=math.degrees(convert_to_360(get_vector_angle(intruder_tmep_point)))
    anlge_max=angle_positive((angle+search_angle/2.0)%360)
    anlge_min=angle_positive((angle-search_angle/2.0)%360)
    orginal_angle=convert_to_360(get_vector_angle(temp_point))

    point_angle=math.degrees(convert_to_360(get_vector_angle(temp_point)))

    # print(("current %.2f radians %.2f point %.2f %.2f")%(point_angle,orginal_angle,temp_point.x,temp_point.y))
    return is_angle_in_range(point_angle,anlge_min,anlge_max)



def check_is_in_dron_search_range_back(cell_postion, drone_position, intruder_position,search_angle):
    transform_vecrot_to_intruder=get_transform_between_points(drone_position,intruder_position)
    temp_point=move_point_with_vector(cell_postion,transform_vecrot_to_intruder)
    intruder_tmep_point=move_point_with_vector(intruder_position,transform_vecrot_to_intruder)

    point_for_center_angle=Point(-intruder_tmep_point.x,-intruder_tmep_point.y)
    angle=math.degrees(convert_to_360(get_vector_angle(point_for_center_angle)))
    anlge_max=angle_positive((angle+search_angle/2.0)%360)
    anlge_min=angle_positive((angle-search_angle/2.0)%360)
    orginal_angle=convert_to_360(get_vector_angle(temp_point))

    point_angle=math.degrees(convert_to_360(get_vector_angle(temp_point)))

    # print(("current %.2f radians %.2f point %.2f %.2f")%(point_angle,orginal_angle,temp_point.x,temp_point.y))
    return is_angle_in_range(point_angle,anlge_min,anlge_max)

class GameMap():
    def __init__(self,settings):
        map_size=settings.map_size
        self.dimension = settings.dimension
        self.x_min=-map_size
        self.x_max=map_size
        self.y_min=-map_size
        self.y_max=-map_size
        self.map_memmory = np.zeros((self.dimension, self.dimension), np.int32)
        self.fluid_map:typing.List[typing.List[FluidCell]]=[]
        self.fluid_memory = np.zeros((self.dimension, self.dimension), np.int32)
        self.map_resolution=settings.map_resolution
        self.poin_ranges=[(0, 100, 3), (100, 200, 5), (200, 361, 3)]



    def get_point_on_map_index(self,x,y):

        x_i = int(round((x - self.x_min) / self.map_resolution))
        y_i= int(round((y - self.y_min) / self.map_resolution))
        return (x_i,y_i)

    def convert_index_to_point(self,x_i,y_i):
        x=x_i*self.map_resolution
        x=x+self.x_min

        y=y_i*self.map_resolution
        y=y+self.y_min
        return (x,y)


    def set_object_on_map(self,object:MovableObject,object_size,object_id):
        drones_candidates: typing.List[Point] = []

        x_i, y_i = self.get_point_on_map_index(object.position.x, object.position.y)
        drones_candidates.append(Point(x_i, y_i))
        while (len(drones_candidates) != 0):

            drone_candidate = drones_candidates[0]
            drones_candidates.remove(drone_candidate)
            if get_2d_distance(self.get_cell_with_index(drone_candidate).position, object.position) <= object_size:
                self.map_memmory[drone_candidate.y][drone_candidate.x] = object_id
                self.fluid_memory[drone_candidate.y][drone_candidate.x] = object_id

                neighbours = self.get_cell_neighbours(drone_candidate.x, drone_candidate.y)
                neighbours_to_check = []
                for neighbour in neighbours:
                    if self.map_memmory[neighbour.y][neighbour.x] == 0:
                        neighbours_to_check.append(neighbour)

                drones_candidates.extend(neighbours_to_check)

    def update_map(self, game_state:GameState, settings,uav:Uav):

        self.map_memmory = np.zeros((self.dimension, self.dimension), np.int32)
        self.fluid_map=[]

        for i in range(0,self.dimension): #build fluid_map
            self.fluid_map.append([])
            for p in range(0, self.dimension):


                point = self.convert_index_to_point(p, i)
                point = Point(point[0], point[1])
                new_cell = FluidCell(-1, point, p, i,settings)
                self.fluid_map[i].append(new_cell)


        #seting object on map, code works but i turned it of becase of performacnes
        for uav in game_state.uav_list:#set uav positions on map
            self.set_object_on_map(uav,settings.uav_size,100)

        for hand in game_state.hands_list:  # set uav positions on map
            self.set_object_on_map(hand,settings.hand_size,200)


        self.set_object_on_map(game_state.intruder,settings.intuder_size,300)







    def get_floading_point(self, position)->FluidCell:
        x_i,y_i=self.get_point_on_map_index(position.x,position.y)
        cell=self.fluid_map[y_i][x_i]
        return cell

    def get_avaiable_neighbours(self, parrent_cell:FluidCell,uav,game_state:GameState,settings:Settings,first_cell):

        x=parrent_cell.index.x
        y=parrent_cell.index.y
        potential_neighbours_index_list = self.get_cell_neighbours(x, y)

        neighbours_cells_list=[]
        for cell_index in potential_neighbours_index_list:

            if self.check_is_index_proply(cell_index):
                cell=self.get_cell_with_index(cell_index)
                if cell==first_cell or cell==parrent_cell.parrent:
                    continue
                if cell.is_visited:
                    neighbours_cells_list.append(cell)
                #is in search range
                elif (check_is_in_dron_search_range(cell.position,uav.position,game_state.intruder.position,20) or get_2d_distance(cell.position,uav.position)<settings.tier1_distance_from_intruder*0.2):

                    #assing points
                    points=self.get_cell_points(cell, game_state, settings)
                    cell.set_points(points)
                    neighbours_cells_list.append(cell)
                    if self.fluid_memory[cell_index.y][cell_index.x]!=100:
                        self.fluid_memory[cell_index.y][cell_index.x]=12

        return neighbours_cells_list


        # neighbours_list=[]
        # x_i,y_i=self.get_point_on_map_index(parrent_cell.position.x,parrent_cell.position.y)
        #
        #
        # if(self.dimension>x_i+1 and y_i+1<self.dimension):
        #     cell=self.fluid_map[y_i+1][x_i+1]
        #     if get_2d_distance(cell.position,uav.position)<tier1_distance_from_intruder*1.3 and get_2d_distance(cell.position,uav.position)>tier1_distance_from_intruder:
        #
        #         neighbours_list.append(cell)
        #
        #
        # if(0<=x_i-1 and y_i+1<self.dimension):
        #     cell=self.fluid_map[y_i+1][x_i]
        #     if get_2d_distance(cell.position,uav.position)<tier1_distance_from_intruder*1.3 and get_2d_distance(cell.position,uav.position)>tier1_distance_from_intruder:
        #         neighbours_list.append(cell)
        #
        #
        #
        # return neighbours_list

    def get_cell_neighbours(self, x, y)->typing.List[Point]:
        potential_neighbours_index_list = []
        potential_neighbours_index_list.append(Point(x + 1, y))
        potential_neighbours_index_list.append(Point(x - 1, y))
        potential_neighbours_index_list.append(Point(x + 1, y + 1))
        potential_neighbours_index_list.append(Point(x, y + 1))
        potential_neighbours_index_list.append(Point(x - 1, y + 1))
        potential_neighbours_index_list.append(Point(x - 1, y - 1))
        potential_neighbours_index_list.append(Point(x, y - 1))
        potential_neighbours_index_list.append(Point(x + 1, y - 1))
        return potential_neighbours_index_list

    def get_cell_points(self, cell, game_state, settings):
        angle = get_vector_angle(cell.position)
        angle = math.degrees(convert_to_360(angle))
        for arange in self.poin_ranges:
            if arange[0] <= angle and arange[1] > angle and get_2d_distance(cell.position,
                                                                            game_state.intruder.position) < settings.back_distance*1.1:
                return arange[2]
        return 0

    def check_is_index_proply(self, indeex_position:Point):
        return self.check_is_demision_proply(indeex_position.x) and self.check_is_demision_proply(indeex_position.y)

    def check_is_demision_proply(self, demision):
        return demision<self.dimension and demision>0

    def has_points_on_path(self):
        for row in self.fluid_map:
            for cell in row:
                if cell.points>0:
                    return True

        return False

    def get_best_points_in_range(self,settings):
        best_cell_in_range=self.fluid_map[0][0]

        for row in self.fluid_map:
            for cell in row:
                if best_cell_in_range.points<cell.points and cell.is_visited==True:
                    best_cell_in_range=cell

        if best_cell_in_range.points==settings.minimal_points:
            return None
        return best_cell_in_range

    def get_best_points_in_range_back(self,game_state:GameState,settings:Settings,uav):
        best_cell_in_range=self.fluid_map[0][0]

        for row in self.fluid_map:
            for cell in row:
                if cell.points==1 and game_state.is_correct_drone(cell.position,cell.uav_arrive_time+game_state.t_curr,uav,settings):
                    return cell


        return None

    def get_cell_with_index(self, cell_index)->FluidCell:
        return self.fluid_map[cell_index.y][cell_index.x]

    def show_path(self, path:typing.List[FluidCell]):
        i=50

        for element in path:
            self.fluid_memory[element.index.y][element.index.x]=i
            i=i+1

    def get_back_avaiable_neighbours(self, parrent_cell:FluidCell,uav,game_state:GameState,settings:Settings,first_cell,temp_ratio):

        x=parrent_cell.index.x
        y=parrent_cell.index.y
        potential_neighbours_index_list = self.get_cell_neighbours(x, y)

        neighbours_cells_list=[]
        for cell_index in potential_neighbours_index_list:

            if self.check_is_index_proply(cell_index):
                cell=self.get_cell_with_index(cell_index)
                if cell==first_cell or cell==parrent_cell.parrent:
                    continue
                if cell.is_visited:
                    neighbours_cells_list.append(cell)
                #is in search range
                elif (check_is_in_dron_search_range_back(cell.position,uav.position,game_state.intruder.position,20) or get_2d_distance(cell.position,uav.position)<settings.tier1_distance_from_intruder*0.2):

                    #assing points
                    points=self.get_cell_points_back(cell, game_state, settings,temp_ratio)
                    cell.set_points(points)
                    neighbours_cells_list.append(cell)
                    if self.fluid_memory[cell_index.y][cell_index.x]!=100:
                        self.fluid_memory[cell_index.y][cell_index.x]=12

        return neighbours_cells_list

    def get_cell_points_back(self, cell, game_state, settings,temp_ratio=1):
        if(get_2d_distance(game_state.intruder.position,cell.position)>=settings.tier1_distance_from_intruder*temp_ratio):
            return 1
        else:
            return 0

    def update_simple_map(self, game_state, uav_in_decision):
        self.map_memmory = np.zeros((self.dimension, self.dimension), np.int32)




        # seting object on map, code works but i turned it of becase of performacnes

        for uav in game_state.uav_list:#set uav positions on map
            x_i, y_i = self.get_point_on_map_index(uav.position.x, uav.position.y)
            if uav==uav_in_decision:
                self.map_memmory[y_i][x_i]=1
            else:
                self.map_memmory[y_i][x_i] = 2

        for hand in game_state.hands_list:  # set uav positions on map
            x_i, y_i = self.get_point_on_map_index(hand.position.x, hand.position.y)
            self.map_memmory[y_i][x_i] = 3

















