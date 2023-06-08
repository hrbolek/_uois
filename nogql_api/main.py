from typing import List
import typing

import asyncio

from fastapi import FastAPI

## Definice DB typu (pomoci SQLAlchemy https://www.sqlalchemy.org/)
## SQLAlchemy zvoleno kvuli moznost komunikovat s DB asynchronne
## https://docs.sqlalchemy.org/en/14/core/future.html?highlight=select#sqlalchemy.future.select

from nogql_api.DBDefinitions import (
    ComposeConnectionString,
    startEngine,
    createBasicDataStructure,
)

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

    ###########################################################################################################################
    #
    # zde definujte do funkce asyncio.gather
    # vlozte asynchronni funkce, ktere maji data uvest do prvotniho konzistentniho stavu

    await asyncio.gather(  # concurency running :)
        # sem lze dat vsechny funkce, ktere maji nejak inicializovat databazi
        # musi byt asynchronniho typu (async def ...)
        createBasicDataStructure(result)
        # createSystemDataStructureRoleTypes(result),
        # createSystemDataStructureGroupTypes(result)
    )

    ###########################################################################################################################
    print(f"all done")
    return result


apiApp = FastAPI()

print("All initialization is done")


@apiApp.get("/hello")  # do not remove, healthchecks are based on this
def hello():
    return {"hello": "world"}


from fastapi import UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from typing import List

from nogql_api.resolvers import create_upload_file_one


@apiApp.post("/nogql/utils/vykazy/")
async def utils_vykazy_post(files: List[UploadFile] = File(...)):
    print("POST", "/nogql/utils/vykazy/", flush=True)
    result = None
    try:
        result = await create_upload_file_one(files)
    except Exception as e:
        print(e, flush=True)
    return result


@apiApp.get("/nogql/utils/vykazy/")
async def utils_vykazy_get():
    print("GET", "/nogql/utils/vykazy/", flush=True)
    content = """
<!DOCTYPE html>
<html lang="en">
    <head>
    <title>Vykazy</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
    </head>
    <body>

        <div class="container-fluid p-5 bg-primary text-white text-center">
            <h1>Výkazy</h1>
        </div>
        
        <div class="container mt-5">
            <div class="row">
                <div class="col">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">
                                Vyberte jeden soubor (.xlsx) a v tomto budou vytvořeny výkazy pro jednotlivé měsíce.
                            </div>
                        </div>
                        <div class="card-body">
                            <form action="." enctype="multipart/form-data" method="post">
                                <div class="mb-3">
                                    <label for="files" class="form-label">Soubor / soubory</label>
                                    <input class="form-control" name="files" type="file" id="files" multiple>
                                </div>
                                <input class="form-control btn btn-outline-primary" type="submit">
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </body>
</html>
    """
    return HTMLResponse(content=content)


from nogql_api.resolvers import exportSchema, getSystemDataJSON


@apiApp.get("/nogql/utils/umlschema")
async def utils_umlschema_get():
    return await exportSchema()

import json
@apiApp.get("/nogql/system", response_class=JSONResponse)
async def utils_system_get():
    result = await getSystemDataJSON()
    return (json.loads(result))

@apiApp.get("/static/{file_path:path}", response_class=FileResponse)
async def static_get(file_path: str):   
    return f"./static/{file_path}"

app = FastAPI()
app.mount("/api", apiApp)

# #https://stackoverflow.com/questions/70610266/proxy-an-external-website-using-python-fast-api-not-supporting-query-params

# import httpx
# from httpx import AsyncClient
# from fastapi import Request
# from fastapi.responses import StreamingResponse
# from starlette.background import BackgroundTask

# app = FastAPI()
# HTTP_SERVER = AsyncClient(base_url="http://localhost:8000/")

# async def _reverse_proxy(request: Request):
#     url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))
#     rp_req = HTTP_SERVER.build_request(
#         request.method, url, headers=request.headers.raw, content=await request.body()
#     )
#     rp_resp = await HTTP_SERVER.send(rp_req, stream=True)
#     return StreamingResponse(
#         rp_resp.aiter_raw(),
#         status_code=rp_resp.status_code,
#         headers=rp_resp.headers,
#         background=BackgroundTask(rp_resp.aclose),
#     )

# app.add_route("/{path:path}", _reverse_proxy, ["GET", "POST"])

# from nogql_api.resolvers import getSystemDataJSON
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(getSystemDataJSON())