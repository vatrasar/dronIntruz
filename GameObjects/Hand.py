from GameObjects.MovableObject import MovableObject


class Hand(MovableObject):
    def __init__(self,x,y,status,velocity_hand):
        super(Hand, self).__init__(x,y,status,40,velocity_hand)
    def move_hand(self):
        pass