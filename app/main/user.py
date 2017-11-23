"""modules and standard libraries to be used by User class"""

from .events import Events

class User(object):
    """user class"""

    def __init__(self, username, email, password):
        """user object constructor"""
        self.username = username
        self.email = email
        self.password = password

        self.events = dict()

    def create_event(self, title, description, location, category):
        """create and add events to dictionary"""
        new_events = Events(title, description, location, category)
        self.events[new_events.id] = new_events
        return new_events.id

    def update_event(self, id, title, description, location, category):
        """update or edit the existing events"""
        for key in self.events.copy().keys():
            if id == key:
                self.events[key].title = title
                self.events[key].description = description
                self.events[key].location = location
                self.events[key].category = category


    def delete_event(self, id):
        """deleted the events with key that matches id passed"""
        for key  in self.events.copy().keys():
            if id == key:
                del self.events[key]
