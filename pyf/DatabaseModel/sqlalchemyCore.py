from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence
from functools import cache
import json
import os

#DATABASE_URI = "postgresql+psycopg2://root:heslo1234@uo_database:5432/data"

@cache
def GetDeclarativeBase():
    return declarative_base()



@cache
def GetUnitedSequence(name):
    seqName = name + "_id_seq"
    unitedSequence = Sequence(seqName)
    return unitedSequence

@cache
def initEngine(connectionstring):
    """Creates engine once and cache the result

    Parameters
    ----------
    connectionstring : str 
        full connection string to database
    
    Returns
    -------
    engine
        is object encapsulating and SQLAchemy engine used for database connection
    """
    engine = create_engine(connectionstring, pool_recycle=360) # see https://docs.sqlalchemy.org/en/14/core/pooling.html
    return engine

@cache
def initSession(connectionstring):
    """Creates callable Session once and cache the result

    Parameters
    ----------
    connectionstring : str 
        full connection string to database
    
    Returns
    -------
    Session
        is object (callable) used for instating a session
    """
    Session = sessionmaker(bind=initEngine(connectionstring))
    return Session

