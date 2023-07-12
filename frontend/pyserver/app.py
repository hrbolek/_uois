import mimetypes
import os
import aiohttp
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse

from prometheus import prometheusClient, collectTime

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


@app.get("/docs/visualize/", response_class=FileResponse)
async def gql_schema_visualizer():
    realpath = os.path.realpath("./voyager.html")
    return realpath

@app.get("/docs/{file_path:path}")
async def read_docs_file(file_path: str):
    print(file_path)
    if os.path.isfile(f"./storybook/{file_path}"):
        return FileResponse(f"./storybook/{file_path}")
    else:
        return FileResponse(f"./storybook/index.html")

# @app.get("/docs/visualize/", response_class=FileResponse)
# async def gql_schema_visualizer():
#     realpath = os.path.realpath("./voyager.html")
#     return realpath

@app.get("/docs/")
async def read_docs_file(file_path: str):
    return FileResponse(f"./storybook/index.html")

# proxy = "http://localhost:31180/api/gql/"
# proxy = "http://10.0.2.27:31180/api/gql/"
#proxy = os.environ.get("GQL_PROXY", "http://localhost:31180/api/gql/")
proxy = os.environ.get("GQL_PROXY", "http://10.0.2.27:31180/api/gql/")
print("using proxy", proxy)
@app.get("/api/gql", response_class=FileResponse)
async def apigql_get():
    realpath = os.path.realpath("./graphiql.html")
    result = realpath
    return result

class Item(BaseModel):
    query: str
    variables: dict = None
    operationName: str = None

@collectTime("gqlquery")
@app.post("/api/gql", response_class=JSONResponse)
async def apigql_post(data: Item, request: Request):
    gqlQuery = {"query": data.query}
    if (data.variables) is not None:
        gqlQuery["variables"] = data.variables
    if (data.operationName) is not None:
        gqlQuery["operationName"] = data.operationName

    # print(demoquery)
    headers = request.headers
    print(headers)
    print(headers.__dict__)
    headers = {}
    async with aiohttp.ClientSession() as session:
        async with session.post(proxy, json=gqlQuery, headers=headers) as resp:
            # print(resp.status)
            json = await resp.json()
    return JSONResponse(content=json, status_code=resp.status)



# def tryResponse(path):
#     realpath = os.path.realpath(path)
#     if os.path.isfile(realpath):
#         # return FileResponse(realpath)
#         return realpath
    
# @app.get("/ui/{file_path:path}", response_class=FileResponse)
# async def read_file(file_path: str):
#     print("cwd", cwd)
#     # print("file_path", file_path)

#     result = tryResponse(f"./js/{file_path}") 
#     if result is not None:
#         print(file_path, result, " => ", mimetypes.guess_type(result))
#         return result
    
#     result = tryResponse(f"./js/index.html") 
#     if result is not None:
#         print(file_path, result, " => ", mimetypes.guess_type(result))
#         return result
    
#     result = tryResponse(cwd + f"./build/{file_path}") 
#     if result is not None:
#         print(file_path, result, " => ", mimetypes.guess_type(result))
#         return result
    
#     result = tryResponse(cwd + f"./build/index.html") 
#     if result is not None:
#         print(file_path, result, " => ", mimetypes.guess_type(result))
#         return result



from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
