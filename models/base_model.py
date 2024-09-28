#!/usr/bin/python3
"""This module defines a BaseModel class."""

from datetime import datetime
import models
import uuid


class BaseModel:
    """Base model for all models in the project."""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance."""
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at attribute."""
        self.updated_at = datetime.now()
        models.storage.new(self)

    def to_dict(self):
        """Return a dictionary representation of the BaseModel."""
        dict_representation = self.__dict__.copy()
        dict_representation['created_at'] = self.created_at.isoformat()
        dict_representation['updated_at'] = self.updated_at.isoformat()
        dict_representation['__class__'] = self.__class__.__name__
        return dict_representation

    def __str__(self):
        """Return a string representation of the BaseModel."""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__
        )
