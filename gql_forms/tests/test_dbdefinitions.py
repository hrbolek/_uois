import sqlalchemy
import sys
import asyncio

# setting path
sys.path.append("../gql_forms")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_forms.DBDefinitions import BaseModel
from gql_forms.DBDefinitions import FormModel, FormTypeModel, FormCategoryModel
from gql_forms.DBDefinitions import SectionModel, PartModel, ItemModel
from gql_forms.DBDefinitions import RequestModel, HistoryModel

from shared import prepare_demodata, prepare_in_memory_sqllite, get_demodata


@pytest.mark.asyncio
async def test_table_users_feed():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()


from gql_forms.DBDefinitions import ComposeConnectionString


def test_connection_string():
    connectionString = ComposeConnectionString()

    assert "://" in connectionString
    assert "@" in connectionString


from gql_forms.DBDefinitions import UUIDColumn


def test_connection_uuidcolumn():
    col = UUIDColumn(name="name")

    assert col is not None


from gql_forms.DBDefinitions import startEngine


@pytest.mark.asyncio
async def test_table_start_engine():
    connectionString = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(
        connectionString, makeDrop=True, makeUp=True
    )

    assert async_session_maker is not None
