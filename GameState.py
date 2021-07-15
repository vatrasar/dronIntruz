

from Enums.StatusEnum import UavStatus, HandStatus, Sides
from GameObjects.Hand import Hand
from GameObjects.Intruder import Intruder
from GameObjects import Uav
from tools.geometric_tools import get_2d_distance


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
        if(settings.hands_number==1):
            self.hands_list.append(Hand(0,0,"",settings.velocity_hand,Sides.RIGHT,settings))
        elif(settings.hands_number==2):
            self.hands_list.append(Hand(0, 0, "", settings.velocity_hand, Sides.RIGHT,settings))
            self.hands_list.append(Hand(0, 0, "", settings.velocity_hand, Sides.LEFT,settings))





    #intruz
    def update_time(self,new_time):
        self.t_curr=new_time

    def update_elements_positions(self,settings):


        for uav in self.uav_list:
            uav.update_position(self.t_curr, settings)

        for hand in self.hands_list:
            if hand.next_event!=None:
                hand.update_position(self.t_curr, settings)

    def check_collisions(self,settings,event_list):
        uav_list_to_delete=[]
        for uav in self.uav_list:
            for hand in self.hands_list:
                if get_2d_distance(uav.position,hand.position)<settings.hand_size+settings.uav_size:
                    uav_list_to_delete.append(uav)

        for uav_to_delete in uav_list_to_delete:
            print("colision!")

            event_list.delete_event(uav_to_delete.next_event)
            for hand in self.hands_list:
                if hand.chasing_drone==uav_to_delete:
                    hand.set_chasing_drone(None)
            self.uav_list.remove(uav_to_delete)



    def update_points_and_energy(self):
        pass
    def is_correct(self, position, d_ta_arrive):
        return True
