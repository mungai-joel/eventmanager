"""standard libraries and modules to be used by Activity class"""
from uuid import uuid4

class Activity(object):
    """activity class"""

    def __init__(self, activity):
        """activity object constructor"""
        self.activity = activity
        self.id = uuid4().hex

    def __repr__(self):
        return '{}'.format(self.activity)