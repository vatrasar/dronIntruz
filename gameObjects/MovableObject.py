from gameObjects.Point import Point
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



