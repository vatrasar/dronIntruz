from GameObjects import Hand, Uav
from GameState import GameState
from Settings import Settings
from events import Event_list, Event
import typing
from Enums.StatusEnum import UavStatus, HandStatus, Sides
from tools.geometric_tools import get_2d_vector_from_polar
from tools.velocity_tools import get_time_to_reach_point_in_streinght_line


def get_drones_in_range()->typing.List[Uav]:
    pass


def is_attack_by_any_hand(drone,game_state:GameState):
    return False


def send_hand_to_drone(terget_uav, owner):
    pass


def plan_move_r(event_list:Event_list, owner:Hand,game_state:GameState,settings:Settings):
    if(owner.next_event!=None):
        event_list.delete_event(owner.next_event)
        owner.next_event=None
    drones_in_range=get_drones_in_range()
    if(len(drones_in_range)!=0):
        #objects with no assigned hand
        drones_to_handle_list=[]
        for drone in drones_in_range:
            if(drone.status!=UavStatus.TIER_1 and not(is_attack_by_any_hand(drone,game_state))):
                drones_to_handle_list.append(drone)
        
        if(len(drones_to_handle_list)):
            send_hand_to_drone(drones_to_handle_list[0],owner)
            return


        #object already under attack of secound hand
        drones_to_handle_list = []
        for drone in drones_in_range:
            if(drone.status!=UavStatus.TIER_1):
                drones_to_handle_list.append(drone)
        if(len(drones_to_handle_list)>0):
            send_hand_to_drone(drones_to_handle_list,owner)
            return


        #object on tier 1, not tracked by secound hand
        drones_to_handle_list = []
        for drone in drones_in_range:
            if(drone.status==UavStatus.TIER_1 and not(is_attack_by_any_hand(drone,game_state))):
                drones_to_handle_list.append(drone)
        if(len(drones_to_handle_list)>0):
            send_hand_to_drone(drones_to_handle_list,owner)
            return


        #rest of drones
        send_hand_to_drone(drones_in_range, owner)
    else:
        if(owner.status!=HandStatus.TIER_0):
            target=None
            if(owner.side==Sides.RIGHT):
                target=get_2d_vector_from_polar(3.14/2,settings.intuder_size+settings.hand_size)
            else:
                target = get_2d_vector_from_polar(3.14 *3/ 2, settings.intuder_size + settings.hand_size)
            time_of_event=get_time_to_reach_point_in_streinght_line(owner.position,target,settings.velocity_hand)
            new_event=Move_r(time_of_event,target,owner,HandStatus.TIER_0,game_state.t_curr)
            event_list.append_event(new_event,owner,HandStatus.BACK)




class Move_r(Event):
    pass


