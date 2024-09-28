#!/usr/bin/python3
"""This is the storage engine using SQLAlchemy. It manages the database connection, sessions, and CRUD operations."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
import os


class DBStorage:
    """Interacts with the MySQL database."""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance."""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects of a certain class or all classes."""
        if cls:
            objs = self.__session.query(cls).all()
        else:
            objs = []
            for class_type in [State, City]:  # Add more classes as needed
                objs.extend(self.__session.query(class_type).all())
        return {f"{type(obj).__name__}.{obj.id}": obj for obj in objs}

    def new(self, obj):
        """Add the object to the current session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the database."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the database."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and start a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)
