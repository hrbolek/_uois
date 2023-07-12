from doctest import master
from functools import cache
from gql_granting.DBDefinitions import BaseModel

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
# zde definujte sva systemova data
#
###########################################################################################################################
import datetime

def get_demodata():
    result = {
        "groups": [
            {"id": "2766f9d4-b095-11ed-9bd8-0242ac110002" },
        ],
        "users": [
            {"id": "ce250c16-b095-11ed-9bd8-0242ac110002" },
        ],

        "acprogramforms": prgforms(),
        "acprogramlanguages": prglanguages(),
        "acprogramlevels": prglevels(),
        "acprogramtitles": prgtitles(),
        "acprogramtypes": prgtypes(),
        "acclassificationlevels": get_acclassificationlevels(),
        "acclassificationtypes": get_acclassificationtypes(),
        "aclessontypes": lessontypes(),

        "acprogramgroups": [
            {"id": "ce250798-b095-11ed-9bd8-0242ac110002" },
        ],
        "acprograms": [
            {"id": "2766fc9a-b095-11ed-9bd8-0242ac110002",
                "type_id": "fd4f0980-9315-11ed-9b95-0242ac110002",
                "lastchange": datetime.datetime.now(),
                "name": "IT Technologie", "name_en": "" },
        ],
        "acsubjects": [
            {"id": "ce250a68-b095-11ed-9bd8-0242ac110002",
                "program_id": "2766fc9a-b095-11ed-9bd8-0242ac110002",
                "lastchange": datetime.datetime.now(),
                "name": "Programování", "name_en": "" },
        ],
        "acsemesters": [
            {"id": "ce250af4-b095-11ed-9bd8-0242ac110002",
                "subject_id": "ce250a68-b095-11ed-9bd8-0242ac110002",
                "classificationtype_id": "a00a0642-b095-11ed-9bd8-0242ac110002",
                "lastchange": datetime.datetime.now(),
                "order": 1, "credits": 24 },
        ],
        "actopics": [
            {"id": "ce250b44-b095-11ed-9bd8-0242ac110002",
                "semester_id": "ce250af4-b095-11ed-9bd8-0242ac110002",
                "lastchange": datetime.datetime.now(),
                "name": "Úvod", "name_en": "", "order" : 1
             },            
        ],
        "aclessons": [
            {"id": "ce250b8a-b095-11ed-9bd8-0242ac110002",        
                "topic_id" : "ce250b44-b095-11ed-9bd8-0242ac110002",
                "type_id": "e2b7cbf6-95e1-11ed-a1eb-0242ac120002",
                "lastchange": datetime.datetime.now(),
                "count": 1            
             },            
        ],
        "acclassifications": [
            {"id": "ce250bd0-b095-11ed-9bd8-0242ac110002", 
                "user_id": "ce250c16-b095-11ed-9bd8-0242ac110002",
                "semester_id": "ce250af4-b095-11ed-9bd8-0242ac110002",
                "classificationtype_id": "a00a0322-b095-11ed-9bd8-0242ac110002",
                "classificationlevel_id": "5faea396-b095-11ed-9bd8-0242ac110002",
                "lastchange": datetime.datetime.now(),
                "order": 1,   
                 },
            {"id": "ce250bd1-b095-11ed-9bd8-0242ac110002", 
                "user_id": "ce250c16-b095-11ed-9bd8-0242ac110002",
                "semester_id": "ce250af4-b095-11ed-9bd8-0242ac110002",
                "classificationtype_id": "a00a0322-b095-11ed-9bd8-0242ac110002",
                "classificationlevel_id": "5faea21a-b095-11ed-9bd8-0242ac110002",
                "lastchange": datetime.datetime.now(),
                "order": 2,
                 },
        ],

    }

    return result

@cache
def get_acclassificationlevels():
    result = [
        {"id": "5fae9dd8-b095-11ed-9bd8-0242ac110002" , "name": 'A', "name_en": 'A'},
        {"id": "5faea134-b095-11ed-9bd8-0242ac110002" , "name": 'B', "name_en": 'B'},
        {"id": "5faea21a-b095-11ed-9bd8-0242ac110002" , "name": 'C', "name_en": 'C'},
        {"id": "5faea2d8-b095-11ed-9bd8-0242ac110002" , "name": 'D', "name_en": 'D'},
        {"id": "5faea332-b095-11ed-9bd8-0242ac110002" , "name": 'E', "name_en": 'E'},
        {"id": "5faea396-b095-11ed-9bd8-0242ac110002" , "name": 'F', "name_en": 'F'},
    ]
    return result

@cache
def get_acclassificationtypes():
    result = [
        {"id": "a00a0322-b095-11ed-9bd8-0242ac110002" , "name": 'Z', "name_en": ''},
        {"id": "a00a0642-b095-11ed-9bd8-0242ac110002" , "name": 'Z+Zk', "name_en": ''},
        {"id": "a00a06f6-b095-11ed-9bd8-0242ac110002" , "name": 'Zk', "name_en": ''},
        {"id": "a00a076e-b095-11ed-9bd8-0242ac110002" , "name": 'KZ', "name_en": ''},
    ]
    return result

