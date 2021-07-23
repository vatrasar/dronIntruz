

from Enums.StatusEnum import UavStatus, HandStatus, Sides
from GameObjects.Hand import Hand
from GameObjects.Intruder import Intruder
from GameObjects import Uav
from events import Event
from tools.geometric_tools import get_2d_distance
from tools.velocity_tools import get_time_to_reach_point_in_streinght_line, get_position_on_line_base_on_travel_time


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
    def is_correct_drone(self, position, d_ta_arrive, uav_to_move,settings):
        """

        :param position:
        :param d_ta_arrive: point in time when dron come to point. It is t_cur+delta
        :param uav_to_move:
        :param settings:
        :return:
        """

        if len(self.uav_list)==2:
            if  self.uav_list[0].next_event==None and self.uav_list[1].next_event==None:
                return True
            secound_uav=None
            for uav in self.uav_list:
                if uav!=uav_to_move:
                    secound_uav=uav
                    secound_uav_position_after_update=secound_uav.get_postions_after_update(d_ta_arrive,settings)
                    distanece=get_2d_distance(position,secound_uav_position_after_update)
                    if secound_uav.status!=UavStatus.TIER_2 and get_2d_distance(position,secound_uav_position_after_update) < 2 * (2*settings.uav_size):
                        return False

        return True

    def clone_game_state(self,settings):
        stat_game_state=GameState(settings)

        #hands
        stat_game_state.hands_list=[]
        for hand in self.hands_list:
            hand_copy=Hand(hand.position.x,hand.position.y,hand.status,hand.velocity,hand.side,settings)
            hand_copy.position.x=hand.position.x
            hand_copy.position.y=hand.position.y
            stat_game_state.hands_list.append(hand_copy)


        #drones
        stat_game_state.uav_list=[]
        for uav in self.uav_list:
            uav_copy=Uav(uav.position.x,uav.position.y,uav.status,uav.points,uav.velocity)
            stat_game_state.uav_list.append(uav_copy)


        stat_game_state.t_curr=self.t_curr

        return stat_game_state

    def is_point_save(self,arrive_time, game_state, neighbour, settings):
        is_point_avaiable = True
        for hand in game_state.hands_list:
            time_to_reach_position_by_hand = get_time_to_reach_point_in_streinght_line(hand.position,
                                                                                       neighbour.position,
                                                                                       settings.velocity_hand)
            hand_estimated_position = get_position_on_line_base_on_travel_time(hand.position, neighbour.position,
                                                                               settings.velocity_hand, arrive_time)
            if (time_to_reach_position_by_hand < arrive_time) or get_2d_distance(hand_estimated_position,
                                                                                 neighbour.position) < 1.3 * (
                    settings.hand_size + settings.uav_size):
                is_point_avaiable = False
                break
        return is_point_avaiable


    def is_point_save_from_hand(arrive_time, game_state, neighbour, settings):
        is_point_avaiable = True
        for hand in game_state.hands_list:
            time_to_reach_position_by_hand = get_time_to_reach_point_in_streinght_line(hand.position,
                                                                                       neighbour.position,
                                                                                       settings.velocity_hand)
            hand_estimated_position = get_position_on_line_base_on_travel_time(hand.position, neighbour.position,
                                                                               settings.velocity_hand, arrive_time)
            if (time_to_reach_position_by_hand < arrive_time) or get_2d_distance(hand_estimated_position,
                                                                                 neighbour.position) < 1.3 * (
                    settings.hand_size + settings.uav_size):
                is_point_avaiable = False
                break
        return is_point_avaiable