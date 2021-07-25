import sys, os, inspect

from Event import Event
from MovableObject import MovableObject



import typing




class Event_list:
    def __init__(self):
        self.event_list:typing.List[Event]=[]
    def get_closest_event(self):
        minimum_event:Event=None
        if len(self.event_list)==0:
            return None
        else:
            minimum_event=self.event_list[0]
        for event in self.event_list:
            if(event.time_of_event<minimum_event.time_of_event):
                minimum_event=event

        return minimum_event

    def delete_event(self, event_to_delete):
        self.event_list.remove(event_to_delete)

    def append_event(self, new_event,owner:MovableObject,current_owner_status):
        self.event_list.append(new_event)
        owner.set_status(current_owner_status)
        owner.set_next_event(new_event)




