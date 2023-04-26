import sqlalchemy
import sys
import asyncio

# setting path
sys.path.append("../gql_forms")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_forms.DBDefinitions import BaseModel
from gql_forms.DBDefinitions import FormModel, FormTypeModel, FormCategoryModel
from gql_forms.DBDefinitions import SectionModel, PartModel
from gql_forms.DBDefinitions import ItemModel, ItemTypeModel, ItemCategoryModel
from gql_forms.DBDefinitions import RequestModel, HistoryModel

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

from gql_forms.DBFeeder import get_demodata

async def prepare_demodata(async_session_maker):
    data = get_demodata()

    from uoishelpers.feeders import ImportModels

    await ImportModels(
        async_session_maker,
        [
            FormModel, FormTypeModel, FormCategoryModel,
            SectionModel, PartModel, 
            ItemModel, ItemTypeModel, ItemCategoryModel,
            RequestModel, HistoryModel
        ],
        data,
    )


from gql_forms.Dataloaders import createLoaders_3, createLoaders


async def createContext(asyncSessionMaker):
    return {
        "asyncSessionMaker": asyncSessionMaker,
        "all": await createLoaders(asyncSessionMaker),
    }
