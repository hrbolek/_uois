from functools import cache

from gql_facilities.DBDefinitions import (
    FacilityTypeModel,
    FacilityModel,
    EventFacilityStateType,
    EventFacilityModel
)

import random
import itertools
from sqlalchemy.future import select


def singleCall(asyncFunc):
    """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
    Dekorovana funkce je asynchronni.
    """
    resultCache = {}

    async def result():
        if resultCache.get("result", None) is None:
            resultCache["result"] = await asyncFunc()
        return resultCache["result"]

    return result


###########################################################################################################################
#
# zde definujte sva systemova data
#
###########################################################################################################################


@cache
def types1():
    # krome id a name, lze mit i dalsi prvky, napriklad cizi klice...
    data = [
        {"id": "282e67ec-6d9e-11ed-a1eb-0242ac120002", "name": "typeA"},
        {"id": "282e6e86-6d9e-11ed-a1eb-0242ac120002", "name": "typeB"},
        {"id": "282e7002-6d9e-11ed-a1eb-0242ac120002", "name": "typeC"},
    ]
    return data


@cache
def determineFacilityTypes():
    """Definuje zakladni typy facility a udrzuje je v pameti (campus/building/floor/room)"""
    facilityTypes = [
        {"name": "campus", "id": ""},
        {"name": "building", "id": ""},
        {"name": "floor", "id": ""},
        {"name": "room", "id": ""},
    ]
    return facilityTypes


# generovvat id podobné uuid

##vymyslet struct která doplni id podle typu facility


def randomFacility(name):
    """Genreruje strukturu facility a jejich hlavního fukcionáře ve formě JSON"""
    result = {
        "name": f"{name}",
        "adress": "RandAdress" + str(random.randint(1, 10)),
        "valid": "True",
    }


###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################

import asyncio


def systemStructures():
    result = {
        'facilitytypes': determineFacilityTypes(),
        # [
        #     {'id': "764217ee-a7a0-11ed-b76e-0242ac110002" , 'name': 'areál', 'name_en': ''},
        #     {'id': "76421cf8-a7a0-11ed-b76e-0242ac110002" , 'name': 'budova', 'name_en': ''},
        #     {'id': "76421e10-a7a0-11ed-b76e-0242ac110002" , 'name': 'patro', 'name_en': ''},
        #     {'id': "76421ee2-a7a0-11ed-b76e-0242ac110002" , 'name': 'skupina místností', 'name_en': ''},
        #     {'id': "76421faa-a7a0-11ed-b76e-0242ac110002" , 'name': 'učebna', 'name_en': ''},
        #     {'id': "7642209a-a7a0-11ed-b76e-0242ac110002" , 'name': 'laboratoř', 'name_en': ''},            
        # ],
        'facilityeventstatetypes': determineFacilityStateType(),
        # 'facilityeventstatetypes': [
        #     {'id': "ba53d10c-a7a0-11ed-b76e-0242ac110002" , 'name': 'rozvrh', 'name_en': ''},
        #     {'id': "ba53d4c2-a7a0-11ed-b76e-0242ac110002" , 'name': 'plán', 'name_en': ''},
        #     {'id': "ba53d580-a7a0-11ed-b76e-0242ac110002" , 'name': 'požádáno', 'name_en': ''},
        #     {'id': "ba53d5f8-a7a0-11ed-b76e-0242ac110002" , 'name': 'schváleno', 'name_en': ''},
        #     {'id': "ba53d65c-a7a0-11ed-b76e-0242ac110002" , 'name': 'zrušeno', 'name_en': ''},
        #     {'id': "ba53d6b6-a7a0-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
        #     {'id': "ba53d71a-a7a0-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
        # ]
    }
    return result


