import datetime
from functools import cache

# from gql_workflow.DBDefinitions import BaseModel, UserModel, GroupModel, RoleTypeModel
# import the base model, when appolo sever ask your container for the first time, gql will ask
# next step define some resolver, how to use resolver in the file graptype
# check all data strcture in database if it have -- (work)
from gql_forms.DBDefinitions import (
    FormCategoryModel,
    FormTypeModel,
    ItemTypeModel,
    ItemCategoryModel,
    FormModel,
    HistoryModel,
    RequestModel,
    SectionModel,
    PartModel,
    ItemModel,
)
import random
import itertools
from functools import cache


from sqlalchemy.future import select

###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################

def get_demodata():
    result = {
        "users": [
            {'id': "a79ee8ce-b085-11ed-9bd8-0242ac110002"}
        ],
        "formtypes": [
            {'id': "2e1140f4-afb0-11ed-9bd8-0242ac110002", 'category_id': '37675bd4-afb0-11ed-9bd8-0242ac110002', 'name': 'Žádost', 'name_en': ''},
            {'id': "2e113e88-afb0-11ed-9bd8-0242ac110002", 'category_id': '37675fe4-afb0-11ed-9bd8-0242ac110002', 'name': 'Zadání DP', 'name_en': ''},
        ],
        "formcategories": [
            {'id': "37675bd4-afb0-11ed-9bd8-0242ac110002", 'name': 'Studentské žádosti', 'name_en': ''},
            {'id': "37675fe4-afb0-11ed-9bd8-0242ac110002", 'name': 'Ostatní', 'name_en': ''},
        ],

        "formrequests": [
            {'id': "13181566-afb0-11ed-9bd8-0242ac110002", 
                'type_id': '2e1140f4-afb0-11ed-9bd8-0242ac110002',
                'createdby': 'a79ee8ce-b085-11ed-9bd8-0242ac110002',
                'lastchange': datetime.datetime.now(),
                'name': 'Žádost o přerušení studia', 'name_en': ''},
        ],

        "forms": [
            {'id': "190d578c-afb1-11ed-9bd8-0242ac110002", 
                "type_id": "2e1140f4-afb0-11ed-9bd8-0242ac110002",
                "name": "Žádost", "name_en": "" },
            {'id': "190d5a7a-afb1-11ed-9bd8-0242ac110002", 
                "type_id": "2e1140f4-afb0-11ed-9bd8-0242ac110002",
                "name": "Žádost", "name_en": "" },
        ],
        "formsections": [
            {'id': "48bbc7d4-afb1-11ed-9bd8-0242ac110002", 
                'form_id': '190d578c-afb1-11ed-9bd8-0242ac110002', 
                'lastchange': datetime.datetime.now(),
                'order': 1, 'name': 'Student' },
            {'id': "48bbca18-afb1-11ed-9bd8-0242ac110002", 
                'form_id': '190d578c-afb1-11ed-9bd8-0242ac110002', 
                'lastchange': datetime.datetime.now(),
                'order': 2, 'name': 'Znění' },
            {'id': "48bbca9a-afb1-11ed-9bd8-0242ac110002", 
                'form_id': '190d5a7a-afb1-11ed-9bd8-0242ac110002', 
                'lastchange': datetime.datetime.now(),
                'order': 1, 'name': 'Student' },
            {'id': "48bbcaea-afb1-11ed-9bd8-0242ac110002", 
                'form_id': '190d5a7a-afb1-11ed-9bd8-0242ac110002', 
                'lastchange': datetime.datetime.now(),
                'order': 2, 'name': 'Znění' },
        ],
        "formparts": [
            {'id': "52e3ee26-afb1-11ed-9bd8-0242ac110002", 
                "section_id": '48bbc7d4-afb1-11ed-9bd8-0242ac110002', 
                'lastchange': datetime.datetime.now(),
                'order': 1, 'name': 'Identifikace' },
            {'id': "52e3f22c-afb1-11ed-9bd8-0242ac110002", 
                "section_id": '48bbca18-afb1-11ed-9bd8-0242ac110002', 
                'lastchange': datetime.datetime.now(),
                'order': 1, 'name': 'Znění' },
            {'id': "52e3f2d6-afb1-11ed-9bd8-0242ac110002", 
                "section_id": '48bbca9a-afb1-11ed-9bd8-0242ac110002', 
                'lastchange': datetime.datetime.now(),
                'order': 1, 'name': 'Identifikace' },
            {'id': "52e3f344-afb1-11ed-9bd8-0242ac110002", 
                "section_id": '48bbcaea-afb1-11ed-9bd8-0242ac110002', 
                'lastchange': datetime.datetime.now(),
                'order': 1, 'name': 'Znění' },
        ],
        "formitems": [
            {'id': "72a3d4b0-afb1-11ed-9bd8-0242ac110002", 
                'part_id': '52e3ee26-afb1-11ed-9bd8-0242ac110002',
                'type_id': '9bdb916a-afb6-11ed-9bd8-0242ac110002',
                'lastchange': datetime.datetime.now(),
                'order': 1, 'name': 'user_id', 'value': '45678' },
            {'id': "72a3d7b2-afb1-11ed-9bd8-0242ac110002", 
                'part_id': '52e3f22c-afb1-11ed-9bd8-0242ac110002', 
                'type_id': '9bdb9426-afb6-11ed-9bd8-0242ac110002',
                'lastchange': datetime.datetime.now(),
                'order': 1, 'name': 'Znění', 'value': 'Žádám o ...' },
            {'id': "72a3d85c-afb1-11ed-9bd8-0242ac110002", 
                'part_id': '52e3f2d6-afb1-11ed-9bd8-0242ac110002', 
                'type_id': '9bdb916a-afb6-11ed-9bd8-0242ac110002',
                'lastchange': datetime.datetime.now(),
                'order': 1, 'name': 'user_id', 'value': '45678' },
            {'id': "72a3d8de-afb1-11ed-9bd8-0242ac110002", 
                'part_id': '52e3f344-afb1-11ed-9bd8-0242ac110002', 
                'type_id': '9bdb9426-afb6-11ed-9bd8-0242ac110002',
                'lastchange': datetime.datetime.now(),
                'order': 1, 'name': 'Znění', 'value': 'Žádám o ...' },
        ],

        "formitemtypes": [
            {'id': "9bdb916a-afb6-11ed-9bd8-0242ac110002", 
                "category_id": "b1cb0f80-afb8-11ed-9bd8-0242ac110002",
                "name": 'student', 'query': '', 'selector': '' },
            {'id': "9bdb93a4-afb6-11ed-9bd8-0242ac110002", 
                "category_id": "b1cb0f80-afb8-11ed-9bd8-0242ac110002",
                "name": 'program', 'query': '', 'selector': '' },
            {'id': "9bdb9426-afb6-11ed-9bd8-0242ac110002", 
                "category_id": "b1cb1462-afb8-11ed-9bd8-0242ac110002",
               "name": 'obsah', 'query': '', 'selector': '' },
            {'id': "9bdb9476-afb6-11ed-9bd8-0242ac110002", 
                "category_id": "b1cb1462-afb8-11ed-9bd8-0242ac110002",
                "name": 'doporučení', 'query': '', 'selector': '' },
        ],

        "formitemcategories": [
            {'id': "b1cb0f80-afb8-11ed-9bd8-0242ac110002" , 'name': 'GQL_API', 'name_en': ''},
            {'id': "b1cb1462-afb8-11ed-9bd8-0242ac110002" , 'name': 'Text', 'name_en': ''},
        ],

        "formhistories": [
            {'id': "84c35266-afb5-11ed-9bd8-0242ac110002", 
                'request_id': '13181566-afb0-11ed-9bd8-0242ac110002', 
                'form_id': '190d578c-afb1-11ed-9bd8-0242ac110002',
                'lastchange': datetime.datetime.now(),
                'name': '' },
            {'id': "84c35504-afb5-11ed-9bd8-0242ac110002", 
                'request_id': '13181566-afb0-11ed-9bd8-0242ac110002', 
                'form_id': '190d5a7a-afb1-11ed-9bd8-0242ac110002',
                'lastchange': datetime.datetime.now(),
                'name': '' },
        ]
    }
    return result

import os
import json
from uoishelpers.feeders import ImportModels
import datetime

def get_demodata():
    def datetime_parser(json_dict):
        for (key, value) in json_dict.items():
            if key in ["startdate", "enddate", "lastchange", "created"]:
                dateValue = datetime.datetime.fromisoformat(value)
                dateValueWOtzinfo = dateValue.replace(tzinfo=None)
                json_dict[key] = dateValueWOtzinfo
        return json_dict


    with open("./systemdata.json", "r") as f:
        jsonData = json.load(f, object_hook=datetime_parser)

    return jsonData

async def initDB(asyncSessionMaker):

    defaultNoDemo = "False"
    if defaultNoDemo == os.environ.get("DEMO", defaultNoDemo):
        dbModels = [
            FormCategoryModel,
            FormTypeModel,
            ItemTypeModel,
            ItemCategoryModel,
            ItemTypeModel
            ]
    else:
        dbModels = [
            FormCategoryModel,
            FormTypeModel,
            ItemCategoryModel,
            ItemTypeModel,
            FormModel,
            RequestModel,
            HistoryModel,
            SectionModel,
            PartModel,
            ItemModel
        ]
        
    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass