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

from gql_granting.DBFeeder import get_demodata

async def prepare_demodata(async_session_maker):
    data = get_demodata()

    from uoishelpers.feeders import ImportModels

    await ImportModels(
        async_session_maker,
        [           
            ProgramModel, ProgramLevelTypeModel, ProgramFormTypeModel, ProgramLanguageTypeModel, ProgramTitleTypeModel, ProgramTypeModel,
            SemesterModel, SubjectModel, TopicModel, LessonModel, LessonTypeModel,
            ClassificationLevelModel, ClassificationModel, ClassificationTypeModel        
        ],
        data,
    )


from gql_granting.Dataloaders import createLoaders_3, createLoaders


async def createContext(asyncSessionMaker):
    return {
        "asyncSessionMaker": asyncSessionMaker,
        "all": await createLoaders(asyncSessionMaker),
    }
