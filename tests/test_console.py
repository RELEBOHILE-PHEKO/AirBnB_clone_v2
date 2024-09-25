#!/usr/bin/python3
"""this module contain unit tests"""

import unittest
from console import HBNBCommand
from io import StringIO
import sys

class TestConsoleCreate(unittest.TestCase):
    def setUp(self):
        """Set up method for tests"""
        self.console = HBNBCommand()
        self.old_stdout = sys.stdout
        sys.stdout = self.stdout = StringIO()

    def tearDown(self):
        """Tear down method for tests"""
        sys.stdout = self.old_stdout

    def test_create_state(self):
        """Test create State with parameters"""
        self.console.onecmd('create State name="California"')
        state_id = self.stdout.getvalue().strip()
        self.assertIn(state_id, storage.all())

    def test_create_place(self):
        """Test create Place with parameters"""
        self.console.onecmd('create Place city_id="0001" user_id="0001" name="My_little_house" number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300 latitude=37.773972 longitude=-122.431297')
        place_id = self.stdout.getvalue().strip()
        self.assertIn(place_id, storage.all())

if __name__ == '__main__':
    unittest.main()

