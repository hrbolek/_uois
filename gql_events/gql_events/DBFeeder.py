from functools import cache

from gql_events.DBDefinitions import BaseModel, EventModel, UserModel

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
# 46638764-a79c-11ed-b76e-0242ac110002
# 466395ec-a79c-11ed-b76e-0242ac110002
# 466396be-a79c-11ed-b76e-0242ac110002
# 4663972c-a79c-11ed-b76e-0242ac110002
# 46639786-a79c-11ed-b76e-0242ac110002
# 
# 
# 
# 
# 
def get_demodata(asyncSessionMaker):
    pass


def EventPresenceTypes():
    result = [
        {'id': '466398c6-a79c-11ed-b76e-0242ac110002', 'name': 'Přítomen', 'name_en': ''},
        {'id': '4663988a-a79c-11ed-b76e-0242ac110002', 'name': 'Neomluven', 'name_en': ''},
        {'id': '4663984e-a79c-11ed-b76e-0242ac110002', 'name': 'Dovolená', 'name_en': ''},
        {'id': '46639812-a79c-11ed-b76e-0242ac110002', 'name': '', 'name_en': ''},
        {'id': '466397d6-a79c-11ed-b76e-0242ac110002', 'name': '', 'name_en': ''},
    ]

    return result

def EventInvitationTypes():
    #initiator, invited mandatory, invited voluntary, accepted, tentatively accepted, rejected
    result = [
        {'id': "e8713b6e-a79c-11ed-b76e-0242ac110002" , 'name': 'organizátor', 'name_en': 'organizer'},
        {'id': "e8713f06-a79c-11ed-b76e-0242ac110002" , 'name': 'pozvaný', 'name_en': 'invited mandatory'},
        {'id': "e8713fce-a79c-11ed-b76e-0242ac110002" , 'name': 'pozvaný nepovinně', 'name_en': 'invited voluntary'},
        {'id': "e871403c-a79c-11ed-b76e-0242ac110002" , 'name': 'přijal', 'name_en': 'accepted'},
        {'id': "e87140aa-a79c-11ed-b76e-0242ac110002" , 'name': 'přijal nejistě', 'name_en': 'tentatively accepted'},
        {'id': "e8714104-a79c-11ed-b76e-0242ac110002" , 'name': 'odmítl', 'name_en': 'rejected'},
        # {'id': "e8714168-a79c-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
        # {'id': "e87141cc-a79c-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
        # {'id': "e8714226-a79c-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
        # {'id': "e8714294-a79c-11ed-b76e-0242ac110002" , 'name': '', 'name_en': ''},
    ]
    return result