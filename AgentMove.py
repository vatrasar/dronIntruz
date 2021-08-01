import random

from Enums import UavStatus
from Event import Event
from Event_list import Event_list
from Move_r import plan_move_r
from Point import Point
from Settings import Settings
from UAV import Uav
from tools.geometric_tools import get_2d_distance, get_random_position
from tools.velocity_tools import get_time_to_reach_point_in_streinght_line, get_d_t_arrive_poison


class AgentMove(Event):

    def handle_event(self, event_list:Event_list, game_state, settings:Settings, rand: random.Random):
        super().handle_event(event_list, game_state, settings, rand)
        self.event_owner.position=self.target_position
        if self.event_owner.action==-1: #environment have3 to wait for decision

            #planning waitning event

            event_time = game_state.t_curr
            if get_2d_distance(self.event_owner.position,game_state.intruder.position)<settings.tier1_distance_from_intruder:
                next_status = UavStatus.ON_ATTACK
            else:
                next_status = UavStatus.TIER_1

            new_event = AgentMove(event_time, self.event_owner.position,self.event_owner, next_status, game_state.t_curr)

            event_list.append_event(new_event, self.event_owner, next_status)
        else:#there is new action, peromorme it
            for hand in game_state.hands_list:
                plan_move_r(event_list, hand, game_state, settings)
            new_position = Point(self.event_owner.position.x, self.event_owner.position.y)
            if self.event_owner.action==0:
                new_position.x=new_position.x+settings.map_resolution
            elif self.event_owner.action==1:
                new_position.x = new_position.x - settings.map_resolution
            elif self.event_owner.action == 2:
                new_position.x = new_position.y + settings.map_resolution
            elif self.event_owner.action == 3:
                new_position.x = new_position.y - settings.map_resolution

            self.event_owner.action=-1
            dtime = get_time_to_reach_point_in_streinght_line(self.event_owner.position, new_position,
                                                              settings.v_of_uav)
            if get_2d_distance(new_position,game_state.intruder.position)>settings.map_size*0.9-settings.uav_size:
                new_position=self.event_owner.position
                dtime=settings.wiat_time




            event_time = game_state.t_curr + dtime
            if get_2d_distance(new_position, game_state.intruder.position) < settings.tier1_distance_from_intruder:
                next_status = UavStatus.ON_ATTACK
            else:
                next_status = UavStatus.TIER_1

            new_event = AgentMove(event_time, new_position, self.event_owner, next_status,
                                  game_state.t_curr)

            event_list.append_event(new_event, self.event_owner, self.event_owner.status)


def plan_agent_init(game_state,settings,rand,event_list:Event_list,uav:Uav):
    dt_arrive = get_d_t_arrive_poison(settings)
    is_new_position_correct = False
    new_position=None
    while (not (is_new_position_correct)):
        new_position = get_random_position(rand, game_state, settings)
        is_new_position_correct = game_state.is_correct_drone(new_position, dt_arrive + game_state.t_curr, uav,
                                                              settings)

    event_time = game_state.t_curr + dt_arrive
    new_event = AgentMove(event_time, new_position, uav, UavStatus.TIER_1, game_state.t_curr)
    event_list.append_event(new_event, uav, UavStatus.TIER_2)