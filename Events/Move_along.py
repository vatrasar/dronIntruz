import random

from Enum import StatusEnum
from Events.Event import Event
from Events.Event_list import Event_list
from GameState import GameState
from Settings import Settings
from gameObjects.UAV import Uav
from Enum.StatusEnum import UavStatus

class Move_along(Event):



    def handle_event(self, event_list:Event_list, game_state:GameState, settings:Settings, rand: random.Random):
        event_list.delete_event(self)
        uav:Uav=self.event_owner
        uav.position=self.target_position
        if(uav.status==UavStatus.TIER_2):
            uav.plan_move_along(game_state,settings,rand,event_list)
            return
        else:
            #plan intruder reaction
            for hand in game_state.hands_list:
                hand.move_hand()

            path=uav.search_p_a_attack()
            if(len(path)!=0):
                if(settings.mode=="RW-RA"):
                    x=rand.random()
                    if(x<settings.prob_of_attack):
                        uav.plan_move_attack()
                    else:
                        x=rand.random()
                        if(x<settings.prob_of_return_to_T2):
                            uav.set_status(UavStatus.TIER_2)
                            uav.plan_move_along(game_state,settings,rand,event_list)#return 2t->1T

                        else:#move on tier1
                            uav.plan_move_along(game_state,settings,rand,event_list)
                    return

            else:#path not found

                if(settings.mode=="RW-RA"):
                    if(uav.status==UavStatus.TIER_1):
                        x = rand.random()
                        if (x < settings.prob_of_return_to_T2):
                            uav.set_status(UavStatus.TIER_2)
                            uav.plan_move_along(game_state,settings,rand,event_list)  # return 2t->1T
                        else:#move on tier 1
                            uav.plan_move_along(game_state,settings,rand,event_list)
                    else:
                        uav.plan_move_along(game_state,settings,rand,event_list)







