import mimetypes
import os
import aiohttp
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse

import prometheus
prometheusClient = prometheus.prometheusClient
collectTime = prometheus.collectTime

from mockoauthserver import server as OAuthServer

# app = FastAPI(root_path="/apif")
app = FastAPI()


@app.get("/ui/msg")
async def apif_read_item(item_id: int):
    return {"hello": "world"}
app.mount("/oauth", OAuthServer.createServer())

oauthserver = "http://localhost:8000/oauth"
oauthservergettoken = oauthserver + "/token"
oauthservergetuser = oauthserver + "/userinfo"
callbackurl = ""
clientsecret = os.environ.get("CLIENTSECRET", "clientsecret")
clientid = os.environ.get("CLIENTID", "clientid")

@app.get("/ui/login")
async def login_with_get():
    return None

@app.get("/ui/login")
async def login_with_get(code: str, state: str):
    queryparams = {
        "client_id": clientid,
        "client_secret": clientsecret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": callbackurl
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(oauthservergettoken, params=queryparams) as resp:           
            jwttext = await resp.text()
    print("jwttext", jwttext)

    return {"hello": "world"}



@app.get("/ui/{file_path:path}")
async def read_file(file_path: str):
    print(file_path)
    if os.path.isfile(f"./js/{file_path}"):
        return FileResponse(f"./js/{file_path}")
    else:
        return FileResponse(f"./js/index.html")

@app.get("/docs/{file_path:path}")
async def read_docs_file(file_path: str):
    print(file_path)
    if os.path.isfile(f"./storybook/{file_path}"):
        return FileResponse(f"./storybook/{file_path}")
    else:
        return FileResponse(f"./storybook/index.html")

@app.get("/docs/")
async def read_docs_file(file_path: str):
    return FileResponse(f"./storybook/index.html")


import gqlproxy 
gqlproxy.connectProxy(app)

from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
