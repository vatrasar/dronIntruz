from GameObjects import Point


class FluidCell():
    def __init__(self,arrive_time,position,i_x,i_y,settings):
        self.parrent:FluidCell=None
        self.uav_arrive_time=arrive_time
        self.points=settings.minimal_points
        self.is_safe=False
        self.position=position
        self.is_visited=False
        self.index=Point(i_x,i_y)
        self.is_queue=False

    def set_parrent(self, cell):
        self.parrent=cell

    def set_uav_arrive_time(self, uav_arrive_time):
        self.uav_arrive_time=uav_arrive_time

    def set_points(self, value):
        self.points=value

    def set_visited(self, new_value):
        self.is_visited=new_value

    def set_is_safe(self, new_value):
        self.is_safe=new_value
