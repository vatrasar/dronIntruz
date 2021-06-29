
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import math

from Enums.StatusEnum import UavStatus


from GameObjects.MovableObject import MovableObject
from tools.geometric_tools import get_random_position, get_2d_distance
from tools.velocity_tools import get_time_to_reach_point_in_streinght_line, get_position_on_circle_base_on_travel_time


class Uav(MovableObject):
    def __init__(self,x,y,status, points,velocity):
        super(Uav, self).__init__(x,y,status,40,velocity)
        self.points=points











    def plan_help(self):
        pass

    
