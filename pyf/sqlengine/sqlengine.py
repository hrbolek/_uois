from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import cache


@cache
def ensureDatabaseExists_old(connectionstring):
    import re

    parts = re.findall("([^/]+)//([^:]+):([^@]+)@([^:]+):([^/]+)/(.*)", connectionstring)
    names = ('driver', 'user', 'password', 'host', 'port', 'database')
    csItems = dict(zip(names, *parts))
    connectionStringWODatabase = f"{csItems['driver']}//{csItems['user']}:{csItems['password']}@{csItems['host']}:{csItems['port']}"
    
    engine = create_engine(connectionStringWODatabase)
    conn = engine.connect()
    try:
        #Preparing query to create a database
        sql = f"SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower({csItems['database']});"
        #Checking if a database exists
        conn.execute(sql)
        result = conn.fetchall()
        if len(result) == 0:
            print(f"Database {csItems['database']} does not exists, trying to create")

        sql = f"CREATE DATABASE IF NOT EXISTS {csItems['database']};"
        #Checking if a database exists
        conn.execute(sql)
    finally:
        conn.close()

def ensureDatabaseExists(connectionstring):
    from sqlalchemy_utils.functions import database_exists, create_database

    if database_exists(connectionstring):
        print('database exists')
    else:
        try:
            create_database(connectionstring)
            print('database newly created')
        except Exception as e:
            print('Missing privilege?')
            print(e)

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

