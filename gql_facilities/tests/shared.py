import sqlalchemy
import sys
import asyncio

# setting path
sys.path.append("../gql_facilities")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_facilities.DBDefinitions import BaseModel
from gql_facilities.DBDefinitions import FacilityModel, FacilityTypeModel
from gql_facilities.DBDefinitions import EventFacilityModel, EventFacilityStateType
from gql_facilities.DBDefinitions import UserModel, GroupModel, EventModel

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


from gql_facilities.DBFeeder import determineFacilityTypes, determineFacilityStateType


def get_demodata():

    facilityTypes = determineFacilityTypes()
    facilityStateTypes = determineFacilityStateType()

    result = {
        "facilityeventstatetypes": [*facilityStateTypes],
        "facilitytypes": [*facilityTypes],
        "facilities": [
            {'id': "66275ffa-a7b3-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
            {'id': "662763a6-a7b3-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
            {'id': "66276464-a7b3-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
            {'id': "662764dc-a7b3-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
            {'id': "6627654a-a7b3-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
            {'id': "662765ae-a7b3-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
            {'id': "66276608-a7b3-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
            {'id': "6627666c-a7b3-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
            {'id': "662766c6-a7b3-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
            {'id': "66276720-a7b3-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},            
        ],
        "events": [
            {'id': "892965ac-a7b3-11ed-b76e-0242ac110002" },
            {'id': "8929694e-a7b3-11ed-b76e-0242ac110002" },
            {'id': "89296a0c-a7b3-11ed-b76e-0242ac110002" },
            {'id': "89296a8e-a7b3-11ed-b76e-0242ac110002" },
            {'id': "89296afc-a7b3-11ed-b76e-0242ac110002" },
        ],
        "facilities_events": [
            {'id': "a236c724-a7b3-11ed-b76e-0242ac110002" },
            {'id': "a236cada-a7b3-11ed-b76e-0242ac110002" },
            {'id': "a236cb98-a7b3-11ed-b76e-0242ac110002" },
            {'id': "a236cc1a-a7b3-11ed-b76e-0242ac110002" },
            {'id': "a236cc7e-a7b3-11ed-b76e-0242ac110002" },
            {'id': "a236ccec-a7b3-11ed-b76e-0242ac110002" },
            {'id': "a236cd50-a7b3-11ed-b76e-0242ac110002" },
            {'id': "a236cdb4-a7b3-11ed-b76e-0242ac110002" },
            {'id': "a236ce18-a7b3-11ed-b76e-0242ac110002" },
            {'id': "a236ce7c-a7b3-11ed-b76e-0242ac110002" },        ]
    }
    return result


async def prepare_demodata(async_session_maker):
    data = get_demodata()

    from uoishelpers.feeders import ImportModels

    await ImportModels(
        async_session_maker,
        [
            UserModel, GroupModel, EventModel,
            FacilityModel, FacilityTypeModel,
            EventFacilityModel, EventFacilityStateType,            
        ],
        data,
    )


from gql_facilities.Dataloaders import createLoaders_3


async def createContext(asyncSessionMaker):
    return {
        "asyncSessionMaker": asyncSessionMaker,
        "all": await createLoaders_3(asyncSessionMaker),
    }
