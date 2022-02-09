from urllib.request import Request
from starlette.graphql import GraphQLApp

from dbInit import GetSession
from DatabaseModel.myDevTools import *
from DatabaseModel import randomData
from DatabaseModel.models import PersonModel, LessonModel, StudentModel, ProgramModel, GroupModel, SubjectModel, SemesterModel, GroupTypeModel, LessonTypeModel, RoomModel, BuildingModel, AreaModel

import dbInit

from fastapi import FastAPI
import graphqlapp
import svgapp

def buildApp():
    Session = GetSession()
    
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
            
    app = FastAPI()
    graphqlapp.attachGraphQL(app, prepareSession)
    svgapp.attachSVGApp(app)
    return app

dbInit.InitAndRandomize()
print('All initialization is done')
app = buildApp()

