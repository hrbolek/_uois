from typing_extensions import Required

#from sqlalchemy.sql.sqltypes import Boolean
from graphene import ObjectType, Field, ID, String, List, DateTime, Mutation, Boolean, Int
from graphene import Schema as GSchema

from starlette.graphql import GraphQLApp
#from starlette_graphene import GraphQLApp

import graphene

from graphqltypes.gql_app import query as MainQuery
#import models.BaseEntities as BaseEntities

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


    #router = fastapi.APIRouter()
    #https://github.com/graphql-python/graphene-sqlalchemy/issues/292
    #router = APIRouter()

    session_scope = contextmanager(sessionFunc)

    # class SessionMiddleware(object):
    #     # this does not work because of default resolvers
    #     def resolve(self, next, root, info, **args):
    #         print('SessionMiddleware Action')
    #         with session_scope() as session:
    #             print('info.context', info.context)
    #             info.context['session'] = session
    #             print('query for', args.keys())
    #             return next(root, info, **args)

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
    
    #graphql_app = GraphQLApp(schema=localSchema(query=Query, mutation=Mutations))
    #graphql_app = GraphQLApp(schema=localSchema(query=createQueryRoot(), mutation=Mutations))
    graphql_app = GraphQLApp(schema=localSchema(query=MainQuery))
    
    app.add_route(bindPoint, graphql_app)

