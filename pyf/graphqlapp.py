from graphene import ObjectType, String, Field, ID, List, DateTime
from graphene import Schema as GSchema

from starlette.graphql import GraphQLApp
import graphene

from fastapi import FastAPI, Request

import models.BaseEntities as BEntities
import models.BaseEntityTypes as BETypes
import models.Relations as Relations

import sqlengine.sqlengine as SqlEngine

connectionString = 'postgresql+psycopg2://postgres:example@postgres/jupyterII'

UserModel, GroupModel, ClassRoomModel, EventModel = BEntities.GetModels()
GroupTypeModel, RoleTypesModel = BETypes.GetModels()
Relations.createRelations()

Session = SqlEngine.init(connectionString)

from contextlib import contextmanager
@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


async def prepareSession():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()    


from fastapi import Depends
from fastapi import APIRouter

def attachGraphQL(app, sessionFunc=prepareSession):
    assert callable(sessionFunc), "sessionFunc must be a function creating session"
    print('attaching attachGraphQL')
    def extractSession(info):
        #return info.context['request'].scope['db_session']
        return info.context.get('session')

    class Group(ObjectType):
        name = String()
        id = ID()
        users = List(lambda: User)
        events = List(lambda: Event)
        
        def resolve_users(parent, info):
            session = extractSession(info)
            groupRecord = session.query(GroupModel).get(parent.id)
            return groupRecord.users #alert, hide passwords!

        def resolve_events(parent, info):
            session = extractSession(info)
            groupRecord = session.query(GroupModel).get(parent.id)
            return groupRecord.events
        
    class Event(ObjectType):
        label = String()
        id = ID()
        start = DateTime()
        end = DateTime()
        
    class User(ObjectType):
        name = String()
        id = ID()
        groups = List(Group)
        events = List(Event)

        def resolve_groups(parent, info):
            session = extractSession(info)
            userRecord = session.query(UserModel).get(parent.id)
            #return [GroupData(group.id, group.name) for group in userRecord.groups]
            return userRecord.groups
        
        def resolve_events(parent, info):
            session = extractSession(info)
            userRecord = session.query(UserModel).get(parent.id)
            return userRecord.events
            
    class Query(ObjectType):

        user = Field(User, id=ID(required=True))
        group = Field(Group, id=ID(required=False, default_value=None), name=String(required=False, default_value=None))
        
        def resolve_user(root, info, id):
            #return {'name': info.context.get('session'), 'id': id}
            #return {'name': info.context['session'], 'id': id}
            session = extractSession(info)
            return session.query(UserModel).get(id)
        
        def resolve_group(root, info, id=None, name=None):
            
            session = extractSession(info)
            if id is None:
                return session.query(GroupModel).filter(GroupModel.name == name).first()
            else:
                return session.query(GroupModel).get(id)


    #router = fastapi.APIRouter()
    #https://github.com/graphql-python/graphene-sqlalchemy/issues/292
    #router = APIRouter()


    class localSchema(graphene.Schema):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

        def execute(self, *args, **kwargs):
            with session_scope() as session:
                if 'context' in kwargs:
                    newkwargs = {**kwargs, 'context': {**kwargs['context'], 'session': session}}
                else:
                    newkwargs = {**kwargs, 'context': {'session': session}}
                return super().execute(*args, **newkwargs)

        async def execute_async(self, *args, **kwargs):
            return await super().execute_async(*args, **kwargs)

    #graphql_app = GraphQLApp(schema=graphene.Schema(query=Query))
    #app.add_route("/gql/", graphql_app)
    graphql_app = GraphQLApp(schema=localSchema(query=Query))
    app.add_route("/gql/", graphql_app)

    #app.add_route("/gql/", GraphQLApp(schema=graphene.Schema(query=Query)))
    
    #@router.post('/gql/')
    async def query(request: Request, db: Session = Depends(sessionFunc)):
        request.scope.setdefault('db_session', db)
        return await graphql_app.handle_graphql(request=request)

    #@router.get('/gql/')
    async def query(request: Request, db: Session = Depends(sessionFunc)):
        request.scope.setdefault('db_session', db)
        return await graphql_app.handle_graphql(request=request)
