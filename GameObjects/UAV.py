
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import math

from Enums.StatusEnum import UavStatus


from GameObjects.MovableObject import MovableObject
from tools.geometric_tools import get_random_position, get_2d_distance, get_transform_between_points, \
    get_vector_with_length_and_direction
from tools.velocity_tools import get_time_to_reach_point_in_streinght_line, get_position_on_circle_base_on_travel_time, \
    get_move_point


class Uav(MovableObject):
    def __init__(self,x,y,status, points,velocity,index):
        super(Uav, self).__init__(x,y,status,40,velocity)
        self.points=points
        self.last_path=[]
        self.index=index











    def plan_help(self):
        pass

    def add_points(self, points):
        self.points=self.points+points

    def get_postions_after_update(self, t_curr, settings):


        delta_time = t_curr - self.next_event.last_postion_update_time

        new_postion = self.position

        if delta_time == 0.0:
            return self.position

        if (self.next_event.next_status == UavStatus.TIER_1 and self.status == UavStatus.TIER_1):  # move on circle

            new_postion = get_position_on_circle_base_on_travel_time(self, delta_time, settings)
        elif (self.status == UavStatus.TIER_2):
            return self.position

        else:
            if get_2d_distance(self.position, self.next_event.target_position) < 0.001:
                return self.position
            transofrm_between_points = get_transform_between_points(self.position, self.next_event.target_position)
            velocity_vector = get_vector_with_length_and_direction(settings.v_of_uav, transofrm_between_points)
            move_vector = get_move_point(velocity_vector, delta_time, self.position)
            new_postion = move_vector

        return new_postion

    
