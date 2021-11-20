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
    with open(configFileName, 'r') as config:
        return json.load(config)

def initDb(connectionstring, doDropAll=False, doCreateAll=False):
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

def buildApp():
    print('Load config')
    connectionstring=getConfig()['connectionstring']

    print('Init Session')
    Session = initSession(connectionstring)
    async def prepareSession():#Session=Session): # default parameters are not allowed here
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
    initDb(connectionstring, doDropAll=True, doCreateAll=True)

    app = FastAPI()
    print('init Db')
    fastapiapp.attachFastApi(app, prepareSession)
    graphqlapp.attachGraphQL(app, prepareSession)
    return app

app = buildApp()