def get_demodata():
    sys = systemStructures()
    result = {**sys,
        "facilities": [
            {'id': "662764dc-a7b3-11ed-b76e-0242ac110002" , 'name': 'Místnost 101', 'name_en': '', 
                'facilitytype_id': "76421faa-a7a0-11ed-b76e-0242ac110002",
                'master_facility_id': '66276464-a7b3-11ed-b76e-0242ac110002',
                'group_id': '480f2802-a869-11ed-924c-0242ac110002'},
            {'id': "66275ffa-a7b3-11ed-b76e-0242ac110002" , 'name': 'Hlavní komplex', 'name_en': '', 
                'facilitytype_id': "764217ee-a7a0-11ed-b76e-0242ac110002",
                'master_facility_id': None,
                'group_id': '480f2802-a869-11ed-924c-0242ac110002'},
            {'id': "662763a6-a7b3-11ed-b76e-0242ac110002" , 'name': 'Budova A', 'name_en': '', 
                'facilitytype_id': "76421cf8-a7a0-11ed-b76e-0242ac110002",
                'master_facility_id': '66275ffa-a7b3-11ed-b76e-0242ac110002',
                'group_id': None},
            {'id': "66276464-a7b3-11ed-b76e-0242ac110002" , 'name': 'Patro 1', 'name_en': '', 
                'facilitytype_id': "76421e10-a7a0-11ed-b76e-0242ac110002",
                'master_facility_id': '662763a6-a7b3-11ed-b76e-0242ac110002',
                'group_id': '480f2802-a869-11ed-924c-0242ac110002'},
            {'id': "6627654a-a7b3-11ed-b76e-0242ac110002" , 'name': 'Místnost 102', 'name_en': '', 
                'facilitytype_id': "76421faa-a7a0-11ed-b76e-0242ac110002",
                'master_facility_id': '66276464-a7b3-11ed-b76e-0242ac110002',
                'group_id': '480f2802-a869-11ed-924c-0242ac110002'},
            # {'id': "662765ae-a7b3-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
            # {'id': "66276608-a7b3-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
            # {'id': "6627666c-a7b3-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
            # {'id': "662766c6-a7b3-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
            # {'id': "66276720-a7b3-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},            
        ],
        "events": [
            {'id': "0800dd68-a7b6-11ed-b76e-0242ac110002" },
            {'id': "0800e20e-a7b6-11ed-b76e-0242ac110002" },
            {'id': "0800e312-a7b6-11ed-b76e-0242ac110002" },
            {'id': "0800e3c6-a7b6-11ed-b76e-0242ac110002" },
            {'id': "0800e466-a7b6-11ed-b76e-0242ac110002" },
            {'id': "0800e506-a7b6-11ed-b76e-0242ac110002" },
            {'id': "0800e5a6-a7b6-11ed-b76e-0242ac110002" },
            {'id': "0800e696-a7b6-11ed-b76e-0242ac110002" },
            {'id': "0800e790-a7b6-11ed-b76e-0242ac110002" },
            {'id': "0800e88a-a7b6-11ed-b76e-0242ac110002" },
        ],
        "facilities_events": [
            {'id': "a236c724-a7b3-11ed-b76e-0242ac110002",
                'event_id': '0800dd68-a7b6-11ed-b76e-0242ac110002',
                'facility_id': '662764dc-a7b3-11ed-b76e-0242ac110002',
                'state_id': 'ba53d580-a7a0-11ed-b76e-0242ac110002'
             },
            {'id': "a236cada-a7b3-11ed-b76e-0242ac110002",
                'event_id': '0800e20e-a7b6-11ed-b76e-0242ac110002',
                'facility_id': '662764dc-a7b3-11ed-b76e-0242ac110002',
                'state_id': 'ba53d580-a7a0-11ed-b76e-0242ac110002'
              },
            {'id': "a236cb98-a7b3-11ed-b76e-0242ac110002",
                'event_id': '0800e312-a7b6-11ed-b76e-0242ac110002',
                'facility_id': '662764dc-a7b3-11ed-b76e-0242ac110002',
                'state_id': 'ba53d580-a7a0-11ed-b76e-0242ac110002'
              },
            {'id': "a236cc1a-a7b3-11ed-b76e-0242ac110002",
                'event_id': '0800e3c6-a7b6-11ed-b76e-0242ac110002',
                'facility_id': '662764dc-a7b3-11ed-b76e-0242ac110002',
                'state_id': 'ba53d4c2-a7a0-11ed-b76e-0242ac110002'
              },
            {'id': "a236cc7e-a7b3-11ed-b76e-0242ac110002",
                'event_id': '0800e466-a7b6-11ed-b76e-0242ac110002',
                'facility_id': '662764dc-a7b3-11ed-b76e-0242ac110002',
                'state_id': 'ba53d4c2-a7a0-11ed-b76e-0242ac110002'
              },
            {'id': "a236ccec-a7b3-11ed-b76e-0242ac110002",
                'event_id': '0800e506-a7b6-11ed-b76e-0242ac110002',
                'facility_id': '6627654a-a7b3-11ed-b76e-0242ac110002',
                'state_id': 'ba53d4c2-a7a0-11ed-b76e-0242ac110002'
              },
            {'id': "a236cd50-a7b3-11ed-b76e-0242ac110002",
                'event_id': '0800e5a6-a7b6-11ed-b76e-0242ac110002',
                'facility_id': '6627654a-a7b3-11ed-b76e-0242ac110002',
                'state_id': 'ba53d4c2-a7a0-11ed-b76e-0242ac110002'
              },
            {'id': "a236cdb4-a7b3-11ed-b76e-0242ac110002",
                'event_id': '0800e696-a7b6-11ed-b76e-0242ac110002',
                'facility_id': '6627654a-a7b3-11ed-b76e-0242ac110002',
                'state_id': 'ba53d65c-a7a0-11ed-b76e-0242ac110002'
              },
            {'id': "a236ce18-a7b3-11ed-b76e-0242ac110002",
                'event_id': '0800e790-a7b6-11ed-b76e-0242ac110002',
                'facility_id': '6627654a-a7b3-11ed-b76e-0242ac110002',
                'state_id': 'ba53d65c-a7a0-11ed-b76e-0242ac110002'
              },
            {'id': "a236ce7c-a7b3-11ed-b76e-0242ac110002",
                'event_id': '0800e88a-a7b6-11ed-b76e-0242ac110002',
                'facility_id': '6627654a-a7b3-11ed-b76e-0242ac110002',
                'state_id': 'ba53d65c-a7a0-11ed-b76e-0242ac110002'
              },
        ],
        "groups" : [
            {'id': "480f2802-a869-11ed-924c-0242ac110002" },
            {'id': "480f3676-a869-11ed-924c-0242ac110002" },
            {'id': "480f3702-a869-11ed-924c-0242ac110002" },
            {'id': "480f3766-a869-11ed-924c-0242ac110002" },
            {'id': "480f37ac-a869-11ed-924c-0242ac110002" },        
        ],
        # 'facilitymanagementgroups': [
        #     {'id': "749892c8-a869-11ed-924c-0242ac110002", 'facility_id': '66275ffa-a7b3-11ed-b76e-0242ac110002', 'group_id': '480f2802-a869-11ed-924c-0242ac110002' },
        #     {'id': "74989502-a869-11ed-924c-0242ac110002", 'facility_id': '662763a6-a7b3-11ed-b76e-0242ac110002', 'group_id': '480f3676-a869-11ed-924c-0242ac110002' },
        #     {'id': "74989584-a869-11ed-924c-0242ac110002", 'facility_id': '66276464-a7b3-11ed-b76e-0242ac110002', 'group_id': '480f3702-a869-11ed-924c-0242ac110002' },
        #     {'id': "749895de-a869-11ed-924c-0242ac110002", 'facility_id': '662764dc-a7b3-11ed-b76e-0242ac110002', 'group_id': '480f3766-a869-11ed-924c-0242ac110002' },
        #     {'id': "74989624-a869-11ed-924c-0242ac110002", 'facility_id': '6627654a-a7b3-11ed-b76e-0242ac110002', 'group_id': '480f37ac-a869-11ed-924c-0242ac110002' },
        # ]


    }
    return result

