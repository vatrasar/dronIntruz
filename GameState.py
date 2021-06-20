from gameObjects.Hand import Hand
from gameObjects.Intruder import Intruder
from gameObjects.UAV import Uav


class GameState():
    def __init__(self,settings_map):
        self.t_curr=0
        #init UAv
        self.uav_list = []
        self.intruder=Intruder(0,0,"",40,settings_map["intruder_max_energy"],settings_map)
        for i in range(0,settings_map["uav_number"]):
            self.uav_list.append(Uav(0,0,"",0))

        #init hands
        self.hands_list = []
        for i in range(0,settings_map["hands_number"]):
            self.hands_list.append(Hand(0,0,""))


    #intruz
    def update_time(self,new_time):
        self.t_curr=new_time

    def update_elements_positions(self):
        pass

    def check_collisions(self):
        pass

    def update_points_and_energy(self):
        pass
