import sys, os, inspect

from Enums import UavStatus
from events import Event
from tools.velocity_tools import get_position_on_circle_base_on_travel_time, get_move_point

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from GameObjects.Point import Point
from tools.geometric_tools import get_2d_distance, get_transform_between_points, get_vector_with_length_and_direction





class MovableObject():
    def __init__(self,x,y,status,object_size,velocity):
        self.position=Point(x,y)
        self.next_event:Event=None
        self.status=status
        self.object_size=object_size
        self.velocity=float(velocity)


    def set_new_position(self, new_position):
        self.position=new_position

    def get_time_to_position(self,new_position):
        distance=get_2d_distance(self.position,new_position)
        time=distance/self.velocity
        return time

    def set_status(self,new_status):
        self.status=new_status

    def set_next_event(self,next_event):
        self.next_event=next_event

    def update_position(self, t_curr,settings):


        delta_time=t_curr-self.next_event.last_postion_update_time

        new_postion=None

        if delta_time==0.0:
            return


        if(self.next_event.next_status==UavStatus.TIER_1 and self.status==UavStatus.TIER_1): #move on circle


            new_position=get_position_on_circle_base_on_travel_time(self,delta_time,settings)
        elif(self.status==UavStatus.TIER_2):
            return

        else:
            if get_2d_distance(self.position,self.next_event.target_position)<0.001:
                return
            transofrm_between_points=get_transform_between_points(self.position,self.next_event.target_position)
            velocity_vector=get_vector_with_length_and_direction(settings.v_of_uav,transofrm_between_points)
            move_vector=get_move_point(velocity_vector,delta_time,self.position)
            new_position=move_vector




        self.next_event.last_postion_update_time=t_curr
        self.set_new_position(new_position)


