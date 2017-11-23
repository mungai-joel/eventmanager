"""modules and standard libraries to be used by Bucketlist classs """

from uuid import uuid4
from .activity import Activity

class BucketList(object):
    """bucketlist class"""

    def __init__(self, title, description):
        """bucketlist object constructor"""
        self.title = title
        self.description = description
        self.id = uuid4().hex

        self.activities = dict()

    def add_activity(self, activity):
        """creates and add activity to dictionary"""
        new_activity = Activity(activity)
        self.activities[new_activity.id] = new_activity
        return new_activity.id

    def edit_activity(self, id, new_activity):
        """update or edit existing activity"""
        for key in self.activities.copy().keys():
            if id == key:
                self.activities[key].activity = new_activity


    def delete_activity(self, id):
        """"""
        for key in self.activities.copy().keys():
            if id == key:
                del self.activities[key]

    def __repr__(self):
        return '{}'.format(self.title)
