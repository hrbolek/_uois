from datetime import datetime
from multiprocessing import connection
from typing import List
import typing

import asyncio

from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter

## Definice GraphQL typu (pomoci strawberry https://strawberry.rocks/)
## Strawberry zvoleno kvuli moznosti mit federovane GraphQL API (https://strawberry.rocks/docs/guides/federation, https://www.apollographql.com/docs/federation/)
from gql_ug.GraphTypeDefinitions import Query, UserGQLModel, GroupGQLModel

## Definice DB typu (pomoci SQLAlchemy https://www.sqlalchemy.org/)
## SQLAlchemy zvoleno kvuli moznost komunikovat s DB asynchronne
## https://docs.sqlalchemy.org/en/14/core/future.html?highlight=select#sqlalchemy.future.select
from gql_ug.DBDefinitions import startEngine, ComposeConnectionString, UserModel, GroupModel
from gql_ug.GraphResolvers import createDataLoaderResolver

## Zabezpecuje prvotni inicializaci DB a definovani Nahodne struktury pro "Univerzity"
from gql_ug.DBFeeder import createSystemDataStructureRoleTypes, createSystemDataStructureGroupTypes

connectionString = ComposeConnectionString()

def singleCall(asyncFunc):
    """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
       Dekorovana funkce je asynchronni.
    """
    resultCache = {}
    async def result():
        if resultCache.get('result', None) is None:
            resultCache['result'] = await asyncFunc()
        return resultCache['result']
    return result

@singleCall
async def RunOnceAndReturnSessionMaker():
    """Provadi inicializaci asynchronniho db engine, inicializaci databaze a vraci asynchronni SessionMaker.
       Protoze je dekorovana, volani teto funkce se provede jen jednou a vystup se zapamatuje a vraci se pri dalsich volanich.
    """
    print(f'starting engine for "{connectionString}"')

    result = await startEngine(connectionstring=connectionString, makeDrop=False, makeUp=True)
    
    print(f'initializing system structures')
    await asyncio.gather( # concurency running :)
    # sem lze dat vsechny funkce, ktere maji nejak inicializovat databazi
    # musi byt asynchronniho typu (async def ...)
        createSystemDataStructureRoleTypes(result),
        createSystemDataStructureGroupTypes(result)
    )
    print(f'all done')

    definition = {
        'user': {'DBModel': UserModel, 'GQLModel': UserGQLModel},
        'group': {'DBModel': GroupModel, 'GQLModel': GroupGQLModel}
    }
    loaders = createDataLoaderResolver(definition)(result)
    print('loaders created', list(loaders.keys()))
    return result

from strawberry.asgi import GraphQL

shared = {
    'counter': 0
}
class MyGraphQL(GraphQL):
    """Rozsirena trida zabezpecujici praci se session"""
    async def __call__(self, scope, receive, send):
        #print("another gql call (ug)")
        #for item in scope['headers']:
        #    print(item)


        import datetime
        import uuid
        from sqlalchemy.orm import sessionmaker

        from sqlalchemy.ext.asyncio import AsyncSession
        from sqlalchemy.ext.asyncio import create_async_engine

        asyncEngine = create_async_engine(connectionString, pool_pre_ping=True, 
            pool_size=20, max_overflow=10, pool_recycle=60, echo_pool="debug") #pool_pre_ping=True, pool_recycle=3600

        asyncSessionMaker = sessionmaker(
            asyncEngine, expire_on_commit=False, class_=AsyncSession
        )

        #asyncSessionMaker = await RunOnceAndReturnSessionMaker()
        #asyncSessionMaker = await startEngine(connectionstring=connectionString)
        hash = f'{uuid.uuid1()}'
        print(datetime.datetime.now(), 'Enter', hash, flush=True)
        async with asyncSessionMaker() as session:
            async with session.begin():
                #shared['counter'] = shared['counter'] + 1
                #print('Plus', shared['counter'])
                #print(session.in_transaction())
                self._session = session
                self._user = {'id': '?'}
                try:
                    result = await GraphQL.__call__(self, scope, receive, send)
                    await session.commit()
                finally:
                    await session.close()
                #shared['counter'] = shared['counter'] - 1
                #print('Minus', shared['counter'])
                print(datetime.datetime.now(), 'Leave', hash, flush=True)
                return result
    
    async def get_context(self, request, response):
        parentResult = await GraphQL.get_context(self, request, response)
        return {**parentResult, 
            'session': self._session, 
            'asyncSessionMaker': await RunOnceAndReturnSessionMaker(),
            'user': self._user
            }
from gql_ug.GraphResolvers import entities_resolver as entities_resolver_external
class MySchema(strawberry.federation.Schema):
    async def execute(
            self,
            query: str,
            variable_values = None,
            context_value = None,
            root_value = None,
            operation_name = None,
            allowed_operation_types = None,
        ):
        params = {'query': query, 'variable_values': variable_values, 
            'context_value': context_value, 'root_value': root_value, 'operation_name': operation_name, 
            'allowed_operation_types': allowed_operation_types}

        #print(params, flush=True)
        return await strawberry.federation.Schema.execute(self, query, variable_values, context_value, root_value, operation_name, allowed_operation_types)
        #return strawberry.federation.Schema.execute_sync(self, query, variable_values, context_value, root_value, operation_name, allowed_operation_types)
    def entities_resolver(self, root, info, representations):
        print('entities_resolver', representations, flush=True)
        return entities_resolver_external(self, root, info, representations)

## ASGI app, kterou "moutneme"
graphql_app = MyGraphQL(
    #strawberry.federation.Schema(Query), 
    MySchema(Query), 
    graphiql = True,
    allow_queries_via_get = True
)

app = FastAPI()
app.mount("/gql", graphql_app)

print('All initialization is done')

#@app.get('/hello')
#def hello():
#    return {'hello': 'world'}