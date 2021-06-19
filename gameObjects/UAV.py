from gameObjects.MovableObject import MovableObject


class Uav(MovableObject):
    def __init__(self,x,y,status, points):
        super(Uav, self).__init__(x,y,status,40)
        self.points=points
