import random

from Events.Event_list import Event_list
from GameState import GameState
from Settings import get_properties
from Statistics import Statistics
from Visualization import plan_visualize


def main():
    settings_map=None
    rand=random.Random()
    try:
        settings_map=get_properties()
    except Exception as exp:
        print(str(exp))
        return

    game_state=GameState(settings_map)
    statistics=Statistics()
    events_list=Event_list()
    #planning init event for uav
    for uav in game_state.uav_list:
        uav.plan_move_along(game_state)
    if settings_map["visualization"]:
        plan_visualize(events_list)

    while(True): #main simulation loop
        closet_event=events_list.get_closest_event()
        if(closet_event==None):
            print("błąd tablica zdarzeń jest pusta")
            break


        game_state.update_time(new_time=closet_event.time_of_event)
        statistics.update_stac()
        if(game_state.t_curr>settings_map["T"]): #end of loop
            statistics.save()
            break

        game_state.update_elements_positions()

        closet_event.handle_event()
        is_collision=game_state.check_collisions()
        game_state.update_points_and_energy()

        if(is_collision or game_state.intruder.health<=0):
            statistics.update_stac()
            break






if __name__ == '__main__':
    main()