@cache
def prgforms():
    result = [
        {
            "id": "19018d2c-930e-11ed-9b95-0242ac110002",
            "name": "prezenční",
            "name_en": "present",
        },
        {
            "id": "19019286-930e-11ed-9b95-0242ac110002",
            "name": "distanční",
            "name_en": "distant",
        },
        {
            "id": "19019704-930e-11ed-9b95-0242ac110002",
            "name": "kombinovaný",
            "name_en": "combined",
        },
    ]
    return result


@cache
def prglanguages():
    result = [
        {
            "id": "36e9a40a-930e-11ed-9b95-0242ac110002",
            "name": "čeština",
            "name_en": "czech",
        },
        {
            "id": "36e9aa04-930e-11ed-9b95-0242ac110002",
            "name": "angličtina",
            "name_en": "english",
        },
    ]
    return result


@cache
def prglevels():
    result = [
        {
            "id": "5c5495ce-930e-11ed-9b95-0242ac110002",
            "priority": 1,
            "name": "magisterský",
            "name_en": "MSc.",
            "length": 5,
        },
        {
            "id": "5c549aec-930e-11ed-9b95-0242ac110002",
            "priority": 2,
            "name": "magisterský navazující na bakalářský",
            "name_en": "MSc.",
            "length": 2,
        },
        {
            "id": "5c549cae-930e-11ed-9b95-0242ac110002",
            "priority": 1,
            "name": "bakalářský",
            "name_en": "Bac.",
            "length": 3,
        },
        {
            "id": "79530a3e-930e-11ed-9b95-0242ac110002",
            "priority": 3,
            "name": "doktorský",
            "name_en": "PhD.",
            "length": 3,
        },
        {
            "id": "795313da-930e-11ed-9b95-0242ac110002",
            "priority": 3,
            "name": "doktorský",
            "name_en": "PhD.",
            "length": 4,
        },
    ]
    return result


@cache
def prgtitles():
    result = [
        {"id": "d1431644-930e-11ed-9b95-0242ac110002", "name": "Ing.", "name_en": ""},
        {"id": "d1431bd0-930e-11ed-9b95-0242ac110002", "name": "Mgr.", "name_en": ""},
        {"id": "d1431d9c-930e-11ed-9b95-0242ac110002", "name": "Bc.", "name_en": ""},
        {"id": "dc5bd804-930e-11ed-9b95-0242ac110002", "name": "Ph.D.", "name_en": ""},
        {"id": "2509ab28-95e2-11ed-a1eb-0242ac120002", "name": "MUDr.", "name_en": ""},
        {"id": "dc5bdd68-930e-11ed-9b95-0242ac110002", "name": "doc.", "name_en": ""},
        {"id": "dc5bdf3e-930e-11ed-9b95-0242ac110002", "name": "prof.", "name_en": ""},
    ]
    return result


@cache
def lessontypes():
    result = [
        {
            "id": "e2b7c66a-95e1-11ed-a1eb-0242ac120002",
            "name": "cvičení",
            "name_en": "",
        },
        {
            "id": "e2b7cbf6-95e1-11ed-a1eb-0242ac120002",
            "name": "přednáška",
            "name_en": "",
        },
        {
            "id": "e2b7cfac-95e1-11ed-a1eb-0242ac120002",
            "name": "laboratorní cvičení",
            "name_en": "",
        },
        {
            "id": "e2b7d1fa-95e1-11ed-a1eb-0242ac120002",
            "name": "seminář",
            "name_en": "",
        },
        {
            "id": "e2b7d48e-95e1-11ed-a1eb-0242ac120002",
            "name": "konzultace",
            "name_en": "",
        },
        {
            "id": "e2b7d88a-95e1-11ed-a1eb-0242ac120002",
            "name": "polní výcvik",
            "name_en": "",
        },
    ]
    return result


