import unittest
import events
import requests
import json

class TestFlaskApiUsingRequests(unittest.TestCase):
    def test_todo_get(self):
        response = requests.get('http://localhost:5000/events/1')
        self.assertEqual(response.json(), {"category": "namecategory","id": 1,"name": "caaname","rsvp": "NO" })

if __name__ == "__main__":
    unittest.main()
