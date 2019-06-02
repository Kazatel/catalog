from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime
from sqlalchemy import Column, Integer, DateTime
Base = declarative_base()


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
            'id': self.id,
        }

class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    genre_id = Column(Integer, ForeignKey('genre.id'))
    genre = relationship(Genre)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'price': self.price,
            'user_id': self.user_id,
            'genre_id': self.genre_id
        }

    @property
    def menu_item(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'price': self.price,
        }




#engine = create_engine('sqlite:///games.db')
engine = create_engine('postgresql://catalog:grader@localhost/catalog') 


Base.metadata.create_all(engine)
