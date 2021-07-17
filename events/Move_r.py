import math

from GameObjects import Hand, Uav, Point
from GameState import GameState
from Settings import Settings
from events import Event_list, Event
import typing
from Enums.StatusEnum import UavStatus, HandStatus, Sides
from tools.geometric_tools import get_2d_vector_from_polar, get_2d_distance, get_vector_angle, \
    get_postion_when_origin_is_central_point, convert_to_360
from tools.velocity_tools import get_time_to_reach_point_in_streinght_line
import random


def get_drones_in_range(game_state:GameState)->typing.List[Uav]:
    drones_in_range=[]
    for uav in game_state.uav_list:
        if uav.status!=UavStatus.TIER_2:
            drones_in_range.append(uav)
    return drones_in_range


def is_attack_by_any_hand(drone,game_state:GameState):
    is_under_attack=False
    for hand in game_state.hands_list:
        if(hand.chasing_drone==drone):
            return True

    return is_under_attack


def send_hand_to_drone(drones, hand,game_state:GameState,settings,event_list:Event_list):
    #choose drone closest to intruder
    closest_drone=drones[0]
    for drone in drones:
        if(get_2d_distance(drone.position,game_state.intruder.position)<get_2d_distance(closest_drone.position,game_state.intruder.position)):
            closest_drone=drone

    tier0_pose = hand.get_hand_tier0_position(settings)
    distance_to_tier0=0
    if(get_2d_distance(closest_drone.position,tier0_pose)>settings.r_of_LR):
        distance_to_tier0=settings.r_of_LR
    else:
        distance_to_tier0=get_2d_distance(closest_drone.position,tier0_pose)

    hand.set_chasing_drone(closest_drone)
    # drone_position_with_new_central=get_postion_when_origin_is_central_point(closest_drone.position,hand.get_hand_tier0_position(settings))
    # angle=get_vector_angle(drone_position_with_new_central)
    # vector=get_2d_vector_from_polar(angle,distance)
    # result_postion=Point(vector[0]+tier0_pose.x,vector[1]+tier0_pose.y)

    distance = get_distance_from_hand_to_intruder(closest_drone, distance_to_tier0, tier0_pose,game_state)

    angle=get_vector_angle(closest_drone.position)
    positon_result=get_2d_vector_from_polar(angle,distance)
    positon_result=Point(positon_result[0],positon_result[1])

    dt_arrive=get_time_to_reach_point_in_streinght_line(hand.position,positon_result,settings.velocity_hand)
    dt_arrive=game_state.t_curr+dt_arrive
    new_event=Move_r(dt_arrive,positon_result,hand,HandStatus.DEFENCE,game_state.t_curr)
    if(dt_arrive-game_state.t_curr>=settings.minimal_hand_move_time):
        event_list.append_event(new_event,hand,HandStatus.DEFENCE)


def get_distance_from_hand_to_intruder(closest_drone, distance_to_tier0, tier0_pose,game_state:GameState):
    angle1 = get_vector_angle(closest_drone.position)
    angle2 = get_vector_angle(tier0_pose)
    angle = abs(convert_to_360(angle2) - convert_to_360(angle1))
    if (angle > 3.14):
        angle = 2 * 3.14 - angle


    distanec_tier0_intruder=get_2d_distance(game_state.intruder.position,tier0_pose)
    sinB=(distanec_tier0_intruder/distance_to_tier0)*math.sin(angle)
    Bdegrees=None
    try:
        Bdegrees=math.degrees(math.asin(sinB))
    except Exception:
        print("lol")

    lambda_degrees=180-math.degrees(angle)-Bdegrees
    distace=(math.sin(math.radians(lambda_degrees))/math.sin(angle))*distance_to_tier0

    return distace


def plan_move_r(event_list:Event_list, owner:Hand,game_state:GameState,settings:Settings):
    owner.set_chasing_drone(None)
    if(owner.next_event!=None):
        event_list.delete_event(owner.next_event)
        owner.next_event=None
    drones_in_range=get_drones_in_range(game_state)
    if(len(drones_in_range)!=0):
        #objects with no assigned hand
        drones_to_handle_list=[]
        for drone in drones_in_range:
            if(drone.status!=UavStatus.TIER_1 and not(is_attack_by_any_hand(drone,game_state))):
                drones_to_handle_list.append(drone)
        
        if(len(drones_to_handle_list)):
            send_hand_to_drone(drones_to_handle_list,owner,game_state,settings,event_list)
            return


        #object already under attack of secound hand
        drones_to_handle_list = []
        for drone in drones_in_range:
            if(drone.status!=UavStatus.TIER_1):
                drones_to_handle_list.append(drone)
        if(len(drones_to_handle_list)>0):
            send_hand_to_drone(drones_to_handle_list,owner,game_state,settings,event_list)
            return


        #object on tier 1, not tracked by secound hand
        drones_to_handle_list = []
        for drone in drones_in_range:
            if(drone.status==UavStatus.TIER_1 and not(is_attack_by_any_hand(drone,game_state))):
                drones_to_handle_list.append(drone)
        if(len(drones_to_handle_list)>0):
            send_hand_to_drone(drones_to_handle_list,owner,game_state,settings,event_list)
            return


        #rest of drones
        send_hand_to_drone(drones_in_range, owner,game_state,settings,event_list)
    else:
        if(owner.status!=HandStatus.TIER_0):
            target=None
            target = owner.get_hand_tier0_position( settings)
            time_of_event=game_state.t_curr+get_time_to_reach_point_in_streinght_line(owner.position,target,settings.velocity_hand)
            new_event=Move_r(time_of_event,target,owner,HandStatus.TIER_0,game_state.t_curr)
            event_list.append_event(new_event,owner,HandStatus.BACK)





class Move_r(Event):
    def handle_event(self, event_list: Event_list, game_state, settings: Settings, rand: random.Random):
        super(Move_r, self).handle_event(event_list,game_state,settings,rand)
        self.event_owner.set_new_position(self.target_position)
        plan_move_r(event_list,self.event_owner,game_state,settings)





