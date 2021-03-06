import sys, os, inspect
import typing

from GameState import GameState
from Map.FluidCel import FluidCell
from Map.Game_Map import GameMap

from events.Move_r import plan_move_r
from tools.geometric_tools import get_2d_distance, get_random_position, get_vector_angle, get_2d_vector_from_polar
from tools.search_tools import select_temp_path_back, search_p_a_back, search_p_a_attack, build_discrete_map
from tools.velocity_tools import get_position_on_circle_base_on_travel_time, get_time_to_reach_point_in_streinght_line, \
    get_d_t_arrive_poison

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


import random



from GameObjects import Uav, Point
from events import Event
from events.Event_list import Event_list

from Settings import Settings

from Enums.StatusEnum import UavStatus






class Move_along(Event):



    def handle_event(self, event_list:Event_list, game_state, settings:Settings, rand: random.Random):
        super().handle_event(event_list,game_state,settings,rand)
        uav:Uav=self.event_owner
        uav.position=self.target_position
        for hand in game_state.hands_list:
            plan_move_r(event_list,hand,game_state,settings)
        if(uav.status==UavStatus.TIER_2):
            plan_move_along(game_state,settings,rand,event_list,uav)
            return
        elif(uav.status==UavStatus.ON_BACK or uav.status==UavStatus.ON_TEMP_BACK):
            if settings.tier1_distance_from_intruder-get_2d_distance(uav.position, game_state.intruder.position) < settings.back_distance:
                #docking procedure on tier 1
                self.palan_docking_on_tier1(event_list, game_state, settings, uav)
                uav.last_path=[]
                return
            plan_move_back(game_state,settings,rand,event_list,uav)
            return
        else:

            # check if is time to start back
            if get_2d_distance(uav.position, game_state.intruder.position) < settings.back_distance or UavStatus.ON_BACK==uav.status:
                #assing points
                self.assing_points(game_state, settings, uav)
                plan_move_back(game_state,settings,rand,event_list,uav)


                return

            path=search_p_a_attack(game_state,settings,uav)
            uav.last_path=path
            if(len(path)>1):

                if(settings.mode=="RW-RA"):
                    x=1
                    if self.event_owner.status==UavStatus.ON_ATTACK:
                        x=0

                    else:
                        x=rand.random()

                    if(x<settings.prob_of_attack):
                        plan_move_attakc(game_state,settings,event_list,uav,path)
                        # print("attack:")
                    else:
                        x=rand.random()
                        if(x<settings.prob_of_return_to_T2):
                            uav.set_status(UavStatus.TIER_2)
                            plan_move_along(game_state,settings,rand,event_list,uav)#return 2t->1T
                        else:#move on tier1
                            plan_move_along(game_state,settings,rand,event_list,uav)
                    return

            else:#path not found

                if(settings.mode=="RW-RA"):
                    if(uav.status==UavStatus.TIER_1):
                        x = rand.random()
                        if (x < settings.prob_of_return_to_T2):
                            uav.set_status(UavStatus.TIER_2)
                            plan_move_along(game_state,settings,rand,event_list,uav)  # return 2t->1T
                        else:#move on tier 1
                            plan_move_along(game_state,settings,rand,event_list,uav)
                    else:
                        self.assing_points(game_state, settings, uav)
                        plan_move_back(game_state,settings,rand,event_list,uav)

    def assing_points(self, game_state, settings, uav):
        game_map: GameMap = build_discrete_map(game_state, settings, uav)
        uav_cell_index = game_map.get_point_on_map_index(uav.position.x, uav.position.y)
        cell = game_map.get_cell_with_index(Point(uav_cell_index[0], uav_cell_index[1]))
        points = game_map.get_cell_points(cell, game_state, settings)
        uav.add_points(points)
        uav.last_path = []

    def palan_docking_on_tier1(self, event_list, game_state:GameState, settings, uav):
        angle = get_vector_angle(uav.position)
        vector = get_2d_vector_from_polar(angle, settings.tier1_distance_from_intruder)
        docking_position = Point(vector[0], vector[1])

        arrive_time = game_state.t_curr + get_time_to_reach_point_in_streinght_line(uav.position, docking_position,
                                                                                    settings.v_of_uav)
        if(game_state.is_correct_drone(docking_position,arrive_time,uav,settings)):
            event = Move_along(arrive_time, docking_position, uav, UavStatus.TIER_1, game_state.t_curr)
            event_list.append_event(event, uav, UavStatus.ON_BACK)
        else:
            plan_wait(event_list, game_state, settings, uav)

    def set_next_status(self, next_status):
        self.next_status=next_status


