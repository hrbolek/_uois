from doctest import master
from functools import cache
# from gql_workflow.DBDefinitions import BaseModel, UserModel, GroupModel, RoleTypeModel
# import the base model, when appolo sever ask your container for the first time, gql will ask 
# next step define some resolver, how to use resolver in the file graptype
# check all data strcture in database if it have -- (work)
from gql_forms.DBDefinitions import BaseModel, UserModel, RequestModel, SectionModel, PartModel, ItemModel
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
        if resultCache.get('result', None) is None:
            resultCache['result'] = await asyncFunc()
        return resultCache['result']
    return result

###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################

async def createBasicDataStructure():
    print()


@cache
def determineRequestNames():
    """Definuje zakladni typy pozadavku a udrzuje je v pameti"""
    requestNames = [
        'Vacation',
        'Sick Leave',
        'Business Trip',
        'Maternity Leave',
        'Parental Leave',
        'Study Leave',
        'Other Leave'
    ]
    return requestNames


@cache
def determineSectionNames():
    """Definuje zakladni typy sekci pozadavku a udrzuje je v pameti"""
    sectionNames = [
        'Submission',
        'Teacher Approval',
        'Dean Approval',
    ]
    return sectionNames

@cache
def determinePartNames():
    """Definuje zakladni typy casti pozadavku a udrzuje je v pameti"""
    partNames = [
        'Student Part',
        'Teacher Part',
        'Dean Part'
    ]
    return partNames

@cache
def determineItemNames():
    """Definuje zakladni typy polozek pozadavku a udrzuje je v pameti"""
    itemNames = [
        'Name',
        'Group',
        'Specialization',
        'Program',
        'email',
        'Description',
        'Status',
        'Department'
    ]
    return itemNames


# def randomString(length=10, chars=string.ascii_lowercase):
#     """Generuje nahodny retezec o zadane delce"""
#     return ''.join(random.choice(chars) for _ in range(length))
# def randomUser():
#     """Generuje nahodneho uzivatele"""
#     return {
#         'name': randomString(),
#         'surname': randomString(),
#         'email': f'{randomString()}@{randomString()}.com',
#     }

# # generate 10 random users
# # users = [randomUser() for _ in range(10)]
# # print(users)

