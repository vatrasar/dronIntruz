from gameObjects.UAV import Uav


class GameState():
    def __init__(self,settings_map):
        self.uav_list = []
        for i in range(0,settings_map["uav_number"]):
            self.uav_list.append(Uav(0,0,"",0))
