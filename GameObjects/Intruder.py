from GameObjects.MovableObject import MovableObject


class Intruder(MovableObject):

    def __init__(self, x, y, status, object_size,init_energy_level,settings):
        super().__init__(x, y, status, object_size,0)
        self.energy=init_energy_level
        self.health=settings.beat_the_score


