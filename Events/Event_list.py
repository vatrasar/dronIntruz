import typing

from Events.Event import Event


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




