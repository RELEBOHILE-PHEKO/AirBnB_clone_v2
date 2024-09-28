#!/usr/bin/python3
"""
Module for testing the DBStorage class
"""
import unittest
import os
from models.engine.db_storage import DBStorage
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestDBStorage(unittest.TestCase):
    """Test cases for the DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment"""
        cls.db_fd, cls.db_path = tempfile.mkstemp()
        cls.db_storage = DBStorage()
        cls.db_storage.reload()

    @classmethod
    def tearDownClass(cls):
        """Clean up the test environment"""
        os.close(cls.db_fd)
        os.unlink(cls.db_path)

    def setUp(self):
        """Set up for each test"""
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        """Clean up after each test"""
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_all_no_class(self):
        """Test all() method without class"""
        result = self.db_storage.all()
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)

    def test_all_with_class(self):
        """Test all() method with a specific class"""
        state = State(name="California")
        self.session.add(state)
        self.session.commit()
        result = self.db_storage.all(State)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 1)
        self.assertIn(f"State.{state.id}", result)

    def test_new(self):
        """Test new() method"""
        user = User(email="test@test.com", password="password")
        self.db_storage.new(user)
        self.db_storage.save()
        result = self.db_storage.all(User)
        self.assertIn(f"User.{user.id}", result)

    def test_save(self):
        """Test save() method"""
        city = City(name="San Francisco", state_id="CA")
        self.db_storage.new(city)
        self.db_storage.save()
        result = self.db_storage.all(City)
        self.assertIn(f"City.{city.id}", result)

    def test_delete(self):
        """Test delete() method"""
        amenity = Amenity(name="WiFi")
        self.db_storage.new(amenity)
        self.db_storage.save()
        self.db_storage.delete(amenity)
        self.db_storage.save()
        result = self.db_storage.all(Amenity)
        self.assertNotIn(f"Amenity.{amenity.id}", result)

    def test_reload(self):
        """Test reload() method"""
        place = Place(name="Cozy Cabin", city_id="SF", user_id="1")
        self.db_storage.new(place)
        self.db_storage.save()
        self.db_storage.reload()
        result = self.db_storage.all(Place)
        self.assertIn(f"Place.{place.id}", result)

    def test_all_with_id(self):
        """Test all() method with a specific id"""
        review = Review(text="Great place!", place_id="1", user_id="1")
        self.db_storage.new(review)
        self.db_storage.save()
        result = self.db_storage.all(Review, review.id)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 1)
        self.assertIn(f"Review.{review.id}", result)


if __name__ == "__main__":
    unittest.main()
