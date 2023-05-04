import sqlalchemy
import sys
import asyncio

# setting path

#sys.path.append("../gql_surveys")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_surveys.DBDefinitions import BaseModel
from gql_surveys.DBDefinitions import AnswerModel, SurveyModel, SurveyTypeModel, QuestionModel, QuestionTypeModel, QuestionValueModel

from tests.shared import prepare_demodata, prepare_in_memory_sqllite, get_demodata


@pytest.mark.asyncio
async def test_table_users_feed():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()


from gql_surveys.DBDefinitions import ComposeConnectionString


def test_connection_string():
    connectionString = ComposeConnectionString()

    assert "://" in connectionString
    assert "@" in connectionString


from gql_surveys.DBDefinitions import UUIDColumn


def test_connection_uuidcolumn():
    col = UUIDColumn(name="name")

    assert col is not None


from gql_surveys.DBDefinitions import startEngine


@pytest.mark.asyncio
async def test_table_start_engine():
    connectionString = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(
        connectionString, makeDrop=True, makeUp=True
    )

    assert async_session_maker is not None

from sqlalchemy.future import select

def createRowTest(tableName, DBModel):
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()
        assert data.get(tableName, None) is not None
        datatable = data[tableName]
        assert len(datatable) > 0

        for row in datatable:
            async with async_session_maker() as session:
                statement = select(DBModel).filter_by(id=row["id"])
                result = await session.execute(statement)
                rows = result.scalars()
                rows = [item for item in rows]
                assert len(rows) == 1
                firstrow = rows[0]
                assert firstrow.id == row["id"]
    return result_test

test_answers_rows = createRowTest("surveyanswers", AnswerModel)
test_survey_rows = createRowTest("surveys", SurveyModel)