def plan_move_along(game_state,settings,rand,event_list:Event_list,uav:Uav):
    dt_arrive=0
    new_position=None

    if(uav.status==UavStatus.TIER_2):
        if(game_state.t_curr==0): #first enter on tier1

            dt_arrive= get_d_t_arrive_poison(settings)
            is_new_position_correct=False
            while(not(is_new_position_correct)):
                new_position=get_random_position(rand,game_state,settings)
                is_new_position_correct=game_state.is_correct_drone(new_position,dt_arrive+game_state.t_curr,uav,settings)
        else:#return from tier 2
            is_new_position_correct = False

            while(not(is_new_position_correct)):
                new_position = get_random_position(rand, game_state, settings)
                dt_arrive=uav.get_time_to_position(new_position)
                is_new_position_correct=game_state.is_correct(new_position,dt_arrive)
        event_time=game_state.t_curr+dt_arrive
        new_event=Move_along(event_time,new_position,uav,UavStatus.TIER_1,game_state.t_curr)
        event_list.append_event(new_event,uav,UavStatus.TIER_2)


    elif(uav.status==UavStatus.TIER_1):#move on tier1
        if(settings.mode=="RW-RA"):
            is_new_position_correct = False
            d_ta_arrive=0
            while(not(is_new_position_correct)):
                d_ta_arrive =get_d_t_arrive_poison(settings)
                new_position = get_position_on_circle_base_on_travel_time(uav,d_ta_arrive, settings)
                is_new_position_correct=game_state.is_correct(new_position,d_ta_arrive)


            event_time = d_ta_arrive + game_state.t_curr
            new_event = Move_along(event_time, new_position, uav,UavStatus.TIER_1,game_state.t_curr)
            event_list.append_event(new_event,uav,UavStatus.TIER_1)




def plan_move_back(game_state,settings,rand,event_list:Event_list,uav:Uav):
    # print("atak stop")
    uav.set_status(UavStatus.ON_BACK)
    is_new_position_correct=False
    path=None
    temp_path = None



    while(not(is_new_position_correct)):
        path:list=search_p_a_back(game_state,settings,uav)
        uav.last_path=path
        if(len(path)<=1):#no rescue path
            is_new_position_correct = False

            temp_path=select_temp_path_back(game_state,settings,uav)
            if(len(temp_path)<=1):#no temp path
                uav.set_status(UavStatus.WAIT)
                break
            time=get_time_to_reach_point_in_streinght_line(uav.position,temp_path[1].position,settings.v_of_uav)
            time=time+game_state.t_curr
            is_new_position_correct=game_state.is_correct(temp_path[1],time)
        else:
            time = get_time_to_reach_point_in_streinght_line(uav.position, path[1].position,
                                                        settings.v_of_uav)
            time = time + game_state.t_curr
            is_new_position_correct=game_state.is_correct(path[1].position,time)


    uav_distance_to_intruder=get_2d_distance(uav.position,game_state.intruder.position)
    if(0<uav_distance_to_intruder<settings.tier1_distance_from_intruder and len(path)>1):# return from attack
        dt_arrive=get_time_to_reach_point_in_streinght_line(uav.position, path[1].position,settings.v_of_uav)
        event_time=dt_arrive+game_state.t_curr
        next_status=UavStatus.TIER_1
        if(len(path)>2):
            next_status=UavStatus.ON_BACK
        new_event=Move_along(event_time,path[1].position,uav,next_status,game_state.t_curr)
        event_list.append_event(new_event,uav,UavStatus.ON_BACK)
    elif(0<uav_distance_to_intruder<settings.tier1_distance_from_intruder and len(temp_path)>1):
        dt_arrive = get_time_to_reach_point_in_streinght_line(uav.position, temp_path[1].position, settings.v_of_uav)
        event_time = dt_arrive + game_state.t_curr
        next_status = UavStatus.ON_BACK
        if (len(temp_path) > 2):
            next_status = UavStatus.ON_TEMP_BACK
        new_event = Move_along(event_time, temp_path[1].position, uav, next_status, game_state.t_curr)
        event_list.append_event(new_event, uav, UavStatus.ON_TEMP_BACK)
    elif(0<uav_distance_to_intruder<settings.tier1_distance_from_intruder and uav.status==UavStatus.WAIT):
        plan_wait(event_list, game_state,  settings, uav)
    if uav.next_event==None:
        print("liul")


def plan_wait(event_list, game_state, settings, uav):
    dt_arrive = settings.wiat_time
    event_time = dt_arrive + game_state.t_curr
    next_status = UavStatus.ON_BACK

    new_event = Move_along(event_time, uav.position, uav, next_status, game_state.t_curr)
    uav.plan_help()
    event_list.append_event(new_event, uav, UavStatus.WAIT)


def plan_move_attakc(game_state:GameState,settings,event_list:Event_list,uav:Uav,path:typing.List[FluidCell]):
    target_position=path[1].position
    dt_arrive=get_time_to_reach_point_in_streinght_line(target_position,uav.position,settings.v_of_uav)
    event_time=dt_arrive+game_state.t_curr
    new_event=Move_along(event_time,target_position,uav,UavStatus.ON_ATTACK,game_state.t_curr)
    event_list.append_event(new_event,uav,UavStatus.ON_ATTACK)

