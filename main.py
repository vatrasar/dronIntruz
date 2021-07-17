import random

import matplotlib.pyplot as plt

from events.Event_list import Event_list
from GameState import GameState
from Settings import Settings
from Statistics import Statistics

from events.Move_along import plan_move_along
import time

from events.visualisation_event import plan_visualize


def main():
    settings=Settings()
    rand=random.Random(654)
    try:
        settings.get_properties()
    except Exception as exp:
        print(str(exp))
        return

    game_state=GameState(settings)
    statistics=Statistics()
    events_list=Event_list()
    #planning init event for uav
    for uav in game_state.uav_list:
        plan_move_along(game_state,settings,rand,events_list,uav)
    if settings.is_visualisation:
        plan_visualize(events_list,settings,game_state)

    while(True): #main simulation loop
        closet_event=events_list.get_closest_event()
        if(closet_event==None):
            print("błąd tablica zdarzeń jest pusta")
            break


        game_state.update_time(new_time=closet_event.time_of_event)
        statistics.update_stac(game_state,settings)
        print("time :"+str(game_state.t_curr))
        if(game_state.t_curr>settings.T): #end of loop
            statistics.save()
            break

        game_state.update_elements_positions(settings)
        game_state.check_collisions(settings,events_list)
        if(closet_event in events_list.event_list):
            closet_event.handle_event(events_list,game_state,settings,rand)

        game_state.check_collisions(settings,events_list)
        game_state.update_points_and_energy()

        if(game_state.intruder.health<=0):
            statistics.update_stac(game_state,settings)
            statistics.save()
            break






if __name__ == '__main__':
    main()
