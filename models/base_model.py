#!/usr/bin/python3
"""
Module for BaseModel class.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import uuid
import datetime

Base = declarative_base()


class BaseModel(Base):
    """A base model that defines common attributes and methods for all models."""

    __tablename__ = 'base_model'  # Example table name

    id = Column(String(60), primary_key=True, default=str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance."""
        if not self.id:
            self.id = str(uuid.uuid4())
        super().__init__(*args, **kwargs)  # Call parent class constructor

    def save(self):
        """Save the current instance to the database."""
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert the object to a dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__class__.__table__.columns}

    def __str__(self):
        """Return a string representation of the instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

