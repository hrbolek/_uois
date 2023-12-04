import mimetypes
import os
import aiohttp
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse

from .prometheus import prometheusClient, collectTime

from mockoauthserver import server as OAuthServer

# app = FastAPI(root_path="/apif")
app = FastAPI()

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

uiApp = FastAPI()

@uiApp.get("/msg")
async def apif_read_item(requets: Request):
    client = requets.client
    headers = requets.headers
    cookies = requets.cookies

    return {
        "hello": "world",
        "client": client,
        "headers": headers,
        "cookies": cookies
        }

@uiApp.get("/{file_path:path}")
async def read_file(file_path: str):
    print(file_path)
    if os.path.isfile(f"./js/{file_path}"):
        return FileResponse(f"./js/{file_path}")
    else:
        return FileResponse(f"./js/index.html")

docsApp = FastAPI()
@docsApp.get("/{file_path:path}")
async def read_docs_file(file_path: str):
    print(file_path)
    if os.path.isfile(f"./storybook/{file_path}"):
        return FileResponse(f"./storybook/{file_path}")
    else:
        return FileResponse(f"./storybook/index.html")

@docsApp.get("/")
async def read_docs_file(file_path: str):
    return FileResponse(f"./storybook/index.html")

apiApp = FastAPI()

from .gqlproxy import connectProxy
connectProxy(apiApp)

from .authenticationMiddleware import BasicAuthenticationMiddleware302, BasicAuthBackend
JWTPUBLICKEY = os.environ.get("JWTPUBLICKEY", "http://localhost:8000/oauth/publickey")
JWTRESOLVEUSERPATH = os.environ.get("JWTRESOLVEUSERPATH", "http://localhost:8000/oauth/userinfo")

uiApp.add_middleware(BasicAuthenticationMiddleware302, backend=BasicAuthBackend(JWTPUBLICKEY=JWTPUBLICKEY, JWTRESOLVEUSERPATH=JWTRESOLVEUSERPATH))
docsApp.add_middleware(BasicAuthenticationMiddleware302, backend=BasicAuthBackend(JWTPUBLICKEY=JWTPUBLICKEY, JWTRESOLVEUSERPATH=JWTRESOLVEUSERPATH))
apiApp.add_middleware(BasicAuthenticationMiddleware302, backend=BasicAuthBackend(JWTPUBLICKEY=JWTPUBLICKEY, JWTRESOLVEUSERPATH=JWTRESOLVEUSERPATH))

app.mount("/api", apiApp)
app.mount("/ui", uiApp)
app.mount("/doc", docsApp)

from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app, endpoint="/metrics")