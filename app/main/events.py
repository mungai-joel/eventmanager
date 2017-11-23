"""modules and standard libraries to be used by Events classs """

from uuid import uuid4
from .reservation import Reservation

class Events(object):
    """Events class"""

    def __init__(self, title, description, location, category):
        """events object constructor"""
        self.title = title
        self.description = description
        self.location = location
        self.category = category
        self.id = uuid4().hex

        self.reservation = dict()
    
    """ Add a reservation to an event"""

    def add_reservation(self, name, phone):
        """creates and add activity to dictionary"""
        new_reservation = Reservation(name, phone)
        self.reservation[new_reservation.id] = new_reservation
        return new_reservation.id


    def __repr__(self):
        return '{}'.format(self.title)