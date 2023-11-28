import os
import aiohttp
from fastapi.responses import JSONResponse, FileResponse
from fastapi import Request
from pydantic import BaseModel

import prometheus
collectTime = prometheus.collectTime

class Item(BaseModel):
    query: str
    variables: dict = None
    operationName: str = None

def connectProxy(app):

    proxy = os.environ.get("GQL_PROXY", "http://10.0.2.27:31180/api/gql/")
    print("using proxy", proxy)

    @app.get("/api/gql", response_class=FileResponse)
    async def apigql_get():
        realpath = os.path.realpath("./graphiql.html")
        result = realpath
        return result

    @app.get("/api/doc", response_class=FileResponse)
    async def apidoc_get():
        realpath = os.path.realpath("./voyager.html")
        result = realpath
        return result

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