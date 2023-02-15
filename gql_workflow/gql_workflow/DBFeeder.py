from doctest import master
from functools import cache
from gql_workflow.DBDefinitions import BaseModel, UserModel, GroupModel, RoleTypeModel

from functools import cache


from sqlalchemy.future import select


def get_demodata(asyncSessionMaker):
    pass

async def randomWorkflowData(session):
    workflow = {
        "name": "another workflow",
        "states": [
            {
                "_id": 0,
                "name": "Student",
                "permisions": [],
                "_id": 1,
                "name": "VK",
                "permisions": [{"roletype": "VK", "level": 2}],
                "_id": 2,
                "name": "Proděkan",
                "permisions": [
                    {"roletype": "PdS", "level": 2},
                    {"roletype": "VK", "level": 1},
                ],
                "_id": 3,
                "name": "Děkan",
                "permisions": [
                    {"roletype": "Děkan", "level": 2},
                    {"roletype": "VK", "level": 1},
                    {"roletype": "PdS", "level": 1},
                ],
                "_id": 4,
                "name": "Student",
                "permisions": [{"roletype": "-1", "level": 2}],
                "_id": 5,
                "name": "Archiv",
                "permisions": [
                    {"roletype": "VK", "level": 1},
                    {"roletype": "Děkan", "level": 1},
                    {"roletype": "PdS", "level": 1},
                ],
            }
        ],
        "transitions": [
            {"_id": 0, "name": "Podat", "source": 0, "destination": 1},
            {"_id": 1, "name": "Vrátit", "source": 1, "destination": 0},
            {"_id": 2, "name": "Doporučit", "source": 1, "destination": 2},
            {"_id": 3, "name": "Vrátit", "source": 2, "destination": 1},
            {"_id": 4, "name": "Doporučit", "source": 2, "destination": 3},
            {"_id": 5, "name": "Vrátit", "source": 3, "destination": 2},
            {"_id": 6, "name": "Schválit", "source": 3, "destination": 4},
            {"_id": 7, "name": "Archivovat", "source": 4, "destination": 4},
        ],
    }

    roleTypes = await getRoleTypesFromDb()
    usersToAdd = []
    async with session.begin():
        session.add_all(usersToAdd)
    await session.commit()
    return None
