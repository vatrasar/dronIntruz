from random import random, Random

import numpy as np
from tensorforce import Environment

from Enums import UavStatus
from Event_list import Event_list
from GameState import GameState
from Move_along import plan_move_along

from Settings import Settings

from tools.search_tools import build_discrete_map, build_simple_discrete_map


class MyEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self.settings = Settings()

        try:
            self.settings.get_properties()
        except Exception as exp:
            print(str(exp))
            return

        self.counter=0
        self.my_random = Random()
        self.game_map = np.zeros((self.settings.simple_dimension,self.settings.simple_dimension),dtype=np.int)
        self.observation_size = self.settings.simple_dimension*self.settings.simple_dimension*4
        self.action_size = 2
        self.max_timestep=100
        self.time_steps=70
        self.is_attack_possible=False
        self.real_points=0


        # self.reset_to_start()



    def max_episode_timesteps(self):
        return self.max_timestep

    def close(self):
        super().close()

    def reset(self, num_parallel=None):
        self.reset_to_start()
        for uav in self.game_state.uav_list:
            plan_move_along(self.game_state, self.settings, self.my_random, self.events_list, uav)
        uav=self.perform_untli_decision()
        state=build_simple_discrete_map(self.game_state,self.settings,uav)

        return state.map_memmory
    def reset_to_start(self):
        self.events_list = Event_list()
        self.game_state=GameState(self.settings)
        self.real_points = 0
        self.attack_in_current = 0
        self.hits=0



    def states(self):
        return dict(type='int', shape=(self.settings.simple_dimension,self.settings.simple_dimension),num_values=4)

    def actions(self):
        return dict(type='int', num_values=2)


    def perform_untli_decision(self):
        is_decision=False
        game_map_resutl=None
        uav_performing_action=None
        # planning init event for uav

        while not(is_decision):
            closet_event = self.events_list.get_closest_event()
            if (closet_event == None):
                print("błąd tablica zdarzeń jest pusta")
                return None

            self.game_state.update_time(new_time=closet_event.time_of_event)

            #print("time :" + str(self.game_state.t_curr))
            if (self.game_state.t_curr > self.settings.T):  # end of loop
                return None

            self.game_state.update_elements_positions(self.settings)
            self.game_state.check_collisions(self.settings, self.events_list)


            for uav in self.game_state.uav_list:
                if closet_event.event_owner==uav and closet_event.next_status==UavStatus.TIER_1:
                    game_map_resutl = build_simple_discrete_map(self.game_state, self.settings, uav)
                    is_decision=True
                    uav_performing_action=uav
                    break


            if (closet_event in self.events_list.event_list):
                closet_event.handle_event(self.events_list, self.game_state, self.settings, self.my_random)

            self.game_state.check_collisions(self.settings, self.events_list)
            self.game_state.update_points_and_energy()
            if is_decision:
                if uav_performing_action.status==UavStatus.ON_ATTACK:
                    self.is_attack_possible=True
                else:
                    self.is_attack_possible = False



            # if (self.game_state.intruder.health <= 0):
            #     statistics.update_stac(game_state, settings)
            #     statistics.save()
            #     break
        return game_map_resutl

    def execute(self, actions):

        self.time_steps=self.time_steps+1
        reward=0
        done=False


        # reward for previous state:

        if self.is_attack_possible:
            self.attack_in_current=self.attack_in_current+1
            if actions==1:
                reward=10
                self.real_points=self.real_points+1
                self.hits=self.hits+1
            else:
                reward=-1


        else:
            if actions==0:
                self.hits = self.hits + 1
                reward=1
            else:
                reward=-1


        uav=self.perform_untli_decision()
        if uav==None:
            done=True
            if self.attack_in_current!=0:
                print("atttakc %.2f"%(self.real_points/self.attack_in_current))
                print("all %.2f"%(self.hits/self.time_steps))


        game_map=build_simple_discrete_map(self.game_state,self.settings,uav)






        return game_map.map_memmory, done, reward