def determineFacilityTypes():
    result = [
        {'id': "764217ee-a7a0-11ed-b76e-0242ac110002" , 'name': 'areál', 'name_en': ''},
        {'id': "76421cf8-a7a0-11ed-b76e-0242ac110002" , 'name': 'budova', 'name_en': ''},
        {'id': "76421e10-a7a0-11ed-b76e-0242ac110002" , 'name': 'patro', 'name_en': ''},
        {'id': "76421ee2-a7a0-11ed-b76e-0242ac110002" , 'name': 'skupina místností', 'name_en': ''},
        {'id': "76421faa-a7a0-11ed-b76e-0242ac110002" , 'name': 'učebna', 'name_en': ''},
        {'id': "7642209a-a7a0-11ed-b76e-0242ac110002" , 'name': 'laboratoř', 'name_en': ''},
    ]
    return result

def determineFacilityStateType():
    # rozvrh, naplánováno, žádost, schváleno, zrušeno, ...
    # planned, requested, accepted, canceled, priority0, priority1, ...

    result = [
        {'id': "ba53d10c-a7a0-11ed-b76e-0242ac110002" , 'name': 'rozvrh', 'name_en': ''},
        {'id': "ba53d4c2-a7a0-11ed-b76e-0242ac110002" , 'name': 'plán', 'name_en': ''},
        {'id': "ba53d580-a7a0-11ed-b76e-0242ac110002" , 'name': 'požádáno', 'name_en': ''},
        {'id': "ba53d5f8-a7a0-11ed-b76e-0242ac110002" , 'name': 'schváleno', 'name_en': ''},
        {'id': "ba53d65c-a7a0-11ed-b76e-0242ac110002" , 'name': 'zrušeno', 'name_en': ''},
        {'id': "ba53d6b6-a7a0-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
        {'id': "ba53d71a-a7a0-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
    ]
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
            FacilityTypeModel,
            EventFacilityStateType,
            FacilityModel,
            EventFacilityModel        
            ]
    else:
        dbModels = [
            FacilityTypeModel,
            EventFacilityStateType,
            FacilityModel,
            EventFacilityModel        
        ]

    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass