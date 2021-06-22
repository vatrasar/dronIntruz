from gameObjects.MovableObject import MovableObject


class Uav(MovableObject):
    def __init__(self,x,y,status, points):
        super(Uav, self).__init__(x,y,status,40)
        self.points=points

    def plan_move_along(self,game_state):
        pass

    def search_p_a_attack(self):
        pass

    def plan_move_attack(self):
        pass
