from gameObjects.MovableObject import MovableObject


class Hand(MovableObject):
    def __init__(self,x,y,status):
        super(Hand, self).__init__(x,y,status,40)