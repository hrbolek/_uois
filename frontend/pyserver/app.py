from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from mockoauthserver import server as OAuthServer
#app = FastAPI(root_path="/apif")
app = FastAPI()


@app.get("/ui/msg")
async def apif_read_item(item_id: int):
    return {"hello": "world"}

@app.get("/ui/{file_path:path}")
async def read_file(file_path: str):
    print(file_path)
    if os.path.isfile(f'./js/{file_path}'):
        return FileResponse(f'./js/{file_path}')
    else:
        return FileResponse(f'./js/index.html')

#app.mount("/ui", StaticFiles(directory="js"), name="static")

#subapp = FastAPI()
#app.mount('/api', subapp)

app.mount('/oauth', OAuthServer.createServer())
