

from Enums.StatusEnum import UavStatus
from GameObjects.Hand import Hand
from GameObjects.Intruder import Intruder
from GameObjects import Uav


class GameState():
    def __init__(self, settings):
        self.t_curr=0
        self.visualize_first=True

        #init UAv
        self.uav_list = []
        self.intruder=Intruder("", 40, settings.intruder_max_energy, settings)
        for i in range(0, settings.uav_number):
            self.uav_list.append(Uav(0,0,UavStatus.TIER_2,0,settings.v_of_uav))

        #init hands
        self.hands_list = []
        for i in range(0, settings.hands_number):
            self.hands_list.append(Hand(0,0,"",settings.velocity_hand))


    #intruz
    def update_time(self,new_time):
        self.t_curr=new_time

    def update_elements_positions(self,settings):
        for uav in self.uav_list:
            uav.update_position(self.t_curr, settings)

    def check_collisions(self):
        pass

    def update_points_and_energy(self):
        pass
    def is_correct(self, position, d_ta_arrive):
        return True
