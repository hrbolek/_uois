import sqlalchemy
import sys
import asyncio

# setting path
sys.path.append("../gql_granting")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_granting.DBDefinitions import BaseModel
from gql_granting.DBDefinitions import ProgramModel, ProgramLevelTypeModel, ProgramFormTypeModel, ProgramLanguageTypeModel, ProgramTitleTypeModel, ProgramTypeModel
from gql_granting.DBDefinitions import SemesterModel, SubjectModel, TopicModel, LessonModel, LessonTypeModel
from gql_granting.DBDefinitions import ClassificationLevelModel, ClassificationModel, ClassificationTypeModel

from shared import prepare_demodata, prepare_in_memory_sqllite, get_demodata


@pytest.mark.asyncio
async def test_table_users_feed():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()


from gql_granting.DBDefinitions import ComposeConnectionString


def test_connection_string():
    connectionString = ComposeConnectionString()

    assert "://" in connectionString
    assert "@" in connectionString


from gql_granting.DBDefinitions import UUIDColumn


def test_connection_uuidcolumn():
    col = UUIDColumn(name="name")

    assert col is not None


from gql_granting.DBDefinitions import startEngine


@pytest.mark.asyncio
async def test_table_start_engine():
    connectionString = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(
        connectionString, makeDrop=True, makeUp=True
    )

    assert async_session_maker is not None
