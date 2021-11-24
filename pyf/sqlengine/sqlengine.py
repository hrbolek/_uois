from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import cache

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

