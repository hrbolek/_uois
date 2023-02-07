from fastapi import FastAPI
from gql_ug.DBDefinitions import startEngine, ComposeConnectionString

## Zabezpecuje prvotni inicializaci DB a definovani Nahodne struktury pro "Univerzity"
from gql_ug.DBFeeder import predefineAllDataStructures

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
    print(f'starting engine for "{connectionString}"')

    result = await startEngine(
        connectionstring=connectionString, makeDrop=False, makeUp=True
    )

    print(f"initializing system structures")
    await predefineAllDataStructures(result)

    print(f"all done")
    return result


from strawberry.asgi import GraphQL
from gql_ug.Dataloaders import createLoaders, createLoaders_3


async def createContext():
    asyncSessionMaker = await RunOnceAndReturnSessionMaker()
    loaders = await createLoaders(asyncSessionMaker)
    return {
        "asyncSessionMaker": await RunOnceAndReturnSessionMaker(),
        "all": await createLoaders_3(asyncSessionMaker),
        **loaders,
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


from gql_ug.GraphTypeDefinitions import schema

## ASGI app, kterou "moutneme"
graphql_app = MyGraphQL(
    # strawberry.federation.Schema(Query),
    schema,
    graphiql=True,
    allow_queries_via_get=True,
)

app = FastAPI()
app.mount("/gql", graphql_app)


@app.on_event("startup")
async def startup_event():
    initizalizedEngine = await RunOnceAndReturnSessionMaker()
    return None


print("All initialization is done")
