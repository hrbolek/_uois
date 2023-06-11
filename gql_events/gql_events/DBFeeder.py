from functools import cache

from gql_events.DBDefinitions import (
    EventModel, 
    EventTypeModel, 
    EventGroupModel, 
    PresenceModel, 
    PresenceTypeModel, 
    InvitationTypeModel
    )
from sqlalchemy.future import select

###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################
# 46638764-a79c-11ed-b76e-0242ac110002
# 466395ec-a79c-11ed-b76e-0242ac110002
# 466396be-a79c-11ed-b76e-0242ac110002
# 4663972c-a79c-11ed-b76e-0242ac110002
# 46639786-a79c-11ed-b76e-0242ac110002

import datetime

# def _get_demodata():
#     result = {
#         'eventtypes': EventTypes(),
#         'eventinvitationtypes': EventInvitationTypes(),
#         'eventpresencetypes': EventPresenceTypes(),
#         'events': [
#             {
#                 'id': "45b2df80-ae0f-11ed-9bd8-0242ac110002" , 'name': 'Zkouška', 'name_en': 'Exam', 
#                 'eventtype_id': 'b87d3ff0-8fd4-11ed-a6d4-0242ac110002',
#                 'startdate': datetime.datetime(year=2022, month=11, day=2, hour=8, minute=0), 
#                 'enddate': datetime.datetime(year=2022, month=11, day=2, hour=10, minute=0)
#             }
#         ],
#         'events_users': [
#             {'id': "89d1e684-ae0f-11ed-9bd8-0242ac110002", "user_id": "89d1e724-ae0f-11ed-9bd8-0242ac110002", 
#             "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002", "invitation_id": "e871403c-a79c-11ed-b76e-0242ac110002", "presencetype_id": "466398c6-a79c-11ed-b76e-0242ac110002"},
#             {'id': "89d1f2d2-ae0f-11ed-9bd8-0242ac110002", "user_id": "89d1f34a-ae0f-11ed-9bd8-0242ac110002", 
#             "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002", "invitation_id": "e871403c-a79c-11ed-b76e-0242ac110002", "presencetype_id": "466398c6-a79c-11ed-b76e-0242ac110002"},
#             {'id': "89d1f3ae-ae0f-11ed-9bd8-0242ac110002", "user_id": "89d1f3cc-ae0f-11ed-9bd8-0242ac110002", 
#             "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002", "invitation_id": "e871403c-a79c-11ed-b76e-0242ac110002", "presencetype_id": "466398c6-a79c-11ed-b76e-0242ac110002"},
#             {'id': "89d1f412-ae0f-11ed-9bd8-0242ac110002", "user_id": "89d1f430-ae0f-11ed-9bd8-0242ac110002", 
#             "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002", "invitation_id": "e871403c-a79c-11ed-b76e-0242ac110002", "presencetype_id": "466398c6-a79c-11ed-b76e-0242ac110002"},
#             {'id': "89d1f46c-ae0f-11ed-9bd8-0242ac110002", "user_id": "89d1f48a-ae0f-11ed-9bd8-0242ac110002", 
#             "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002", "invitation_id": "e871403c-a79c-11ed-b76e-0242ac110002", "presencetype_id": "466398c6-a79c-11ed-b76e-0242ac110002"},
#             {'id': "89d1f4c6-ae0f-11ed-9bd8-0242ac110002", "user_id": "89d1f4e4-ae0f-11ed-9bd8-0242ac110002", 
#             "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002", "invitation_id": "e871403c-a79c-11ed-b76e-0242ac110002", "presencetype_id": "466398c6-a79c-11ed-b76e-0242ac110002"},
#             {'id': "89d1f520-ae0f-11ed-9bd8-0242ac110002", "user_id": "89d1f534-ae0f-11ed-9bd8-0242ac110002", 
#             "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002", "invitation_id": "e871403c-a79c-11ed-b76e-0242ac110002", "presencetype_id": "466398c6-a79c-11ed-b76e-0242ac110002"},
#             {'id': "89d1f570-ae0f-11ed-9bd8-0242ac110002", "user_id": "89d1f58e-ae0f-11ed-9bd8-0242ac110002", 
#             "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002", "invitation_id": "e871403c-a79c-11ed-b76e-0242ac110002", "presencetype_id": "466398c6-a79c-11ed-b76e-0242ac110002"},
#             {'id': "89d1f5ca-ae0f-11ed-9bd8-0242ac110002", "user_id": "89d1f5de-ae0f-11ed-9bd8-0242ac110002", 
#             "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002", "invitation_id": "e871403c-a79c-11ed-b76e-0242ac110002", "presencetype_id": "466398c6-a79c-11ed-b76e-0242ac110002"},
#             {'id': "89d1f624-ae0f-11ed-9bd8-0242ac110002", "user_id": "89d1f638-ae0f-11ed-9bd8-0242ac110002", 
#             "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002", "invitation_id": "e871403c-a79c-11ed-b76e-0242ac110002", "presencetype_id": "466398c6-a79c-11ed-b76e-0242ac110002"},
#         ],
#         'events_groups': [
#             {'id': "9baf3aaa-ae0f-11ed-9bd8-0242ac110002", "group_id": "9baf3b54-ae0f-11ed-9bd8-0242ac110002", "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002"},
#             {'id': "9baf3d34-ae0f-11ed-9bd8-0242ac110002", "group_id": "9baf3d70-ae0f-11ed-9bd8-0242ac110002", "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002"},
#             {'id': "9baf3dca-ae0f-11ed-9bd8-0242ac110002", "group_id": "9baf3de8-ae0f-11ed-9bd8-0242ac110002", "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002"},
#             {'id': "9baf3e24-ae0f-11ed-9bd8-0242ac110002", "group_id": "9baf3e42-ae0f-11ed-9bd8-0242ac110002", "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002"},
#             {'id': "9baf3e7e-ae0f-11ed-9bd8-0242ac110002", "group_id": "9baf3e92-ae0f-11ed-9bd8-0242ac110002", "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002"},
#             {'id': "9baf3ece-ae0f-11ed-9bd8-0242ac110002", "group_id": "9baf3eec-ae0f-11ed-9bd8-0242ac110002", "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002"},
#             {'id': "9baf3f28-ae0f-11ed-9bd8-0242ac110002", "group_id": "9baf3f3c-ae0f-11ed-9bd8-0242ac110002", "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002"},
#             {'id': "9baf3f82-ae0f-11ed-9bd8-0242ac110002", "group_id": "9baf3f96-ae0f-11ed-9bd8-0242ac110002", "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002"},
#             {'id': "9baf3fd2-ae0f-11ed-9bd8-0242ac110002", "group_id": "9baf3fe6-ae0f-11ed-9bd8-0242ac110002", "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002"},
#             {'id': "9baf402c-ae0f-11ed-9bd8-0242ac110002", "group_id": "9baf4040-ae0f-11ed-9bd8-0242ac110002", "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002"},


