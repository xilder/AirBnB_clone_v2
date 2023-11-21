#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), primary_key=True, nullable=False)
#    cities = relationship('City', backref='states',
#                         cascade='all, delete-orphan')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
