from MovableObject import MovableObject


class Intruder(MovableObject):

    def __init__(self, status, object_size,init_energy_level,settings):
        super(Intruder, self).__init__(0, 0, status, object_size,0)

        self.energy=init_energy_level
        self.health=settings.beat_the_score


