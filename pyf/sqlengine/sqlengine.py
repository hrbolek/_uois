from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from functools import cache

@cache
def getBaseModel():
    BaseModel = declarative_base()
    return BaseModel

@cache
def init(connectionstring=None, doDropAll=False, doCreateAll=False):

    assert not(connectionstring is None), 'Connection string missing'

    BaseModel = getBaseModel()

    #engine = create_engine('postgresql+psycopg2://user:password@hostname/database_name')
    #engine = create_engine('postgresql+psycopg2://postgres:example@postgres/jupyterII') 
    engine = create_engine(connectionstring) 
    Session = sessionmaker(bind=engine)
    
    if doDropAll:
        BaseModel.metadata.drop_all(engine)
    if doCreateAll:
        BaseModel.metadata.create_all(engine)

    return Session
    