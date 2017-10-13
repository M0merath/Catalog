import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
#from sqlalchemy import types

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
    #Returns data in JSON-serialized format
        return {
            'name' : self.name,
            'id' : self.id,
        }

class Recipe(Base):
    __tablename__ = 'recipe'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    summary = Column(String(150))
    ingredients = Column(String(200))
    directions = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    category = relationship(Category)

    @property
    def serialize(self):
    #Returns data in JSON-serialized format
        return {
            'name' : self.name,
            'summary' : self.summary,
            'ingredients' : self.ingredients,
            'directions' : self.directions,
            'id' : self.id,
            #'category' : self.category,
            'category_id' : self.category_id,
            'user_id' : self.user_id
        }

engine = create_engine(
'sqlite:///gastronaut.db')
Base.metadata.create_all(engine)
