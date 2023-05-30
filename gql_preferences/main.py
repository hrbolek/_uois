import asyncio

#from api.dbdefinitions import ComposeConnectionString, startEngine
from gql_preferences.dbfeeder import initDB
from gql_preferences.DBDefinitions import ComposeConnectionString, startEngine

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

    #result = await startEngine(connectionstring=connectionString, makeDrop=False, makeUp=True)
    result = await startEngine(connectionstring=connectionString, makeDrop=True, makeUp=True)
    
    print(f'initializing system structures')

    ###########################################################################################################################
    #
    # vlozte asynchronni funkce, ktere maji data uvest do prvotniho konzistentniho stavu
   
    await initDB(result)

    ###########################################################################################################################
    print(f'all done')
    return result


from strawberry.asgi import GraphQL
from gql_preferences.dataloaders import createDataLoders

class MyGraphQL(GraphQL):
    """Rozsirena trida zabezpecujici praci se session"""

    async def __call__(self, scope, receive, send):
        asyncSessionMaker = await RunOnceAndReturnSessionMaker()
        async with asyncSessionMaker() as session:
            self._session = session
            self._user = {"id": "f8089aa6-2c4a-4746-9503-105fcc5d054c"}
            return await GraphQL.__call__(self, scope, receive, send)

    async def get_context(self, request, response):
        parentResult = await GraphQL.get_context(self, request, response)
        asyncSessionMaker = await RunOnceAndReturnSessionMaker()
        
        return {
            **parentResult,
            "asyncSessionMaker": asyncSessionMaker,
            "user": self._user,
            #"all_": createDataLoders(asyncSessionMaker),
            "all": await createDataLoders(asyncSessionMaker)
        }


from fastapi import  FastAPI
app = FastAPI()

from gql_preferences.GraphTypeDefinitions import schema
graphql_app = MyGraphQL(schema, graphiql=True, allow_queries_via_get=False)
app.mount("/gql", graphql_app)


@app.on_event("startup")
async def startup_event():
    initizalizedEngine = await RunOnceAndReturnSessionMaker()
    return None

