import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from random import Random

from events.Event_list import Event_list
from GameState import GameState


class Event():
    def __init__(self,time_of_event,target_position,event_owner):
        self.time_of_event=time_of_event
        self.target_position=target_position
        self.event_owner=event_owner

    def handle_event(self,event_list:Event_list,game_state:GameState,settings,rand:Random):
        pass

