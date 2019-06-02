from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Genre, Base, Game, User

engine = create_engine('sqlite:///games.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create genres
Genre_list = ["ALL", "Action", "Adventure", "Role-playing", "Simulation", "Strategy", "Sports",]
for g in Genre_list:
    gr = Genre(name=g)
    session.add(gr)
    session.commit()

print "added menu items!"


# Create dummy user1
User1 = User(name="John Doe", email="john.doe@google.com",
             picture='')
session.add(User1)
session.commit()


# Games for user1

game1 = Game(user_id=User1.id, name="Skyrim", description="Action RPG , do so if you like swrod and magic",
                     price="$7.50", genre_id=4)

session.add(game1)
session.commit()


game2= Game(user_id=User1.id, name="Tomb Raider 1", description="Old good Lara, who wants to go back to good memories",
                     price="$7.50", genre_id=2)

session.add(game2)
session.commit()


# Create dummy user2
User2 = User(name="Tom Doe", email="tom.doe@google.com",
             picture='')
session.add(User2)
session.commit()


game3 = Game(user_id=User2.id, name="Red alert 2", description="Best strategy game ever!",
                     price="$7.50", genre_id=6)

session.add(game3)
session.commit()


game4= Game(user_id=User2.id, name="Tomb Raider 2", description="Old good Lara, who wants to go back to good memories",
                     price="$7.80", genre_id=2)

session.add(game4)
session.commit()
