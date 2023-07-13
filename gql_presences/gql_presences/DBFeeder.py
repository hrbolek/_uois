from doctest import master
from functools import cache
from gql_presences.DBDefinitions import (
    ContentModel,
    TaskModel,
)

import random
import itertools
from functools import cache


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
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################


@cache
def determinePresenceTypes():
    """Definuje zakladni typy přítomnosti a udrzuje je v pameti"""
    presenceTypes = [
        {
            "name": "přítomen",
            "name_en": "present",
            "id": "a6ca5364-7abd-11ed-a1eb-0242ac120002",
        },
        # doplnit zbytek UUID
        {
            "name": "absent",
            "name_en": "absent",
            "id": "a6ca574c-7abd-11ed-a1eb-0242ac120002",
        },
        {
            "name": "nemoc",
            "name_en": "sick leave",
            "id": "a6ca5b7a-7abd-11ed-a1eb-0242ac120002",
        },
        {
            "name": "ŘD",
            "name_en": "official leave",
            "id": "a6ca5d0a-7abd-11ed-a1eb-0242ac120002",
        },
        {
            "name": "služba",
            "name_en": "guard duty",
            "id": "a6ca5ee0-7abd-11ed-a1eb-0242ac120002",
        },
        {
            "name": "NV",
            "name_en": "compensatory leave",
            "id": "a6ca6264-7abd-11ed-a1eb-0242ac120002",
        },
    ]
    return presenceTypes


@cache
def determineTasks():
    """Determinuje základní úlohy"""

    tasks = [
        {
            "brief_des": "create adatabase for presence",
            "detailed_des": "create data structures, which define presence at an event, presence types at an event, specified content and tasks for the event ",
            "reference": "presence",
            "date_of_entry": randomDate(),
            "date_of_submission": randomDate(),
            "date_of_fulfillment": randomDate(),
            "id": "1fdd0994-7b0f-11ed-a1eb-0242ac120002",
        },
        {
            "brief_des": "create a database for a user",
            "detailed_des": "create data structures, which define a user (name, surname, email, etc.), who has a certain role in a group at the university ",
            "reference": "user",
            "date_of_entry": randomDate(),
            "date_of_submission": randomDate(),
            "date_of_fulfillment": randomDate(),
            "id": "1fdd0c28-7b0f-11ed-a1eb-0242ac120002",
        },
        {
            "brief_des": "create a database for an event",
            "detailed_des": "create data structures, which define an event, event type(classes, test, etc), what time it is, its location (area, building, classroom) ",
            "reference": "event",
            "date_of_entry": randomDate(),
            "date_of_submission": randomDate(),
            "date_of_fulfillment": randomDate(),
            "id": "1fdd0e12-7b0f-11ed-a1eb-0242ac120002",
        },
    ]
    tasks = []
    return tasks


@cache
def determineContents():

    """Define základní typy obsahu na události"""

    contents = [
        {
            "brief_des": "INF / LESSON",
            "detailed_des": "students will learn advanced programming techniques, such as creating your own simple database ",
            "id": "0ea557e6-7b12-11ed-a1eb-0242ac120002",
        },
        {
            "brief_des": "INF / EXAM",
            "detailed_des": "Students will have to define data structures for a school ",
            "id": "0ea55a84-7b12-11ed-a1eb-0242ac120002",
        },
        {
            "brief_des": "INF / CREDIT TEST",
            "detailed_des": "Students will have to create an ER-Diagram ",
            "id": "0ea558b7-7b12-11ed-a1eb-0242ac120002",
        },
    ]
    contents = []
    return contents


import datetime


def randomDate():

    """Vytváří nám náhodný datum"""

    day = random.randrange(1, 28)
    month = random.randrange(1, 13)
    year = 2022

    # return {day,'/', month,'/', year}
    return datetime.date(year, month, day)


import asyncio


import os
import json
from uoishelpers.feeders import ImportModels
import datetime

def get_demodata():
    def datetime_parser(json_dict):
        for (key, value) in json_dict.items():
            result = value
            try:
                dateValue = datetime.datetime.fromisoformat(value)
                result = dateValue.replace(tzinfo=None)
            except :
                #print(key, value)
                pass
            json_dict[key] = result

            # if key in ["startdate", "enddate", "lastchange", "created", 
            #            "date_of_entry",
            #             "date_of_fulfillment",
            #             "date_of_submission"]:
            #     if value is None:
            #         dateValueWOtzinfo = None
            #     else:
            #         try:
            #             dateValue = datetime.datetime.fromisoformat(value)
            #             dateValueWOtzinfo = dateValue.replace(tzinfo=None)
            #         except:
            #             print("jsonconvert Error", key, value, flush=True)
            #             dateValueWOtzinfo = None
                
            #     json_dict[key] = dateValueWOtzinfo
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
            ContentModel,
            TaskModel,
        ]

    
    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass