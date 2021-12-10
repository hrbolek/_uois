from typing_extensions import Required

#from sqlalchemy.sql.sqltypes import Boolean
from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean
from graphene import Schema as GSchema

from starlette.graphql import GraphQLApp
#from starlette_graphene import GraphQLApp

import graphene

import models.BaseEntities as BaseEntities

from contextlib import contextmanager

def attachGraphQL(app, sessionFunc, bindPoint='/gql'):
    """Attaches a Swagger endpoint to a FastAPI

    Parameters
    ----------
    app: FastAPI
        app to bind to
    prepareSession: lambda : session
        callable which returns a db session
    """
    assert callable(sessionFunc), "sessionFunc must be a function creating a session"

    session_scope = contextmanager(sessionFunc)
    UserModel, GroupModel, RoleModel, GroupTypeModel, RoleTypeModel = BaseEntities.GetModels()

    print('attaching attachGraphQL')
    def extractSession(info):
        #return info.context['request'].scope['db_session']
        return info.context.get('session')

    class GroupType(ObjectType):
        id = ID()
        name = String()
        groups = List(lambda: Group)

    class Group(ObjectType):
        name = String()
        id = ID()
        users = List(lambda: User)
        events = List(lambda: Event)
        grouptype_id = ID()
        
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
        id = ID()
        name = String()
        surname = String()
        email = String()
        
        groups = List(Group)
        groups_by_type = Field(List(Group), typeId=ID())
        events = List(Event)

        def resolve_groups_by_type(parent, info, typeId):
            session = extractSession(info)
            userRecord = session.query(UserModel).get(parent.id)
            return filter(lambda item: str(item.grouptype_id) == typeId, userRecord.groups)


        def resolve_groups(parent, info):
            session = extractSession(info)
            userRecord = session.query(UserModel).get(parent.id)
            #return [GroupData(group.id, group.name) for group in userRecord.groups]
            return userRecord.groups
        
        def resolve_events(parent, info):
            session = extractSession(info)
            userRecord = session.query(UserModel).get(parent.id)
            return userRecord.events
            
    class CreateUser(Mutation):
        class Arguments:
            id = ID(required=False)
            surname = String(required=False)
            name = String(required=False)
            email = String(required=False)

        ok = Boolean()
        user = Field(User)

        def mutate(root, info, id=None, name=None, surname=None, email=None):
            session = extractSession(info)
            dataRecord = UserModel(name=name, surname=surname, email=email)
            session.add(dataRecord)
            session.commit()
            return CreateUser(user=dataRecord, ok=True)

    class UpdateUser(Mutation):
        class Arguments:
            id = ID(required=False)
            surname = String(required=False)
            name = String(required=False)
            email = String(required=False)

        ok = Boolean()
        user = Field(User)

        def mutate(root, info, id=None, name=None, surname=None, email=None):
            session = extractSession(info)

            dataRecord = session.query(UserModel).get(id)
            if not(name is None):
                dataRecord.name = name
            if not(surname is None):
                dataRecord.surname = surname
            if not(email is None):
                dataRecord.email = email
            session.commit()

            return CreateUser(user=dataRecord, ok=True)

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

    class Mutations(ObjectType):
        create_user = CreateUser.Field()
        update_user = UpdateUser.Field()

    #router = fastapi.APIRouter()
    #https://github.com/graphql-python/graphene-sqlalchemy/issues/292
    #router = APIRouter()

    class SessionMiddleware(object):
        def resolve(self, next, root, info, **args):
            print('SessionMiddleware Action')
            with session_scope() as session:
                print('info.context', info.context)
                info.context['session'] = session
                print('query for', args.keys())
                return next(root, info, **args)


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
            with session_scope() as session:
                if 'context' in kwargs:
                    newkwargs = {**kwargs, 'context': {**kwargs['context'], 'session': session}}
                else:
                    newkwargs = {**kwargs, 'context': {'session': session}}
                return await super().execute_async(*args, **newkwargs)



    #graphql_app = GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutations), context_value={'session': None})#, middleware=[SessionMiddleware()])
    #app.add_route("/gql/", graphql_app)
    graphql_app = GraphQLApp(schema=localSchema(query=Query, mutation=Mutations))
    
    app.add_route(bindPoint, graphql_app)

