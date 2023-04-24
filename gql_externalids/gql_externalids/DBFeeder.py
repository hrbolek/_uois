from functools import cache
from gql_externalids.DBDefinitions import (
    ExternalIdTypeModel,
    ExternalIdCategoryModel,
    ExternalIdModel
    )
from sqlalchemy.future import select

def get_demodata():
    result = {
        "externalidtypes": determineExternalIdsTypes(),
        "externalids": [
            {'id': "cd85ef7c-ad44-11ed-9bd8-0242ac110002", "inner_id": "be1b2f34-ad44-11ed-9bd8-0242ac110002", "outer_id": "600", "typeid_id": "1db4ac10-67e8-11ed-9022-0242ac120002" },
            {'id': "cd85f22e-ad44-11ed-9bd8-0242ac110002", "inner_id": "be1b4992-ad44-11ed-9bd8-0242ac110002", "outer_id": "601", "typeid_id": "1db4ac10-67e8-11ed-9022-0242ac120002" },
            {'id': "cd85f2b0-ad44-11ed-9bd8-0242ac110002", "inner_id": "be1b4a28-ad44-11ed-9bd8-0242ac110002", "outer_id": "602", "typeid_id": "1db4ac10-67e8-11ed-9022-0242ac120002" },
            {'id': "cd85f30a-ad44-11ed-9bd8-0242ac110002", "inner_id": "be1b4a82-ad44-11ed-9bd8-0242ac110002", "outer_id": "603", "typeid_id": "1db4ac10-67e8-11ed-9022-0242ac120002" },
            {'id': "cd85f350-ad44-11ed-9bd8-0242ac110002", "inner_id": "be1b4ad2-ad44-11ed-9bd8-0242ac110002", "outer_id": "604", "typeid_id": "1db4ac10-67e8-11ed-9022-0242ac120002" },
            {'id': "cd85f396-ad44-11ed-9bd8-0242ac110002", "inner_id": "be1b4b18-ad44-11ed-9bd8-0242ac110002", "outer_id": "605", "typeid_id": "1db4ac10-67e8-11ed-9022-0242ac120002" },
            {'id': "cd85f3dc-ad44-11ed-9bd8-0242ac110002", "inner_id": "be1b4b68-ad44-11ed-9bd8-0242ac110002", "outer_id": "606", "typeid_id": "1db4ac10-67e8-11ed-9022-0242ac120002" },
            {'id': "cd85f422-ad44-11ed-9bd8-0242ac110002", "inner_id": "be1b4bae-ad44-11ed-9bd8-0242ac110002", "outer_id": "607", "typeid_id": "1db4ac10-67e8-11ed-9022-0242ac120002" },
            {'id': "cd85f468-ad44-11ed-9bd8-0242ac110002", "inner_id": "be1b4c30-ad44-11ed-9bd8-0242ac110002", "outer_id": "608", "typeid_id": "1db4ac10-67e8-11ed-9022-0242ac120002" },
            {'id': "cd85f4a4-ad44-11ed-9bd8-0242ac110002", "inner_id": "44c9722a-ad45-11ed-9bd8-0242ac110002", "outer_id": "609", "typeid_id": "1db4ac10-67e8-11ed-9022-0242ac120002" },


            {'id': "7f747a6a-ee46-4863-a88d-4a5357dd7bbc", "inner_id": "1decba11-4d86-4312-bca0-5e847a414cf9", "outer_id": "610", "typeid_id": "1db4ac10-67e8-11ed-9022-0242ac120002" },
            {'id': "d8897332-b6f0-4e2c-b2d5-4f1040f58425", "inner_id": "c6de02f9-2921-43a8-bff7-087081922225", "outer_id": "611", "typeid_id": "1db4ac10-67e8-11ed-9022-0242ac120002" },
        ],
        "users": [
            {'id': "be1b2f34-ad44-11ed-9bd8-0242ac110002" },
            {'id': "be1b4992-ad44-11ed-9bd8-0242ac110002" },
            {'id': "be1b4a28-ad44-11ed-9bd8-0242ac110002" },
            {'id': "be1b4a82-ad44-11ed-9bd8-0242ac110002" },
            {'id': "be1b4ad2-ad44-11ed-9bd8-0242ac110002" },
            {'id': "be1b4b18-ad44-11ed-9bd8-0242ac110002" },
            {'id': "be1b4b68-ad44-11ed-9bd8-0242ac110002" },
            {'id': "be1b4bae-ad44-11ed-9bd8-0242ac110002" },
            {'id': "44c9722a-ad45-11ed-9bd8-0242ac110002" },
            {'id': "be1b4c30-ad44-11ed-9bd8-0242ac110002" },
        ],
        "groups": [
            {'id': "1decba11-4d86-4312-bca0-5e847a414cf9" },
            {'id': "c6de02f9-2921-43a8-bff7-087081922225" },
        ],
    }
    return result
###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################


@cache
def determineExternalIdsTypes():
    """Definuje zakladni typy externich Id a udrzuje je v pameti.
    Pozor, data se v databazi mohou zmenit! Pouzivat obezretne!
    """

    idTypes = [
        {"name": "UOApl", "id": "1db4ac10-67e8-11ed-9022-0242ac120002"},
        {"name": "VVP", "id": "1db4b020-67e8-11ed-9022-0242ac120002"},
        {"name": "SCOPUS", "id": "1db4b188-67e8-11ed-9022-0242ac120002"},
        {"name": "WoS", "id": "1db4b2be-67e8-11ed-9022-0242ac120002"},
        {"name": "ResearcherId", "id": "1db4b3d6-67e8-11ed-9022-0242ac120002"},
    ]
    return idTypes


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
            ExternalIdTypeModel,
            ExternalIdCategoryModel,
        ]
    else:
        dbModels = [
            ExternalIdTypeModel,
            ExternalIdCategoryModel,
            ExternalIdModel
        ]

    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass