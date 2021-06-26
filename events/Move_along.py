import sys, os, inspect

from tools.geometric_tools import get_2d_distance, get_random_position
from tools.search_tools import select_temp_path_back, search_p_a_back, plan_move_attack, search_p_a_attack
from tools.velocity_tools import get_position_on_circle_base_on_travel_time, get_time_to_reach_point_in_streinght_line, \
    get_d_t_arrive_poison

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


import random



from GameObjects import Uav
from events import Event
from events.Event_list import Event_list

from Settings import Settings

from Enums.StatusEnum import UavStatus

class Move_along(Event):



    def handle_event(self, event_list:Event_list, game_state, settings:Settings, rand: random.Random):
        event_list.delete_event(self)
        uav:Uav=self.event_owner
        uav.position=self.target_position
        if(uav.status==UavStatus.TIER_2):
            plan_move_along(game_state,settings,rand,event_list,uav)
            return
        else:
            #plan intruder reaction
            for hand in game_state.hands_list:
                hand.move_hand()

            path=search_p_a_attack()
            if(len(path)!=0):
                if(settings.mode=="RW-RA"):
                    x=rand.random()
                    if(x<settings.prob_of_attack):
                        plan_move_attack()
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
                        plan_move_along(game_state,settings,rand,event_list,uav)



def plan_move_along(game_state,settings,rand,event_list:Event_list,uav:Uav):
    dt_arrive=0
    new_position=None

    if(uav.status==UavStatus.TIER_2):
        if(game_state.t_curr==0): #first enter on tier1

            dt_arrive= get_d_t_arrive_poison(settings)
            is_new_position_correct=False
            while(not(is_new_position_correct)):
                new_position=get_random_position(rand,game_state,settings)
                is_new_position_correct=game_state.is_correct(new_position,dt_arrive)
        else:#return from tier 2
            is_new_position_correct = False
            while(not(is_new_position_correct)):
                new_position = get_random_position(rand, game_state, settings)
                dt_arrive=uav.get_time_to_position(new_position)
                is_new_position_correct=game_state.is_correct(new_position,dt_arrive)
        event_time=game_state.t_curr+dt_arrive
        new_event=Move_along(event_time,new_position,uav)
        event_list.append_event(new_event)

    elif(uav.status==UavStatus.TIER_1):#move on tier1
        if(settings["mode"]=="RW-RA"):
            is_new_position_correct = False
            while(not(is_new_position_correct)):
                d_ta_arrive =get_d_t_arrive_poison(settings)
                new_position = get_position_on_circle_base_on_travel_time(d_ta_arrive, new_position, settings,settings)
                is_new_position_correct=game_state.is_correct(new_position,d_ta_arrive)

    else:#back to from attack
        is_new_position_correct=False
        path=None
        temp_path = None
        while(not(is_new_position_correct)):
            path:list=search_p_a_back()
            if(len(path)==0):
                is_new_position_correct = False
                while(not(is_new_position_correct)):
                    temp_path=select_temp_path_back()
                    if(len(temp_path)==0):
                        uav.set_status(UavStatus.WAIT)
                        break
                    time=get_time_to_reach_point_in_streinght_line(uav.position,temp_path[len(temp_path)-1],settings)
                    is_new_position_correct=game_state.is_correct(temp_path[len(temp_path)-1],time)
            else:
                time = get_time_to_reach_point_in_streinght_line(uav.position, path[len(path) - 1],
                                                                 settings)
                is_new_position_correct=game_state.is_correct(path[len(path)-1],time)


        uav_distance_to_intruder=get_2d_distance(uav.position,game_state.intruder.position)
        if(0<uav_distance_to_intruder<settings.tier1_distance_from_intruder and len(path)!=0):# return from attack
            dt_arrive=get_time_to_reach_point_in_streinght_line(uav.position, path[0],settings)
            event_time=dt_arrive+game_state.t_curr
            new_event=Move_along(event_time,path[0],uav)
            event_list.append_event(new_event)
        elif(0<uav_distance_to_intruder<settings.tier1_distance_from_intruder and len(path)==0 and len(temp_path)==0):
            dt_arrive = get_time_to_reach_point_in_streinght_line(uav.position, temp_path[0], settings)
            event_time = dt_arrive + game_state.t_curr
            new_event = Move_along(event_time, temp_path[0], uav)
            event_list.append_event(new_event)
        elif(0<uav_distance_to_intruder<settings.tier1_distance_from_intruder and uav.status==UavStatus.WAIT):
            dt_arrive =settings.wiat_time
            event_time = dt_arrive + game_state.t_curr
            new_event = Move_along(event_time, uav.position, uav)
            uav.plan_help()
            event_list.append_event(new_event)









