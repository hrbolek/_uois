from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.exceptions import HTTPException
import os
from fastapi.responses import JSONResponse

#app = FastAPI(root_path="/apif")
app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(content={'detail': str(exc.detail), 'status_code': exc.status_code, 'app': 'frontend'})

@app.get("/ui/{file_path:path}")
async def read_file(file_path: str):
    print(f'query for /ui/{file_path}')
    if os.path.isfile(f'./js/{file_path}'):
        return FileResponse(f'./js/{file_path}')
    else:
        return FileResponse(f'./js/index.html')

#app.mount("/ui", StaticFiles(directory="js"), name="static")

#subapp = FastAPI()
@app.get("/msg")
async def apif_read_item(item_id: int):
    
    return {"hello": "world"}
#app.mount('/api', subapp)
