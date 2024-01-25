import logging
import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager

from mockoauthserver import server as OAuthServer

from .users import (
    ComposeConnectionString, 
    startEngine, initDB, 
    getDemoData, passwordValidator, emailMapper
)

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s.%(msecs)03d\t%(levelname)s:\t%(message)s', 
    datefmt='%Y-%m-%dT%I:%M:%S')


# region DB setup

## Definice GraphQL typu (pomoci strawberry https://strawberry.rocks/)
## Strawberry zvoleno kvuli moznosti mit federovane GraphQL API (https://strawberry.rocks/docs/guides/federation, https://www.apollographql.com/docs/federation/)
## Definice DB typu (pomoci SQLAlchemy https://www.sqlalchemy.org/)
## SQLAlchemy zvoleno kvuli moznost komunikovat s DB asynchronne
## https://docs.sqlalchemy.org/en/14/core/future.html?highlight=select#sqlalchemy.future.select


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

@singleCall
async def RunOnceAndReturnSessionMaker():
    """Provadi inicializaci asynchronniho db engine, inicializaci databaze a vraci asynchronni SessionMaker.
    Protoze je dekorovana, volani teto funkce se provede jen jednou a vystup se zapamatuje a vraci se pri dalsich volanich.
    """

    makeDrop = os.getenv("DEMO", None) in ["True", True]
    logging.info(f'starting engine for "{connectionString} makeDrop={makeDrop}"')

    asyncSessionMaker = await startEngine(
        connectionstring=connectionString, makeDrop=makeDrop, makeUp=True
    )

    logging.info(f"initializing system structures")

    await initDB(asyncSessionMaker)

    logging.info(f"all done")
    return asyncSessionMaker

# endregion


DEMO = os.getenv("DEMO", None)
assert DEMO is not None, "DEMO environment variable must be explicitly defined"
assert (DEMO == "True") or (DEMO == "False"), "DEMO environment variable can have only `True` or `False` values"
DEMO = DEMO == "True"

if DEMO:
    print("####################################################")
    print("#                                                  #")
    print("# RUNNING IN DEMO                                  #")
    print("#                                                  #")
    print("####################################################")

    logging.info("####################################################")
    logging.info("#                                                  #")
    logging.info("# RUNNING IN DEMO                                  #")
    logging.info("#                                                  #")
    logging.info("####################################################")



# app = FastAPI(root_path="/apif")
@asynccontextmanager
async def lifespan(app: FastAPI):
    initizalizedEngine = await RunOnceAndReturnSessionMaker()
    yield

app = FastAPI(lifespan=lifespan)

from .appindex import createIndexResponse
# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request, exc):
#     print(exc)
#     return await createIndexResponse(request=request)

from .authenticationMiddleware import BasicAuthenticationMiddleware302, BasicAuthBackend
JWTPUBLICKEY = os.environ.get("JWTPUBLICKEY", "http://localhost:8000/oauth/publickey")
JWTRESOLVEUSERPATH = os.environ.get("JWTRESOLVEUSERPATH", "http://localhost:8000/oauth/userinfo")


from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

import json

#######################################################################
#
# pouziti html jako SPA - single page applications
# predpoklada se, ze html maji integrovany router (react-router) 
# a ze si obslouzi zbytek cesty
# aplikace jsou chraneny autentizaci
#
#######################################################################
configFile = "config.json"
dirName = ""
if __file__:
    dirName = os.path.dirname(__file__)

print("executing in", dirName)

configFile = dirName + "/" + configFile
def createApp(key, setup):
    file = setup["file"]
    print(f"creating sub app {key} with setup {setup}")
    subApp = FastAPI()
    @subApp.get("/{file_path:path}")
    async def getFile(file_path: str):
        filename = dirName + "/htmls/" + file
        print(f"serving app {file} from `{filename}`")
        if os.path.isfile(filename):
            return FileResponse(filename)
        else:
            return RedirectResponse("/")
    
    if not DEMO:
        subApp.add_middleware(BasicAuthenticationMiddleware302, backend=BasicAuthBackend(JWTPUBLICKEY=JWTPUBLICKEY, JWTRESOLVEUSERPATH=JWTRESOLVEUSERPATH))
    app.mount("/" + key, subApp)

with open(configFile, "r", encoding="utf-8") as f:
    config = json.load(f)
    print(f"app config set to\n{config}")
    for key, setup in config.items():
        createApp(key, setup)

@app.get("/logout")
def logout():
    result = RedirectResponse("/oauth/login2?redirect_uri=/", status_code=303)
    result.delete_cookie("authorization")
    return result

#######################################################################
#
# tato cast je pro FAKE autentizaci
# poskytuje autentizacni (prihlasovaci stranku)
# ma volny pristup
#
#######################################################################
demoData = getDemoData()
users = demoData.get("users", [])

async def bindedPasswordValidator(email, password):
    asyncSessionMaker = await RunOnceAndReturnSessionMaker()
    print(f"check for {email} & {password}")
    result = await passwordValidator(asyncSessionMaker, email, password)
    return result

async def bindedEmailMapper(email):
    asyncSessionMaker = await RunOnceAndReturnSessionMaker()
    result = await emailMapper(asyncSessionMaker, email)
    return result

db_users = [{"id": user["id"], "email": user["email"]} for user in users]
app.mount("/oauth", OAuthServer.createServer(
    db_users=db_users,
    passwordValidator=bindedPasswordValidator,
    emailMapper=bindedEmailMapper
    ))

#######################################################################
#
# tato cast je proxy pro API endpoint
# je dostupna jen s autentizaci
#
#######################################################################

apiApp = FastAPI()
if not DEMO:
    apiApp.add_middleware(BasicAuthenticationMiddleware302, backend=BasicAuthBackend(JWTPUBLICKEY=JWTPUBLICKEY, JWTRESOLVEUSERPATH=JWTRESOLVEUSERPATH))
app.mount("/api", apiApp)

from .gqlproxy import connectProxy
connectProxy(apiApp)

#######################################################################
#
# tato cast je pro debug
# je dostupna jen s autentizaci
#
#######################################################################

debugApp = FastAPI()

@debugApp.get("/")
async def hello(requets: Request):
    client = requets.client
    headers = requets.headers
    cookies = requets.cookies

    return {
        "hello": "world",
        "client": client,
        "headers": headers,
        "cookies": cookies
        }

if not DEMO:
    debugApp.add_middleware(BasicAuthenticationMiddleware302, backend=BasicAuthBackend(JWTPUBLICKEY=JWTPUBLICKEY, JWTRESOLVEUSERPATH=JWTRESOLVEUSERPATH))

app.mount("/debug", debugApp)

@app.get("/")
async def index(request: Request):
    return await createIndexResponse(request=request)