import typing

from Enums.StatusEnum import UavStatus, Sides
from Hand import Hand

from Intruder import Intruder
from UAV import Uav

from tools.geometric_tools import get_2d_distance
from tools.velocity_tools import get_time_to_reach_point_in_streinght_line, get_position_on_line_base_on_travel_time


class GameState():
    def __init__(self, settings):
        self.t_curr=0
        self.visualize_first=True

        #init UAv
        self.uav_list:typing.List[Uav] = []
        self.list_of_dead_uavs=[]
        self.intruder=Intruder("", 40, settings.intruder_max_energy, settings)
        for i in range(0, settings.uav_number):
            self.uav_list.append(Uav(0,0,UavStatus.TIER_2,0,settings.v_of_uav,i))

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

            self.remove_drone(event_list, uav_to_delete)

    def remove_drone(self, event_list, uav_to_delete):
        event_list.delete_event(uav_to_delete.next_event)
        for hand in self.hands_list:
            if hand.chasing_drone == uav_to_delete:
                hand.set_chasing_drone(None)
        self.list_of_dead_uavs.append(uav_to_delete)
        uav_to_delete.set_status(UavStatus.DEAD)
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


            uav_copy=Uav(uav.position.x,uav.position.y,uav.status,uav.points,uav.velocity,uav.index)
            stat_game_state.uav_list.append(uav_copy)
        if len(self.list_of_dead_uavs) > 0:
            for uav in self.list_of_dead_uavs:
                uav_copy = Uav(uav.position.x, uav.position.y, uav.status, uav.points, uav.velocity, uav.index)
                stat_game_state.uav_list.append(uav_copy)
        if stat_game_state.uav_list[0].index>stat_game_state.uav_list[1].index:
            stat_game_state.uav_list.reverse()


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