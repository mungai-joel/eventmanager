"""Package and modules to be imported"""

from unittest import TestCase
from app.main.events import Events
from app.main.reservation import Reservation
from app.main.user import User

class TestEvents(TestCase):
    """Main Events Test class"""
    def setUp(self):
        """Sets up test fixture"""
        self.new_event = Events(
                                        'Andela Bootcamp',
                                         'This is an event for upcoming and new programmers',
                                         'Kindaruma Road',
                                         'Educational'
                                         )
    def test_add_resevation(self):
        """Test whether an reservation has been saved"""
        before_add = len(self.new_event.reservation)
        self.new_event.add_reservation('Joel Mungai', '0721777777')
        after_add = len(self.new_event.reservation)
        self.assertEqual(after_add - before_add, 1)
        
            
class TestUser(TestCase):
    """Sets up fixture for tests"""
    def setUp(self):
        """Set up test fixture"""
        self.new_user = User('mary', 'mary@mail', 'i1234')

    def test_create_events(self):
        """Test whether event has been  created"""
        result = len(self.new_user.events)
        self.new_user.create_event('this is new',
                                        'andela tests',
                                        'Kindaruma Road',
                                        'Educational'
                                        )
        after_add = len(self.new_user.bucketlists)
        self.assertEqual(after_add - result, 1)

    def test_update_events(self):
        """Test whether events has been edited"""
        id = self.new_user.create_event('this is another',
                                             'another test',
                                             'ngong road',
                                             'uncategorized'
                                             )
        self.new_user.update_event(
                                        id, 'this work',
                                         'good test',
                                         'kindaruma road',
                                         'educational'
                                         )
        self.assertEqual(self.new_user.events[id].title,
                         'this work'
                         )
        self.assertEqual(self.new_user.events[id].description,
                         'yes it does')

        self.assertEqual(self.new_user.events[id].location,
                         'kindaruma road')

        self.assertEqual(self.new_user.events[id].description,
                         'educational')
                         
    def test_delete_events(self):
        """Test whether  events has been deleted"""
        id = self.new_user.create_event('Jameson Party', 'ty dolla sign and nasty c', 'ngong race course', 'entertainment')
        result = len(self.new_user.events)
        self.new_user.delete_event(id)
        after_delete = len(self.new_user.events)
        self.assertTrue(result, after_delete)
