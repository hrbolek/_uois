from functools import cache
import json
import os

from fastapi import FastAPI, Request

#from models import BaseModel

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
    return result

from sqlalchemy_utils.functions import database_exists, create_database

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

    assert not(connectionstring is None), 'Connection string missing'
    print('initDb started')
    
    if not database_exists(connectionstring):  #=> False
        try:
            create_database(connectionstring)
            doCreateAll = True
            print('Database created')
        except Exception as e:
            print('Database does not exists and cannot be created')
            raise

    print(f'Session with doDropAll={doDropAll} & doCreateAll={doCreateAll}')
    #####################
    #initModels()
    #####################

    from models.BaseModel import BaseModel
    
    from models.GroupRelated.GroupModel import GroupModel
    from models.GroupRelated.UserModel import UserModel
    from models.GroupRelated.UserGroupModel import UserGroupModel
    from models.GroupRelated.RoleModel import RoleModel
    from models.GroupRelated.RoleTypeModel import RoleTypeModel
    from models.GroupRelated.GroupTypeModel import GroupTypeModel
    
    from models.EventsRelated.EventModel import EventModel
    from models.EventsRelated.EventUserModel import EventUserModel
    from models.EventsRelated.EventGroupModel import EventGroupModel
    from models.EventsRelated.EventRoomModel import EventRoomModel

    from models.AcreditationRelated.AcrediationUserRole import AcreaditationUserRoleTypeModel, ProgramUserRoleModel, SubjectUserRoleModel, StudyPlanUserRoleModel
    from models.AcreditationRelated.ProgramModel import ProgramModel
    from models.AcreditationRelated.SubjectModel import SubjectModel
    from models.AcreditationRelated.SubjectSemesterModel import SubjectSemesterModel
    from models.AcreditationRelated.SubjectTopic import SubjectTopicModel
    from models.AcreditationRelated.StudyPlan import StudyPlanModel
    from models.AcreditationRelated.StudyPlanItem import StudyPlanItemModel

    from models.FacilitiesRelated.ArealModel import ArealModel
    from models.FacilitiesRelated.BuildingModel import BuildingModel
    from models.FacilitiesRelated.RoomModel import RoomModel

    #from models import GroupModel, UserModel, UserGroupModel, RoleModel, RoleTypeModel
    #from models import EventModel, EventUserModel, EventGroupModel
    #from models import ArealModel, BuildingModel, RoomModel
    #from models import ProgramModel, SubjectModel, SubjectSemesterModel, SubjectTopicModel, AcreditationUserRoleModel

    #all = [GroupModel, UserModel, UserGroupModel, RoleModel, RoleTypeModel, EventModel, EventUserModel, EventGroupModel]
    engine = initEngine(connectionstring) 
    Session = initSession(connectionstring)
    
    if doDropAll:
        BaseModel.metadata.drop_all(engine)
        print('DB Drop Done')
    if doCreateAll:
        BaseModel.metadata.create_all(engine)
        print('DB Create All Done')

    print('table list')
    for item in BaseModel.metadata.tables.keys():
        print('\t', item)
    print('initDb finished')
    return Session

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
    
    initDb(connectionstring, doDropAll=True, doCreateAll=True)
    #initDb(connectionstring)

    app = FastAPI()
    print('init Db')
    fastapiapp.attachFastApi(app, prepareSession)
    graphqlapp.attachGraphQL(app, prepareSession)
    return app

app = buildApp()
