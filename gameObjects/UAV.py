import math

from Enum.StatusEnum import UavStatus
from Events.Event_list import Event_list
from Events.Move_along import Move_along
from GameState import GameState
from gameObjects.MovableObject import MovableObject
from tools.geometric_tools import get_random_position, get_alpha_for_distance_on_circle, get_vector_angle, \
    get_2d_vector_from_polar, get_2d_distance
from tools.velocity_tools import get_time_to_reach_point_in_streinght_line, get_position_on_circle_base_on_travel_time


class Uav(MovableObject):
    def __init__(self,x,y,status, points,velocity):
        super(Uav, self).__init__(x,y,status,40,velocity)
        self.points=points




    def plan_move_along(self,game_state:GameState,settings,rand,event_list:Event_list):
        dt_arrive=0
        new_position=None

        if(self.status==UavStatus.TIER_2):
            if(game_state.t_curr==0): #first enter on tier1
                d_ta_arrive=1
                d_ta_arrive = self.get_d_t_arrive_poison(settings)
                is_new_position_correct=False
                while(is_new_position_correct):
                    new_position=get_random_position(rand,game_state,settings)
                    is_new_position_correct=game_state.is_correct(new_position,d_ta_arrive)
            else:#return from tier 2
                is_new_position_correct = False
                while(is_new_position_correct):
                    new_position = get_random_position(rand, game_state, settings)
                    dt_arrive=self.get_time_to_position(new_position)
                    is_new_position_correct=game_state.is_correct(new_position,dt_arrive)
            event_time=game_state.t_curr+dt_arrive
            new_event=Move_along(event_time,new_position,self)
            event_list.append_event(new_event)

        elif(self.status==UavStatus.TIER_1):#move on tier1
            if(settings["mode"]=="RW-RA"):
                is_new_position_correct = False
                while(is_new_position_correct):
                    d_ta_arrive =self.get_d_t_arrive_poison(settings)
                    new_position = get_position_on_circle_base_on_travel_time(d_ta_arrive, new_position, settings)
                    is_new_position_correct=game_state.is_correct(new_position,d_ta_arrive)

        else:#back to from attack
            is_new_position_correct=False
            path=None
            temp_path = None
            while(is_new_position_correct):
                path:list=self.search_p_a_back()
                if(len(path)==0):
                    while(is_new_position_correct):
                        temp_path=self.select_temp_path_back()
                        if(len(temp_path)==0):
                            self.set_status(UavStatus.WAIT)
                            break
                        time=get_time_to_reach_point_in_streinght_line(self.position,temp_path[len(temp_path)-1],settings)
                        is_new_position_correct=game_state.is_correct(temp_path[len(temp_path)-1],time)
                else:
                    time = get_time_to_reach_point_in_streinght_line(self.position, path[len(path) - 1],
                                                                     settings)
                    is_new_position_correct=game_state.is_correct(path[len(path)-1],time)


            uav_distance_to_intruder=get_2d_distance(self.position,game_state.intruder.position)
            if(0<uav_distance_to_intruder<settings["tier1_distance_from_intruder"] and len(path)!=0):# return from attack
                dt_arrive=get_time_to_reach_point_in_streinght_line(self.position, path[0],settings)
                event_time=dt_arrive+game_state.t_curr
                new_event=Move_along(event_time,path[0],self)
                event_list.append_event(new_event)
            elif(0<uav_distance_to_intruder<settings["tier1_distance_from_intruder"] and len(path)==0 and len(temp_path)==0):
                dt_arrive = get_time_to_reach_point_in_streinght_line(self.position, temp_path[0], settings)
                event_time = dt_arrive + game_state.t_curr
                new_event = Move_along(event_time, temp_path[0], self)
                event_list.append_event(new_event)
            elif(0<uav_distance_to_intruder<settings["tier1_distance_from_intruder"] and self.status==UavStatus.WAIT):
                dt_arrive =settings["wiat_time"]
                event_time = dt_arrive + game_state.t_curr
                new_event = Move_along(event_time, self.position, self)
                self.plan_help()
                event_list.append_event(new_event)





    def get_d_t_arrive_poison(self,settings):
        d_ta_arrive=0
        if (settings["arrive_deterministic"]):
            d_ta_arrive = 1.0 / settings["arrive_deterministic"]
        else:
            d_ta_arrive = -1.0 / settings["arrive_deterministic"] * math.log(2, math.e)
        return d_ta_arrive

    def search_p_a_attack(self):
        pass

    def plan_move_attack(self):
        pass

    def search_p_a_back(self)->list:
        pass

    def select_temp_path_back(self)->list:
        pass

    def plan_help(self):
        pass
