class Event():
    def __init__(self,time_of_event,target_position,event_owner):
        self.time_of_event=time_of_event
        self.target_position=target_position
        self.event_owner=event_owner

    def handle_event(self):
        pass

