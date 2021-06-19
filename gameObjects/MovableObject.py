from gameObjects.Point import Point


class MovableObject():
    def __init__(self,x,y,status,object_size):
        self.position=Point(x,y)
        self.next_event=None
        self.status=status
        self.object_size=object_size

