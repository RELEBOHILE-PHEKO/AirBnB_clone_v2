#!/usr/bin/python3
"""
Module for DBStorage class
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import os

class DBStorage:
    """The class for database storage."""
    __engine = None
    __session = None
    __objects = {}  # Temporary storage for testing purposes

    def __init__(self):
        """Initialize a new DBStorage instance."""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_pre_ping=True
        )
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None, id=None):
        """
        Query the current database session.

        Args:
            cls (class, optional): The class to query.
            id (str, optional): The id of the object to retrieve.

        Returns:
            dict: A dictionary of objects.
        """
        classes = [User, State, City, Amenity, Place, Review]
        if cls:
            classes = [cls]

        objects = []
        for c in classes:
            objects.extend(self.__session.query(c).all())

        if id:
            objects = [obj for obj in objects if obj.id == id]

        return {f"{type(obj).__name__}.{obj.id}": obj for obj in objects}

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)
        self.__objects[f"{type(obj).__name__}.{obj.id}"] = obj  # Track objects

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()
        self.__objects.clear()  # Clear tracked objects after saving

    def delete(self, obj=None):
        """Delete from the current database session."""
        if obj:
            self.__session.delete(obj)
            if f"{type(obj).__name__}.{obj.id}" in self.__objects:
                del self.__objects[f"{type(obj).__name__}.{obj.id}"]  # Remove from tracked objects

    def reload(self):
        """Create all tables in the database and create a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the session."""
        self.__session.close()
