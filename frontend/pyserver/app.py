from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
import os
import aiohttp

from mockoauthserver import server as OAuthServer

# app = FastAPI(root_path="/apif")
app = FastAPI()


@app.get("/ui/msg")
async def apif_read_item(item_id: int):
    return {"hello": "world"}

proxy = "http://localhost:31180/api/gql/"

@app.get("/api/gql/", response_class=HTMLResponse)
async def apigql_get(request: Request):
    print("apigql_get")
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(proxy) as resp:
    #         print(resp.status)
    #         html = await resp.text()
    # print("apigql_get")
    # return html 
    # return FileResponse(path="./graphiql.html")
    result = tryResponse(cwd + "./pyserver/graphiql.html") 
    if result is not None:
        print("ok")
        return result
    print(cwd)

class Item(BaseModel):
    query: str
    variables: dict = None
    operationName: str = None

@app.get("/api/visualize/", response_class=FileResponse)
async def gql_schema_visualizer():
    realpath = os.path.realpath("./pyserver/voyager.html")
    if os.path.isfile(realpath):
        print(realpath)
        return realpath
    print(realpath)
    return realpath

@app.post("/api/gql/", response_class=JSONResponse)
async def apigql_post(data: Item, request: Request):
    # jsonbody = await request.json()
    # print(data.query)
    # print(data.variables)
    # print(data.operationName)

    demoquery={"query": data.query}
    if (data.variables) is not None:
        demoquery["variables"] = data.variables
    if (data.operationName) is not None:
        demoquery["operationName"] = data.operationName

    # print(demoquery)
    async with aiohttp.ClientSession() as session:
        async with session.post(proxy, json=demoquery) as resp:
            # print(resp.status)
            json = await resp.json()
    return JSONResponse(content=json, status_code=resp.status)

import os
import mimetypes
cwd = os.getcwd()

def tryResponse(path):
    realpath = os.path.realpath(path)
    if os.path.isfile(realpath):
        # return FileResponse(realpath)
        return realpath
    
@app.get("/ui/{file_path:path}", response_class=FileResponse)
async def read_file(file_path: str):
    print("cwd", cwd)
    # print("file_path", file_path)

    result = tryResponse(f"./js/{file_path}") 
    if result is not None:
        print(file_path, result, " => ", mimetypes.guess_type(result))
        return result
    
    result = tryResponse(f"./js/index.html") 
    if result is not None:
        print(file_path, result, " => ", mimetypes.guess_type(result))
        return result
    
    result = tryResponse(cwd + f"./build/{file_path}") 
    if result is not None:
        print(file_path, result, " => ", mimetypes.guess_type(result))
        return result
    
    result = tryResponse(cwd + f"./build/index.html") 
    if result is not None:
        print(file_path, result, " => ", mimetypes.guess_type(result))
        return result


# app.mount("/ui", StaticFiles(directory="js"), name="static")

# subapp = FastAPI()
# app.mount('/api', subapp)

app.mount("/oauth", OAuthServer.createServer())
