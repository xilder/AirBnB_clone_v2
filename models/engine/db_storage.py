#!/usr/bin/python3
"""class DBStorage"""
import models
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """defines a class to manage the database of the hbnb clone"""

    __engine = None
    __session = None

    def __init__(self):
        """initialises the class"""

        user = getenv('HBNB_MYSQL_USER')
        passwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        db_url = "mysql+mysqldb://{}:{}@{}/{}".format(
                user, passwd, host, db)
        self.__engine = create_engine(db_url, pool_pre_ping=True)
        if getenv('HBNB_DEV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        returns all instances of the class if given else returns all
        instances
        """
        dictionary = {}
        classes = (State, City, User, Place, Review, Amenity)
        if cls is not None:
            classes = (cls)
        for cls_type in classes:
            for obj in self.__session.query(cls_type).all():
                key = f"{obj.__class__.__name__}.{obj.id}"
                dictionary[key] = obj
        return dictionary

    def reload(self):
        """creates all the table of the database"""

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def count(self, cls=None):
        total = 0
        if cls is None:
            for cls in self.all_classes.values():
                total += self.__session.query(cls).count()
        else:
            cls = self.all_classes.get(cls, None)
            total += self.__session.query(cls).count()
        return count

    def new(self, obj):
        """adds new obj to the database"""
        try:
            self.__session.add(obj)
        except Exception as ex:
            self.__session.rollback()
            raise ex

    def save(self):
        """commits changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """removes obj from database"""
        if obj is not None:
            self.__session.delete(obj)

    def close(self):
        """closes session"""
        self.__session.close()
