import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from GameObjects.Point import Point
from tools.geometric_tools import get_2d_distance


class MovableObject():
    def __init__(self,x,y,status,object_size,velocity):
        self.position=Point(x,y)
        self.next_event=None
        self.status=status
        self.object_size=object_size
        self.velocity=float(velocity)

    def get_time_to_position(self,new_position):
        distance=get_2d_distance(self.position,new_position)
        time=distance/self.velocity
        return time

    def set_status(self,new_status):
        self.status=new_status




