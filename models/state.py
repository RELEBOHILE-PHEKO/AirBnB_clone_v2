#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel

class State(BaseModel, Base):
    """ The state class, contains state ID and name """
    __tablename__ = 'states'
    
    name = Column(String(128), nullable=False)
    
    # Relationship to the City class
    cities = relationship("City", back_populates="state", cascade="all, delete")