#         ],
#     }
#     return result


# def EventTypes():
#     result = [
#         {'id': "c0a12392-ae0e-11ed-9bd8-0242ac110002" , 'name': 'P', 'name_en': ''},
#         {'id': 'b87d3ff0-8fd4-11ed-a6d4-0242ac110002', 'name': 'Ostatní', 'name_en': ''},
#         {'id': 'b87d7b28-8fd4-11ed-a6d4-0242ac110002', 'name': 'LAB', 'name_en': ''},
#         {'id': 'b87d7be6-8fd4-11ed-a6d4-0242ac110002', 'name': 'P', 'name_en': ''},
#         {'id': 'b87d7c2c-8fd4-11ed-a6d4-0242ac110002', 'name': 'CV', 'name_en': ''},
#         {'id': 'b87d7ce0-8fd4-11ed-a6d4-0242ac110002', 'name': 'SEM', 'name_en': ''},
#         {'id': 'b87d7eb6-8fd4-11ed-a6d4-0242ac110002', 'name': 'PV', 'name_en': ''},
#         {'id': 'b87d82e4-8fd4-11ed-a6d4-0242ac110002', 'name': 'ZK', 'name_en': ''},
#         {'id': 'b87d8442-8fd4-11ed-a6d4-0242ac110002', 'name': 'EX', 'name_en': ''},
#         {'id': 'b87d90e0-8fd4-11ed-a6d4-0242ac110002', 'name': 'STŽ', 'name_en': ''},
#         {'id': 'b87d9266-8fd4-11ed-a6d4-0242ac110002', 'name': 'KON', 'name_en': ''},
#         {'id': 'b87d9400-8fd4-11ed-a6d4-0242ac110002', 'name': 'PX', 'name_en': ''},
#         {'id': 'b87d98c4-8fd4-11ed-a6d4-0242ac110002', 'name': 'TER', 'name_en': ''},
#         {'id': 'b87e1010-8fd4-11ed-a6d4-0242ac110002', 'name': 'KRZ', 'name_en': ''},
#         {'id': 'b87e5796-8fd4-11ed-a6d4-0242ac110002', 'name': 'J', 'name_en': ''},
#         {'id': 'b87e6380-8fd4-11ed-a6d4-0242ac110002', 'name': 'SMP', 'name_en': ''},
#         {'id': 'b87e69b6-8fd4-11ed-a6d4-0242ac110002', 'name': 'KOL', 'name_en': ''},
#         {'id': 'b87e6c04-8fd4-11ed-a6d4-0242ac110002', 'name': 'SKP', 'name_en': ''},
#         {'id': 'b87f7cac-8fd4-11ed-a6d4-0242ac110002', 'name': 'SZK', 'name_en': ''},
#         {'id': 'b8803df4-8fd4-11ed-a6d4-0242ac110002', 'name': 'SMS', 'name_en': ''}
#     ]
#     return result


