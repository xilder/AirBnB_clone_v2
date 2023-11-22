#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Float, Integer, String, Column, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv


metadata = Base.metadata
place_amenity = Table('place_amenity',
                      metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False
                     ) if getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False
                     ) if getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    name = Column(String(128), nullable=False
                  ) if getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    description = Column(String(1024)
                         ) if getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    number_rooms = Column(Integer, nullable=False, default=0
                          ) if getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    number_bathrooms = Column(Integer, nullable=False, default=0
                              ) if getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    max_guest = Column(Integer, nullable=False, default=0
                       ) if getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    price_by_night = Column(Integer, nullable=False, default=0
                            ) if getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    latitude = Column(Float) if getenv('HBNB_TYPE_STORAGE') == 'db' else 0.0
    longitude = Column(Float) if getenv('HBNB_TYPE_STORAGE') == 'db' else 0.0
    reviews = relationship('Review', backref='places',
                           cascade='all, delete-orphan')
    amenity_ids = []
    amenities = relationship('Amenity', secondary=place_amenity,
                             viewonly=False
                             ) if getenv('HBNB_TYPE_STORAGE') == 'db' else None

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """retrieves reviews that are related to this instance by id"""
            from models import storage
            reviews = []
            for review in storage.all(Review).values():
                if review.place_id == self.id:
                    reviews.append(review)

            return reviews

        @property
        def amenities(self):
            """retrieves amenities that are related to this instance by id"""
            from models import storage
            amenities = []
            for amenity in storage.all(Amenity).values():
                if amenity.id in self.amenity_id:
                    amenities.append(amenity)
            return amenities
        @amenities.setter
        def amenities(self, value):
            """adds an amenity"""
            if type(value) is Amenity and value.id not in self.amenity_ids:
                self.amenity_ids.append(value.id)
