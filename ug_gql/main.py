from urllib.request import Request

from fastapi import FastAPI
            
app = FastAPI()

print('All initialization is done')

@app.get('api/ug_gql')
def hello():
    return {'hello': 'world'}
