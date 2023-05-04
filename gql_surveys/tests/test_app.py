import sqlalchemy
import sys
import asyncio

from fastapi import FastAPI
from fastapi.testclient import TestClient
import main

main.connectionString = "sqlite+aiosqlite:///:memory:"
client = TestClient(main.app)
print(main.connectionString, flush=True)

def test_app():

    query = """
        query {
            surveyPage {
                    id
                    name
            }
        }
    """

    response = client.post("/gql", json={"query": query})
    assert response.status_code == 200
    
    jsonData = response.json()
    print(jsonData, flush=True)
    assert jsonData.get('errors', None) is None
    