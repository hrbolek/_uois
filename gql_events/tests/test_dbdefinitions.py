import sqlalchemy
import sys
import asyncio

# setting path
sys.path.append("../gql_events")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_events.DBDefinitions import BaseModel
from gql_events.DBDefinitions import EventModel, EventTypeModel, EventGroupModel
from gql_events.DBDefinitions import PresenceModel, PresenceTypeModel, InvitationTypeModel

from sqlalchemy.future import select

from shared import prepare_demodata, prepare_in_memory_sqllite, get_demodata


@pytest.mark.asyncio
async def test_load_demo_data():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    #data = get_demodata()

    


from gql_events.DBDefinitions import ComposeConnectionString


def test_connection_string():
    connectionString = ComposeConnectionString()

    assert "://" in connectionString
    assert "@" in connectionString


from gql_events.DBDefinitions import UUIDColumn


def test_connection_uuidcolumn():
    col = UUIDColumn(name="name")

    assert col is not None


from gql_events.DBDefinitions import startEngine


@pytest.mark.asyncio
async def test_table_start_engine():
    connectionString = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(
        connectionString, makeDrop=True, makeUp=True
    )

    assert async_session_maker is not None


