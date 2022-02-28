from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(content={'detail': str(exc.detail), 'status_code': exc.status_code, 'app': 'backend'})

@app.get('/api/')
async def sayHello(request: Request):
    return {'hello': 'World'}

@app.post('/gql')
async def getBuildingData(request: Request):
    return {
        'id' : 789,
        'name' : 'KŠ/9A',
        'rooms' : [
            {'id': 789, 'name': 'KŠ/9A/586'}
        ],
        'areal' : {'id' : 789, 'name': 'KŠ'},
        'user' : {'id' : 789, 'name': 'John', 'surname': 'Nowick'}
    }