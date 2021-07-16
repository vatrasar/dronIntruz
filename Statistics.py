import shutil
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
        self.settings=settings
        self.game_states_list.append(to_svae)

    def clone_game_state(self,game_state:GameState,settings):
        stat_game_state=GameState(settings)

        #hands
        stat_game_state.hands_list=[]
        for hand in game_state.hands_list:
            hand_copy=Hand(hand.position.x,hand.position.y,hand.status,hand.velocity,hand.side,settings)
            hand_copy.position.x=hand.position.x
            hand_copy.position.y=hand.position.y
            stat_game_state.hands_list.append(hand_copy)


        #drones
        stat_game_state.uav_list=[]
        for uav in game_state.uav_list:
            uav_copy=Uav(uav.position.x,uav.position.y,uav.status,uav.points,uav.velocity)
            stat_game_state.uav_list.append(uav_copy)

        stat_game_state.t_curr=game_state.t_curr

        return stat_game_state




    def save(self):
        save_directory = self.create_folder()

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
        plt.clf()
        import os



        #distance to hands
        x = []
        y = []
        xr1, yr1, xl1, yl1 = [], [], [], []
        xr2, yr2, xl2, yl2 = [], [], [], []
        if self.settings.hands_number > 0:
            for state in self.game_states_list:



                if len(state.uav_list)>0 and state.uav_list[0].status!=UavStatus.TIER_2:#hand1
                    if len(state.uav_list)>0 and state.uav_list[0].status!=UavStatus.TIER_2:#uav1
                        distance1=get_2d_distance(state.hands_list[0].position,state.uav_list[0].position)
                        xr1.append(state.t_curr)
                        yr1.append(distance1)

                    if len(state.uav_list)>1 and state.uav_list[1].status!=UavStatus.TIER_2:
                        distance1 = get_2d_distance(state.hands_list[0].position, state.uav_list[1].position)

                        xr2.append(state.t_curr)
                        yr2.append(distance1)

                if len(state.uav_list)>0 and len(state.hands_list)>1 and state.uav_list[0].status!=UavStatus.TIER_2:#hand2
                    if len(state.uav_list) > 0 and state.uav_list[0].status != UavStatus.TIER_2:  # uav1
                        distance1 = get_2d_distance(state.hands_list[1].position, state.uav_list[0].position)
                        xl1.append(state.t_curr)
                        yl1.append(distance1)

                    if len(state.uav_list) > 1 and state.uav_list[1].status != UavStatus.TIER_2:
                        distance1 = get_2d_distance(state.hands_list[1].position, state.uav_list[1].position)

                        xl2.append(state.t_curr)
                        yl2.append(distance1)
            #plot
            if len(xl1)>0:
                plt.plot(xl1, yl1)
                plt.plot(xl2, yl2)
                plt.legend(["uav1","uav2"])
                plt.savefig(save_directory + "/" + "distanceToL.svg")
                plt.clf()

            if len(xr1) > 0:
                plt.plot(xr1, yr1)
                plt.plot(xr2, yr2)
                plt.legend(["uav1","uav2"])
                plt.savefig(save_directory + "/" + "distanceToR.svg")
                plt.clf()


        #points of uavs
        x1,x2=[],[]
        y1,y2=[],[]
        x_sum,y_sum=[],[]
        for state in self.game_states_list:
            if len(state.uav_list)>0:
                x1.append(state.t_curr)
                y1.append(state.uav_list[0].points)

            if len(state.uav_list)>1:
                x2.append(state.t_curr)
                y2.append(state.uav_list[1].points)
                x_sum.append(state.t_curr)
                y_sum.append(state.uav_list[1].points+state.uav_list[0].points)
        if len(x1) > 0:
            plt.plot(x1, y1)
            plt.plot(x2, y2)

            plt.legend(["uav1", "uav2"])
            plt.savefig(save_directory + "/" + "points.svg")
            plt.clf()

            plt.plot(x_sum, y_sum)
            plt.savefig(save_directory + "/" + "pointsSum.svg")
            plt.clf()

        # plt.plot(x,y)
        # plt.savefig(save_directory+"/"+"distance_between_uav.svg")

    def create_folder(self):
        save_directory = "./charts"
        import os
        if not os.path.exists(save_directory):
            os.mkdir(save_directory)
        for filename in os.listdir(save_directory):
            file_path = os.path.join(save_directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        return save_directory





