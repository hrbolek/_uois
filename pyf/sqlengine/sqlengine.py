from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import cache

@cache
def initEngine(connectionstring):
    engine = create_engine(connectionstring)
    return engine

@cache
def initSession(connectionstring):
    Session = sessionmaker(bind=initEngine(connectionstring))
    return Session

