import math
import typing

import numpy as np

from GameObjects import Point, Uav
from GameState import GameState
from Map.FluidCel import FluidCell
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

class GameMap():
    def __init__(self,settings):
        map_size=settings.tier1_distance_from_intruder*1.3
        self.dimension = int((map_size - (-map_size)) / settings.map_resolution)
        self.x_min=-map_size
        self.x_max=map_size
        self.y_min=-map_size
        self.y_max=-map_size
        self.map_memmory = np.zeros((self.dimension, self.dimension), np.int32)
        self.fluid_map:typing.List[typing.List[FluidCell]]=[]

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

    def update_map(self, game_state:GameState, settings,uav:Uav):
        fluid_memory = np.zeros((self.dimension, self.dimension), np.int32)
        self.map_memmory = np.zeros((self.dimension, self.dimension), np.int32)
        self.fluid_map=[]
        for i in range(0,self.dimension):
            self.fluid_map.append([])
            for p in range(0, self.dimension):


                #drones
                for drone in game_state.uav_list:
                    point=self.convert_index_to_point(i,p)
                    point=Point(point[0],point[1])
                    if get_2d_distance(point,drone.position)<=settings.uav_size:

                        self.map_memmory[p][i]=self.map_memmory[p][i]+1

                #hands
                for hand in game_state.hands_list:
                    point=self.convert_index_to_point(i,p)
                    point=Point(point[0],point[1])
                    if get_2d_distance(point,hand.position)<=settings.hand_size:
                        self.map_memmory[p][i]=self.map_memmory[p][i]+1


                point = self.convert_index_to_point(i, p)
                point = Point(point[0], point[1])
                if get_2d_distance(point, game_state.intruder.position) <= settings.intuder_size:
                    self.map_memmory[p][i] = self.map_memmory[p][i]+1

                new_cell=FluidCell(-1, point)
                self.fluid_map[i].append(new_cell)

                angle=get_vector_angle(new_cell.position)

                angle=math.degrees(convert_to_360(angle))



                for arange in self.poin_ranges:
                    if arange[0]<=angle and arange[1]>angle and get_2d_distance(new_cell.position,game_state.intruder.position)<settings.intuder_size+settings.uav_size:
                        new_cell.set_points(arange[2])

                if(check_is_in_dron_search_range(new_cell.position,uav.position,game_state.intruder.position,20) or get_2d_distance(new_cell.position,uav.position)<settings.tier1_distance_from_intruder*0.2):
                    new_cell.set_is_safe(True)
                if new_cell.is_safe:
                    fluid_memory[p][i]=1
                else:
                    fluid_memory[p][i]=0
                if self.map_memmory[p][i]!=0:
                    fluid_memory[p][i] = 3
        print("tets")


    def get_floading_point(self, position)->FluidCell:
        x_i,y_i=self.get_point_on_map_index(position.x,position.y)
        cell=self.fluid_map[y_i][x_i]
        return cell

    def get_avaiable_neighbours(self, parrent_cell:FluidCell,tier1_distance_from_intruder,uav):

        neighbours_list=[]
        x_i,y_i=self.get_point_on_map_index(parrent_cell.position.x,parrent_cell.position.y)


        if(self.dimension>x_i+1 and y_i+1<self.dimension):
            cell=self.fluid_map[y_i+1][x_i+1]
            if get_2d_distance(cell.position,uav.position)<tier1_distance_from_intruder*1.3 and get_2d_distance(cell.position,uav.position)>tier1_distance_from_intruder:

                neighbours_list.append(cell)


        if(0<=x_i-1 and y_i+1<self.dimension):
            cell=self.fluid_map[y_i+1][x_i]
            if get_2d_distance(cell.position,uav.position)<tier1_distance_from_intruder*1.3 and get_2d_distance(cell.position,uav.position)>tier1_distance_from_intruder:
                neighbours_list.append(cell)



        return neighbours_list

    def has_points_on_path(self):
        for row in self.fluid_map:
            for cell in row:
                if cell.points>0:
                    return True

        return False

    def get_best_points_in_range(self):
        best_cell_in_range=self.fluid_map[0][0]

        for row in self.fluid_map:
            for cell in row:
                if best_cell_in_range.points<cell.points and cell.is_visited==True:
                    best_cell_in_range=cell


        return best_cell_in_range