# def EventPresenceTypes():
#     result = [
#         {'id': '466398c6-a79c-11ed-b76e-0242ac110002', 'name': 'Přítomen', 'name_en': ''},
#         {'id': '4663988a-a79c-11ed-b76e-0242ac110002', 'name': 'Neomluven', 'name_en': ''},
#         {'id': '4663984e-a79c-11ed-b76e-0242ac110002', 'name': 'Dovolená', 'name_en': ''},
#         {'id': '46639812-a79c-11ed-b76e-0242ac110002', 'name': '', 'name_en': ''},
#         {'id': '466397d6-a79c-11ed-b76e-0242ac110002', 'name': '', 'name_en': ''},
#     ]

#     return result

# def EventInvitationTypes():
#     #initiator, invited mandatory, invited voluntary, accepted, tentatively accepted, rejected
#     result = [
#         {'id': "e8713b6e-a79c-11ed-b76e-0242ac110002" , 'name': 'organizátor', 'name_en': 'organizer'},
#         {'id': "e8713f06-a79c-11ed-b76e-0242ac110002" , 'name': 'pozvaný', 'name_en': 'invited mandatory'},
#         {'id': "e8713fce-a79c-11ed-b76e-0242ac110002" , 'name': 'pozvaný nepovinně', 'name_en': 'invited voluntary'},
#         {'id': "e871403c-a79c-11ed-b76e-0242ac110002" , 'name': 'přijal', 'name_en': 'accepted'},
#         {'id': "e87140aa-a79c-11ed-b76e-0242ac110002" , 'name': 'přijal nejistě', 'name_en': 'tentatively accepted'},
#         {'id': "e8714104-a79c-11ed-b76e-0242ac110002" , 'name': 'odmítl', 'name_en': 'rejected'},
#         # {'id': "e8714168-a79c-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
#         # {'id': "e87141cc-a79c-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
#         # {'id': "e8714226-a79c-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
#         # {'id': "e8714294-a79c-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
#     ]
#     return result


import asyncio
import os
import json

from uoishelpers.feeders import ImportModels
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

    defaultNoDemo = "_________"
    if defaultNoDemo == os.environ.get("DEMO", defaultNoDemo):
        print("No Demo mode")
        dbModels = [
            EventTypeModel,           
            PresenceTypeModel, 
            InvitationTypeModel        ]
    else:
        print("Demo mode")
        dbModels = [
            EventTypeModel, 
            PresenceTypeModel, 
            InvitationTypeModel,
            EventModel, 
            EventGroupModel, 
            PresenceModel, 
        ]

    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass
