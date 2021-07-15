import typing

from Enums import UavStatus
from GameObjects import Hand, Uav
from GameState import GameState
from tools.geometric_tools import get_2d_distance
from matplotlib import pyplot as plt
import os

class Statistics():

    def __init__(self):
        self.game_states_list:typing.List[GameState]=[]
    def update_stac(self,game_state,settings):
        to_svae=self.clone_game_state(game_state, settings)
        self.game_states_list.append(to_svae)

    def clone_game_state(self,game_state:GameState,settings):
        stat_game_state=GameState(settings)

        #hands
        stat_game_state.hands_list=[]
        for hand in game_state.hands_list:
            hand_copy=Hand(hand.position.x,hand.position.y,hand.status,hand.velocity,hand.side,settings)
            stat_game_state.hands_list.append(hand_copy)


        #drones
        stat_game_state.uav_list=[]
        for uav in game_state.uav_list:
            uav_copy=Uav(uav.position.x,uav.position.y,uav.status,uav.points,uav.velocity)
            stat_game_state.uav_list.append(uav_copy)

        stat_game_state.t_curr=game_state.t_curr

        return stat_game_state




    def save(self):
        save_directory = "./charts"
        import os
        if not os.path.exists(save_directory):
            os.mkdir(save_directory)

        #distance between uav
        x=[]
        y=[]
        for state in self.game_states_list:
            if len(state.uav_list)==2 and state.uav_list[0].status!=UavStatus.TIER_2 and state.uav_list[1].status!=UavStatus.TIER_2 :
                distance=get_2d_distance(state.uav_list[0].position,state.uav_list[1].position)
                x.append(state.t_curr)
                y.append(distance)
        plt.plot(x,y)
        plt.savefig(save_directory+"/"+"distance_between_uav.svg")
        import os





