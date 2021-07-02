from Enums.StatusEnum import Sides
from GameObjects.MovableObject import MovableObject
from Settings import Settings
from tools.geometric_tools import get_2d_vector_from_polar


class Hand(MovableObject):
    def __init__(self,x,y,status,velocity_hand,side:Sides,settings:Settings):
        super(Hand, self).__init__(x,y,status,40,velocity_hand)
        self.side=side
        self.chasing_drone=None

        tier_0_positon=self.get_hand_tier0_position(settings)
        self.position.x=tier_0_positon[0]
        self.position.y=tier_0_positon[1]
    def move_hand(self):
        pass

    def set_chasing_drone(self,drone_to_chase):
        self.chasing_drone=drone_to_chase

    def get_hand_tier0_position(self, settings):
        target = None
        if (self.side == Sides.RIGHT):
            target = get_2d_vector_from_polar(3.14 / 2, settings.intuder_size + settings.hand_size)
        else:
            target = get_2d_vector_from_polar(3.14 * 3 / 2, settings.intuder_size + settings.hand_size)
        return target