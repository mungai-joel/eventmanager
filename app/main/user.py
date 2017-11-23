"""modules and standard libraries to be used by User class"""

from .bucketlist import BucketList

class User(object):
    """user class"""

    def __init__(self, username, email, password):
        """user object constructor"""
        self.username = username
        self.email = email
        self.password = password

        self.bucketlists = dict()

    def create_bucketlist(self, title, description):
        """create and add bucketlist to dictionary"""
        new_bucketlist = BucketList(title, description)
        self.bucketlists[new_bucketlist.id] = new_bucketlist
        return new_bucketlist.id

    def update_bucketlist(self, id, title, description):
        """update or edit the existing bucketlist"""
        for key in self.bucketlists.copy().keys():
            if id == key:
                self.bucketlists[key].title = title
                self.bucketlists[key].description = description


    def delete_bucketlist(self, id):
        """deleted the bucketlist with key that matches id passed"""
        for key  in self.bucketlists.copy().keys():
            if id == key:
                del self.bucketlists[key]
