from functools import cache
import json

from fastapi import FastAPI, Request

from models.Initialization import initModels
from models.BaseModel import getBaseModel

from sqlengine.sqlengine import initEngine, initSession

import fastapiapp
import graphqlapp

@cache
def getConfig(configFileName='config.json'):
    """Reads config from file

    Parameters
    ----------
    configFileName: str
        name of the file to be readed

    Returns
    -------
    json: dict
        data structure defining parameters describing application and stored externally
    """
    with open(configFileName, 'r') as config:
        return json.load(config)

def initDb(connectionstring, doDropAll=False, doCreateAll=False):
    """Initialize database connection

    Parameters
    ----------
    connectionstring: str
        full connection string defining the connection to database
    doDropAll: boolean=False
        if True, database is dropped
    doCreateAll: boolean=False
        if True, database is redefined, usually used with doDropAll=True

    Returns
    -------
    Session: callable
        used for instatiating a session

    """

    print('initDb started')
    BaseModel = getBaseModel()
    print(f'Session with doDropAll={doDropAll} & doCreateAll={doCreateAll}')
    assert not(connectionstring is None), 'Connection string missing'

    initModels()
    engine = initEngine(connectionstring) 
    Session = initSession(connectionstring)
    
    if doDropAll:
        BaseModel.metadata.drop_all(engine)
    if doCreateAll:
        BaseModel.metadata.create_all(engine)

    print('initDb finished')
    return Session

def preloadData(Session):
    session = Session()
    try:
        session.query(GroupTypeModel)
        pass
    finally:
        session.close()
    pass

def buildApp():
    """builds a FastAPI application object with binded Swagger and GraphQL endpoints

    Returns
    -------
    app
        FastAPI instance with binded endpoints
    """
    print('Load config')
    connectionstring = getConfig()['connectionstring']

    print('Init Session')
    Session = initSession(connectionstring)
    def prepareSession():#Session=Session): # default parameters are not allowed here
        """generator for creating db session encapsulated with try/except block and followed session.commit() / session.rollback()

        Returns
        -------
        generator
            contains just one item which is instance of Session (SQLAlchemy)
        """
        session = Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()    

    #app = FastAPI(root_path="/apif")
    #initDb(connectionstring, doDropAll=True, doCreateAll=True)
    initDb(connectionstring)

    app = FastAPI()
    print('init Db')
    fastapiapp.attachFastApi(app, prepareSession)
    graphqlapp.attachGraphQL(app, prepareSession)
    return app

app = buildApp()
