import sys, os, inspect

from GameObjects import MovableObject

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from random import Random

from events.Event_list import Event_list
from GameState import GameState


class Event():
    def __init__(self, time_of_event, target_position, event_owner, next_status, last_postion_update_time):
        self.time_of_event=time_of_event
        self.target_position=target_position
        self.event_owner:MovableObject=event_owner
        self.next_status=next_status
        self.last_postion_update_time=last_postion_update_time

    def handle_event(self,event_list:Event_list,game_state:GameState,settings,rand:Random):
        event_list.delete_event(self)
        self.event_owner.set_status(self.next_status)

