from Enums.StatusEnum import Sides
from GameObjects.MovableObject import MovableObject


class Hand(MovableObject):
    def __init__(self,x,y,status,velocity_hand,side:Sides):
        super(Hand, self).__init__(x,y,status,40,velocity_hand)
        self.side=side
        self.chasing_drone=None
    def move_hand(self):
        pass

    def set_chasing_drone(self,drone_to_chase):
        self.chasing_drone=drone_to_chase