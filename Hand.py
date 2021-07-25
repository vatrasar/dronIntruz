from Enums.StatusEnum import Sides
from MovableObject import MovableObject
from Settings import Settings
from tools.geometric_tools import get_2d_vector_from_polar, get_2d_distance, get_transform_between_points, \
    get_vector_with_length_and_direction
from Point import Point
from tools.velocity_tools import get_move_point


class Hand(MovableObject):
    def __init__(self,x,y,status,velocity_hand,side:Sides,settings:Settings):
        super(Hand, self).__init__(x,y,status,40,velocity_hand)
        self.side=side
        self.chasing_drone=None

        tier_0_positon=self.get_hand_tier0_position(settings)
        self.position.x=tier_0_positon.x
        self.position.y=tier_0_positon.y
    def move_hand(self):
        pass

    def set_chasing_drone(self,drone_to_chase):
        self.chasing_drone=drone_to_chase

    def get_hand_tier0_position(self, settings):
        target = None
        if (self.side == Sides.RIGHT):
            target = get_2d_vector_from_polar(0, settings.intuder_size + settings.hand_size)
        else:
            target = get_2d_vector_from_polar(3.14, settings.intuder_size + settings.hand_size)

        return Point(target[0],target[1])


    def update_position(self, t_curr,settings):


        delta_time=t_curr-self.next_event.last_postion_update_time

        new_postion=None

        if delta_time==0.0:
            return



        if get_2d_distance(self.position,self.next_event.target_position)<0.001:
            return
        transofrm_between_points=get_transform_between_points(self.position,self.next_event.target_position)
        velocity_vector=get_vector_with_length_and_direction(settings.velocity_hand,transofrm_between_points)
        move_vector=get_move_point(velocity_vector,delta_time,self.position)
        new_position=move_vector




        self.next_event.last_postion_update_time=t_curr
        self.set_new_position(new_position)