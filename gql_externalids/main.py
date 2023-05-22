from typing import List
import typing

import asyncio

from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter

## Definice DB typu (pomoci SQLAlchemy https://www.sqlalchemy.org/)
## SQLAlchemy zvoleno kvuli moznost komunikovat s DB asynchronne
## https://docs.sqlalchemy.org/en/14/core/future.html?highlight=select#sqlalchemy.future.select
from gql_externalids.DBDefinitions import startEngine, ComposeConnectionString

## Zabezpecuje prvotni inicializaci DB a definovani Nahodne struktury pro "Univerzity"
from gql_externalids.DBFeeder import initDB

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


@singleCall
async def RunOnceAndReturnSessionMaker():
    """Provadi inicializaci asynchronniho db engine, inicializaci databaze a vraci asynchronni SessionMaker.
    Protoze je dekorovana, volani teto funkce se provede jen jednou a vystup se zapamatuje a vraci se pri dalsich volanich.
    """
    ###########################################################################################################################
    #
    # v teto konkretni implementaci a konfiguraci je tato funkce volana po te, co je spusten kontejner Apollo
    # tento se dotaze na subgrafy podle konfigurace (viz apollo/server.js)
    # v ramci tohoto prvotniho volani se proprve a naposledy spusti tato funkce
    # vystupem teto funkce je SessionMaker, ten je po dobu zivotnosti kontejneru ulozen do pameti
    # kazde dalsi volani jen "vytahuje" tuto strukturu z pameti
    #
    ###########################################################################################################################
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

    # await asyncio.gather(  # concurency running :)
    #     # sem lze dat vsechny funkce, ktere maji nejak inicializovat databazi
    #     # musi byt asynchronniho typu (async def ...)
    #     createSystemDataStructureExternalIdTypes(result),
    #     # createSystemDataStructureGroupTypes(result)
    # )
    await initDB(result)
    ###########################################################################################################################
    print(f"all done")
    return result


from strawberry.asgi import GraphQL

from gql_externalids.Dataloaders import createLoaders_3
class MyGraphQL(GraphQL):
    """Rozsirena trida zabezpecujici praci se session"""

    async def __call__(self, scope, receive, send):
        ###########################################################################################################################
        #
        # tato metoda je volana pokazde, kdyz je posla dotaz na graphQL endpoint
        # metoda fakticky vytvari obalku, ktera zabezpecuje zivot session (vytvoreni a uzavreni, viz context management)
        # session je vytvorena, ulozena a zpristupnena pres metodu get_context
        #
        ###########################################################################################################################

        asyncSessionMaker = await RunOnceAndReturnSessionMaker()
        async with asyncSessionMaker() as session:
            self._session = session
            self._user = {"id": "?"}
            return await GraphQL.__call__(self, scope, receive, send)

    async def get_context(self, request, response):
        parentResult = await GraphQL.get_context(self, request, response)
        asyncSessionMaker = await RunOnceAndReturnSessionMaker()
        return {
            **parentResult,
            "session": self._session,
            "asyncSessionMaker": asyncSessionMaker,
            "user": self._user,
            "all": await createLoaders_3(asyncSessionMaker)
        }


## Definice GraphQL typu (pomoci strawberry https://strawberry.rocks/)
## Strawberry zvoleno kvuli moznosti mit federovane GraphQL API (https://strawberry.rocks/docs/guides/federation, https://www.apollographql.com/docs/federation/)
from gql_externalids.GraphTypeDefinitions import schema

## ASGI app, kterou "moutneme"
graphql_app = MyGraphQL(schema, graphiql=True, allow_queries_via_get=True)

app = FastAPI()
app.mount("/gql", graphql_app)


@app.on_event("startup")
async def startup_event():
    initizalizedEngine = await RunOnceAndReturnSessionMaker()
    return None


print("All initialization is done")

# @app.get('/hello')
# def hello():
#    return {'hello': 'world'}

###########################################################################################################################
#
# pokud jste pripraveni testovat GQL funkcionalitu, rozsirte apollo/server.js
#
###########################################################################################################################
