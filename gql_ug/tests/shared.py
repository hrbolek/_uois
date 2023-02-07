import sqlalchemy
import sys
import asyncio

# setting path
sys.path.append("../gql_ug")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_ug.DBDefinitions import BaseModel
from gql_ug.DBDefinitions import RoleTypeModel, RoleModel
from gql_ug.DBDefinitions import UserModel, GroupModel, GroupTypeModel, MembershipModel


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


from gql_ug.DBFeeder import determineRoleTypes, determineGroupTypes


def get_demodata():

    roleTypes = determineRoleTypes()
    groupTypes = determineGroupTypes()

    result = {
        # 'roletypes': [
        #     {'name': 'rektor', 'name_en': 'rector', 'id': 'ae3f0d74-6159-11ed-b753-0242ac120003'},
        #     {'name': 'prorektor', 'name_en': 'vicerector', 'id': 'ae3f2886-6159-11ed-b753-0242ac120003'},
        #     {'name': 'děkan', 'name_en': 'dean', 'id': 'ae3f2912-6159-11ed-b753-0242ac120003'},
        #     {'name': 'proděkan', 'name_en': 'vicedean', 'id': 'ae3f2980-6159-11ed-b753-0242ac120003'},
        #     {'name': 'vedoucí katedry', 'name_en': 'head of department', 'id': 'ae3f29ee-6159-11ed-b753-0242ac120003'},
        # ],
        # 'grouptypes': [
        #     {"name": "univerzita", "name_en": "university", "ex_type": "100", "id": "cd49e152-610c-11ed-9f29-001a7dda7110"},
        #     {"name": "fakulta", "name_en": "faculty", "ex_type": "300", "id": "cd49e153-610c-11ed-bf19-001a7dda7110"},
        #     {"name": "katedra", "name_en": "department", "ex_type": "500", "id": "cd49e155-610c-11ed-844e-001a7dda7110"},
        #     {"name": "studijní skupina", "name_en": "study group", "ex_type": "001", "id": "cd49e157-610c-11ed-9312-001a7dda7110"},
        # ],
        "roletypes": [*roleTypes],
        "grouptypes": [*groupTypes],
        "users": [
            {
                "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
                "name": "John",
                "surname": "Newbie",
                "email": "john.newbie@world.com",
            },
            {
                "id": "2d9dc868-a4a2-11ed-b9df-0242ac120003",
                "name": "Julia",
                "surname": "Newbie",
                "email": "julia.newbie@world.com",
            },
            {
                "id": "2d9dc9a8-a4a2-11ed-b9df-0242ac120003",
                "name": "Johnson",
                "surname": "Newbie",
                "email": "johnson.newbie@world.com",
            },
            {
                "id": "2d9dcbec-a4a2-11ed-b9df-0242ac120003",
                "name": "Jepeto",
                "surname": "Newbie",
                "email": "jepeto.newbie@world.com",
            },
        ],
        "groups": [
            {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni",
                "grouptype_id": "cd49e152-610c-11ed-9f29-001a7dda7110",
                "mastergroup_id": None,
            },
            {
                "id": "2d9dced0-a4a2-11ed-b9df-0242ac120003",
                "name": "Fac",
                "grouptype_id": "cd49e153-610c-11ed-bf19-001a7dda7110",
                "mastergroup_id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
            },
            {
                "id": "2d9dd1c8-a4a2-11ed-b9df-0242ac120003",
                "name": "Dep",
                "grouptype_id": "cd49e155-610c-11ed-844e-001a7dda7110",
                "mastergroup_id": "2d9dced0-a4a2-11ed-b9df-0242ac120003",
            },
            {
                "id": "2d9dd2ea-a4a2-11ed-b9df-0242ac120003",
                "name": "St",
                "grouptype_id": "cd49e157-610c-11ed-9312-001a7dda7110",
                "mastergroup_id": "2d9dced0-a4a2-11ed-b9df-0242ac120003",
            },
        ],
        "memberships": [
            {
                "id": "7cea8596-a4a2-11ed-b9df-0242ac120003",
                "user_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
                "group_id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
            }
        ],
        "roles": [
            {
                "id": "7cea8802-a4a2-11ed-b9df-0242ac120003",
                "user_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
                "group_id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "roletype_id": "ae3f0d74-6159-11ed-b753-0242ac120003",
            }
        ],
    }
    return result


# 7cea8a96-a4a2-11ed-b9df-0242ac120003
# 7cea8bcc-a4a2-11ed-b9df-0242ac120003
# 7cea8cee-a4a2-11ed-b9df-0242ac120003
# 7cea8e24-a4a2-11ed-b9df-0242ac120003
# 7cea9158-a4a2-11ed-b9df-0242ac120003
# 7cea92b6-a4a2-11ed-b9df-0242ac120003
# 7cea93ce-a4a2-11ed-b9df-0242ac120003
# 7cea9504-a4a2-11ed-b9df-0242ac120003


async def prepare_demodata(async_session_maker):
    data = get_demodata()

    from uoishelpers.feeders import ImportModels

    await ImportModels(
        async_session_maker,
        [
            UserModel,
            GroupModel,
            GroupTypeModel,
            MembershipModel,
            RoleModel,
            RoleTypeModel,
        ],
        data,
    )


from gql_ug.Dataloaders import createLoaders_3


async def createContext(asyncSessionMaker):
    return {
        "asyncSessionMaker": asyncSessionMaker,
        "all": await createLoaders_3(asyncSessionMaker),
    }