@cache
def prgtypes():
    result = [
        {
            "id": "fd4f0980-9315-11ed-9b95-0242ac110002",
            "name": "bakalářský prezenční 3 roky čeština",
            "name_en": "bachelor present 3 years czech",
            "title_id": "d1431d9c-930e-11ed-9b95-0242ac110002",
            "form_id": "19018d2c-930e-11ed-9b95-0242ac110002",
            "language_id": "36e9a40a-930e-11ed-9b95-0242ac110002",
            "level_id": "5c549cae-930e-11ed-9b95-0242ac110002",
        },
        {
            "id": "fd4f1d4e-9315-11ed-9b95-0242ac110002",
            "name": "bakalářský kombinovaný 3 roky čeština",
            "name_en": "bachelor combined 3 years czech",
            "title_id": "d1431d9c-930e-11ed-9b95-0242ac110002",
            "form_id": "19019704-930e-11ed-9b95-0242ac110002",
            "language_id": "36e9a40a-930e-11ed-9b95-0242ac110002",
            "level_id": "5c549cae-930e-11ed-9b95-0242ac110002",
        },
        {
            "id": "fd4f1eb6-9315-11ed-9b95-0242ac110002",
            "name": "magisterský navazující na bakalářský prezenční 2 roky čeština",
            "name_en": "master extending bachelor present 2 years czech",
            "title_id": "d1431644-930e-11ed-9b95-0242ac110002",
            "form_id": "19018d2c-930e-11ed-9b95-0242ac110002",
            "language_id": "36e9a40a-930e-11ed-9b95-0242ac110002",
            "level_id": "5c5495ce-930e-11ed-9b95-0242ac110002",
        },
        {
            "id": "fd4f1f4c-9315-11ed-9b95-0242ac110002",
            "name": "magisterský navazující na bakalářský kombinovaný 2 roky čeština",
            "name_en": "master extending bachelor combined 2 years czech",
            "title_id": "d1431644-930e-11ed-9b95-0242ac110002",
            "form_id": "19019704-930e-11ed-9b95-0242ac110002",
            "language_id": "36e9a40a-930e-11ed-9b95-0242ac110002",
            "level_id": "5c5495ce-930e-11ed-9b95-0242ac110002",
        },
        {
            "id": "fd4f1fba-9315-11ed-9b95-0242ac110002",
            "name": "doktorský prezenční 4 roky čeština",
            "name_en": "doctoral present 4 years czech",
            "title_id": "dc5bd804-930e-11ed-9b95-0242ac110002",
            "form_id": "19018d2c-930e-11ed-9b95-0242ac110002",
            "language_id": "36e9a40a-930e-11ed-9b95-0242ac110002",
            "level_id": "79530a3e-930e-11ed-9b95-0242ac110002",
        },
        {
            "id": "fd4f2028-9315-11ed-9b95-0242ac110002",
            "name": "doktorský kombinovaný 4 roky čeština",
            "name_en": "doctoral combined 4 years czech",
            "title_id": "dc5bd804-930e-11ed-9b95-0242ac110002",
            "form_id": "19019704-930e-11ed-9b95-0242ac110002",
            "language_id": "36e9a40a-930e-11ed-9b95-0242ac110002",
            "level_id": "79530a3e-930e-11ed-9b95-0242ac110002",
        },
        {
            "id": "fd4f2082-9315-11ed-9b95-0242ac110002",
            "name": "magisterský prezenční 5 let čeština",
            "name_en": "master present 5 years czech",
            "title_id": "d1431644-930e-11ed-9b95-0242ac110002",
            "form_id": "19018d2c-930e-11ed-9b95-0242ac110002",
            "language_id": "36e9a40a-930e-11ed-9b95-0242ac110002",
            "level_id": "5c5495ce-930e-11ed-9b95-0242ac110002",
        },
        {
            "id": "fd4f20dc-9315-11ed-9b95-0242ac110002",
            "name": "magisterský prezenční 6 let čeština",
            "name_en": "master present 6 years czech",
            "title_id": "2509ab28-95e2-11ed-a1eb-0242ac120002",
            "form_id": "19018d2c-930e-11ed-9b95-0242ac110002",
            "language_id": "36e9a40a-930e-11ed-9b95-0242ac110002",
            "level_id": "5c5495ce-930e-11ed-9b95-0242ac110002",
        },
    ]
    return result


###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################
from gql_granting.DBDefinitions import (
    
    ProgramFormTypeModel,
    ProgramLanguageTypeModel,
    ProgramLevelTypeModel,
    ProgramTitleTypeModel,
    ProgramTypeModel,
    ProgramModel,
    SubjectModel,
    SemesterModel,
    TopicModel,
    LessonModel,
    LessonTypeModel,
    
    ClassificationLevelModel,
    ClassificationModel,
    ClassificationTypeModel,


)

import asyncio
import os
import json

from uoishelpers.feeders import ImportModels

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

    defaultNoDemo = "_________"
    if defaultNoDemo == os.environ.get("DEMO", defaultNoDemo):
        dbModels = [
            ProgramFormTypeModel,
            ProgramLanguageTypeModel,
            ProgramLevelTypeModel,
            ProgramTitleTypeModel,
            ProgramTypeModel,
            LessonTypeModel,

            ClassificationLevelModel,
            ClassificationTypeModel,
        ]
    else:
        dbModels = [
            ProgramFormTypeModel,
            ProgramLanguageTypeModel,
            ProgramLevelTypeModel,
            ProgramTitleTypeModel,
            ProgramTypeModel,
            LessonTypeModel,
            ClassificationLevelModel,
            ClassificationTypeModel,

            ProgramModel,
            SubjectModel,
            SemesterModel,
            TopicModel,
            LessonModel,
            ClassificationModel,

        ]
        
    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass
