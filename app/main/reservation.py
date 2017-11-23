"""standard libraries and modules to be used by Reservation class"""
from uuid import uuid4

class Reservation(object):
    """reservation class"""

    def __init__(self, name, phone):
        """reservation object constructor"""
        self.name = name
        self.phone = phone
        self.id = uuid4().hex

    def __repr__(self):
        return '{}'.format(self.name)