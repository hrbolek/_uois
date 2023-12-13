import logging
import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from mockoauthserver import server as OAuthServer

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s.%(msecs)03d\t%(levelname)s:\t%(message)s', 
    datefmt='%Y-%m-%dT%I:%M:%S')


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
app = FastAPI()


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
    subApp = FastAPI()
    @subApp.get("/{file_path:path}")
    async def getFile(file_path: str):
        return FileResponse(dirName + "/htmls/" + file)
    
    if not DEMO:
        subApp.add_middleware(BasicAuthenticationMiddleware302, backend=BasicAuthBackend(JWTPUBLICKEY=JWTPUBLICKEY, JWTRESOLVEUSERPATH=JWTRESOLVEUSERPATH))
    app.mount("/" + key, subApp)

with open(configFile, "r", encoding="utf-8") as f:
    config = json.load(f)
    for key, setup in config.items():
        createApp(key, setup)


#######################################################################
#
# tato cast je pro FAKE autentizaci
# poskytuje autentizacni (prihlasovaci stranku)
# ma volny pristup
#
#######################################################################
users= [
        {
            "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
            "name": "John",
            "surname": "Newbie",
            "email": "john.newbie@world.com"
        },
        {
            "id": "2d9dc868-a4a2-11ed-b9df-0242ac120003",
            "name": "Julia",
            "surname": "Newbie",
            "email": "julia.newbie@world.com"
        },
        {
            "id": "2d9dc9a8-a4a2-11ed-b9df-0242ac120003",
            "name": "Johnson",
            "surname": "Newbie",
            "email": "johnson.newbie@world.com"
        },
        {
            "id": "2d9dcbec-a4a2-11ed-b9df-0242ac120003",
            "name": "Jepeto",
            "surname": "Newbie",
            "email": "jepeto.newbie@world.com"
        }]

db_users = [{"id": user["id"], "email": user["email"]} for user in users]
app.mount("/oauth", OAuthServer.createServer(db_users=db_users))

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

