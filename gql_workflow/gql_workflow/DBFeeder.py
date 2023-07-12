from functools import cache

from gql_workflow.DBDefinitions import (
    AuthorizationModel,
    AuthorizationGroupModel,
    AuthorizationRoleTypeModel,
    AuthorizationUserModel,
    WorkflowModel,
    WorkflowStateModel,
    WorkflowStateRoleTypeModel,
    WorkflowStateUserModel,
    WorkflowTransitionModel
)

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


    data = {
        'awauthorizations': [
            {'id': 'e0ca6b6c-e962-4944-88d6-fb85e98572de'},
        ],
        'awauthorizationusers': [
            {
                'id': 'c84ce88c-690c-4ff3-990c-9d4c01e847c1',
                'authorization_id': 'e0ca6b6c-e962-4944-88d6-fb85e98572de',
                'user_id': '',

                'accesslevel': 1
            },
        ],
        'awauthorizationgroups': [
            {
                'id': '829e3687-2cfa-4961-ad45-68f26e3bc3d8',
                'authorization_id': 'e0ca6b6c-e962-4944-88d6-fb85e98572de',
                'group_id': '',

                'accesslevel': 1
            },            
        ],
        'awauthorizationroletypes': [
            {
                'id': '8eeb8bee-a54e-4514-bddd-941c1a1f17e8',
                'authorization_id': 'e0ca6b6c-e962-4944-88d6-fb85e98572de',
                'group_id': '',
                'roletype_id': '',

                'accesslevel': 1
            },
        ],


    }
    #roleTypes = await getRoleTypesFromDb()
    usersToAdd = []
    async with session.begin():
        session.add_all(usersToAdd)
    await session.commit()
    return None





import os
import json
from uoishelpers.feeders import ImportModels
import datetime

def get_demodata():
    def datetime_parser(json_dict):
        for (key, value) in json_dict.items():
            if key in ["startdate", "enddate", "lastchange", "created"]:
                if value is None:
                    dateValueWOtzinfo = None
                else:
                    try:
                        dateValue = datetime.datetime.fromisoformat(value)
                        dateValueWOtzinfo = dateValue.replace(tzinfo=None)
                    except:
                        print("jsonconvert Error", key, value, flush=True)
                        dateValueWOtzinfo = None
                
                json_dict[key] = dateValueWOtzinfo
        return json_dict


    with open("./systemdata.json", "r") as f:
        jsonData = json.load(f, object_hook=datetime_parser)

    return jsonData

async def initDB(asyncSessionMaker):

    defaultNoDemo = "False"
    if defaultNoDemo == os.environ.get("DEMO", defaultNoDemo):
        dbModels = [
            
        ]
    else:
        dbModels = [
            AuthorizationModel,
            AuthorizationGroupModel,
            AuthorizationRoleTypeModel,
            AuthorizationUserModel,
            WorkflowModel,
            WorkflowStateModel,
            WorkflowStateRoleTypeModel,
            WorkflowStateUserModel,
            WorkflowTransitionModel
        ]

    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass