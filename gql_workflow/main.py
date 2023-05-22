from typing import List
import typing

import asyncio

from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter

## Definice GraphQL typu (pomoci strawberry https://strawberry.rocks/)
## Strawberry zvoleno kvuli moznosti mit federovane GraphQL API (https://strawberry.rocks/docs/guides/federation, https://www.apollographql.com/docs/federation/)
from gql_workflow.GraphTypeDefinitions import Query

## Definice DB typu (pomoci SQLAlchemy https://www.sqlalchemy.org/)
## SQLAlchemy zvoleno kvuli moznost komunikovat s DB asynchronne
## https://docs.sqlalchemy.org/en/14/core/future.html?highlight=select#sqlalchemy.future.select
from gql_workflow.DBDefinitions import startEngine, ComposeConnectionString

## Zabezpecuje prvotni inicializaci DB a definovani Nahodne struktury pro "Univerzity"
# from gql_workflow.DBFeeder import createSystemDataStructureRoleTypes, createSystemDataStructureGroupTypes

connectionString = ComposeConnectionString()


def singleCall(asyncFunc):
    """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
    Dekorovana funkce je asynchronni.
    """
    resultCache = {}

    async def result():
        if resultCache.get("result", None) is None:
            resultCache["result"] = await asyncFunc()
        return resultCache["result"]

    return result

from gql_workflow.DBFeeder import initDB

@singleCall
async def RunOnceAndReturnSessionMaker():
    """Provadi inicializaci asynchronniho db engine, inicializaci databaze a vraci asynchronni SessionMaker.
    Protoze je dekorovana, volani teto funkce se provede jen jednou a vystup se zapamatuje a vraci se pri dalsich volanich.
    """

    print(f'starting engine for "{connectionString}"')
    import os
    makeDrop = os.environ.get("DEMO", "") == "true"
    result = await startEngine(
        connectionstring=connectionString, makeDrop=makeDrop, makeUp=True
    )

    print(f"initializing system structures")

    ###########################################################################################################################
    #
    # zde definujte do funkce asyncio.gather
    # vlozte asynchronni funkce, ktere maji data uvest do prvotniho konzistentniho stavu
    await initDB(result)
    # await asyncio.gather( # concurency running :)
    # sem lze dat vsechny funkce, ktere maji nejak inicializovat databazi
    # musi byt asynchronniho typu (async def ...)
    # createSystemDataStructureRoleTypes(result),
    # createSystemDataStructureGroupTypes(result)
    # )

    ###########################################################################################################################
    print(f"all done")
    return result


from strawberry.asgi import GraphQL

from gql_workflow.Dataloaders import createLoaders
async def createContext():
    asyncSessionMaker = await RunOnceAndReturnSessionMaker()
    loaders = await createLoaders(asyncSessionMaker)
    return {
        "asyncSessionMaker": await RunOnceAndReturnSessionMaker(),
        "all": await createLoaders(asyncSessionMaker),
        #**loaders,
    }


class MyGraphQL(GraphQL):
    """Rozsirena trida zabezpecujici praci se session"""

    async def __call__(self, scope, receive, send):
        # print("another gql call (ug)")
        # for item in scope['headers']:
        #    print(item)
        self._user = "?"
        result = await GraphQL.__call__(self, scope, receive, send)
        return result

    async def get_context(self, request, response):
        parentResult = await GraphQL.get_context(self, request, response)
        localResult = await createContext()
        return {**parentResult, **localResult, "user": self._user}


from gql_workflow.GraphTypeDefinitions import schema
## ASGI app, kterou "moutneme"
graphql_app = MyGraphQL(
    schema, graphiql=True, allow_queries_via_get=True
)

app = FastAPI()
app.mount("/gql", graphql_app)

print("All initialization is done")

# @app.get('/hello')
# def hello():
#    return {'hello': 'world'}
