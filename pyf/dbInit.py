import os
import json
from functools import cache

from sqlalchemy_utils.functions import database_exists, create_database

from DatabaseModel.sqlalchemyCore import initEngine, initSession, GetDeclarativeBase
from DatabaseModel.myDevTools import *
from DatabaseModel import randomData
from DatabaseModel.models import PersonModel, LessonModel, StudentModel, ProgramModel, GroupModel, SubjectModel, SemesterModel, GroupTypeModel, LessonTypeModel, RoomModel, BuildingModel, AreaModel
#from DatabaseModel import sqlalchemyCore #přístup do modulu přes tečku


@cache
def getConnectionString(configFileName='config.json'):
    """Reads config from file

    Parameters
    ----------
    configFileName: str
        name of the file to be readed
        the expected structure is:
        {
            "connectionstring": "driver://user:password@host/databasename"
            
        }
        driver should be "postgresql+psycopg2"


    Returns
    -------
    json: dict
        data structure defining parameters describing application and stored externally
    """

    result = { 'connectionstring': 'postgresql+psycopg2://postgres:postgres@postgres:5432/uois' }
    if os.path.isfile(configFileName):
        with open(configFileName, 'r') as config:
            result = json.load(config)
            connectionstring = result['connectionstring']

    else:
        user = os.environ["POSTGRES_USER"]
        password = os.environ["POSTGRES_PASSWORD"]
        connectionstring = "postgresql+psycopg2://" + user + ":" + password + "@postgres:5432/data"

    if not database_exists(connectionstring):  #=> False
        try:
            create_database(connectionstring)
            print('Database created')
        except Exception as e:
            print('Database does not exists and cannot be created')
            raise
    else:
        print('Database exists')

    print('connectionstring', connectionstring)

    return connectionstring

@cache
def GetSession():
    SQLBase = GetDeclarativeBase()

    connectionString = getConnectionString()
    engine = initEngine(connectionString)

    #SQLBase.metadata.drop_all(engine)
    #SQLBase.metadata.create_all(engine)

    Session = initSession(connectionString)
    return Session



def InitAndRandomize():
    SQLBase = GetDeclarativeBase()

    connectionString = getConnectionString()
    engine = initEngine(connectionString)

    SQLBase.metadata.drop_all(engine)
    SQLBase.metadata.create_all(engine)

    Session = initSession(connectionString)

    mySession = Session()

    print('preloading data')
    randomData.preloadData(mySession)
    print('preloading data done')
    print('preloading buildings')
    randomData.buildings(mySession)
    print('preloading buildings done')
    print('preloading lessons')
    randomData.lekce(mySession)
    print('preloading lessons done')

    mySession.close()

    return Session


