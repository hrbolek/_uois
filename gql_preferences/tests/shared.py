import sqlalchemy
import asyncio
import pytest

# from ..uoishelpers.uuid import UUIDColumn
from gql_preferences.DBDefinitions import(
    BaseModel,
    TagModel,
    TagEntityModel
    )

async def prepare_in_memory_sqllite():
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker

    asyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # asyncEngine = create_async_engine("sqlite+aiosqlite:///data.sqlite")
    async with asyncEngine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async_session_maker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker

from gql_preferences.dbfeeder import get_demodata

async def prepare_demodata(async_session_maker):

    data = get_demodata()

    from gql_preferences.dbfeeder import ImportModels

    await ImportModels(
        async_session_maker,
        [
            TagModel,
            TagEntityModel
        ],
        data,
    )


from gql_preferences.dataloaders import createDataLoders

async def createContext(asyncSessionMaker):
    return {
        "asyncSessionMaker": asyncSessionMaker,
        "all": await createDataLoders(asyncSessionMaker),
        "user": {"id": "f8089aa6-2c4a-4746-9503-105fcc5d054c"}
    }


def createGQLClient():

    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    import main

    main.connectionString = "sqlite+aiosqlite:///:memory:"

    client = TestClient(main.app)
    print(main.connectionString, flush=True)
    return client
