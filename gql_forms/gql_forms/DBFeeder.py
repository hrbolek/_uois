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
import datetime


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

# @cache
# def determineRoleTypes():
#     """Definuje zakladni typy roli a udrzuje je v pameti"""
#     roleTypes = [
#         {'name': 'rektor', 'name_en': 'rector', 'id': 'ae3f0d74-6159-11ed-b753-0242ac120003'}, 
#         {'name': 'prorektor', 'name_en': 'vicerector', 'id': 'ae3f2886-6159-11ed-b753-0242ac120003'}, 
#         {'name': 'děkan', 'name_en': 'dean', 'id': 'ae3f2912-6159-11ed-b753-0242ac120003'}, 
#         {'name': 'proděkan', 'name_en': 'vicedean', 'id': 'ae3f2980-6159-11ed-b753-0242ac120003'}, 
#         {'name': 'vedoucí katedry', 'name_en': 'head of department', 'id': 'ae3f29ee-6159-11ed-b753-0242ac120003'}, 
#         {'name': 'vedoucí učitel', 'name_en': 'leading teacher', 'id': 'ae3f2a5c-6159-11ed-b753-0242ac120003'}
#     ]
#     return roleTypes
@cache
def determineSectionNames():
    """Definuje zakladni typy sekci pozadavku a udrzuje je v pameti"""
    sectionNames = [
        'Student Information',
        'Request Description',
        'Head of Department Approval',
        'Department Suggestion',
        'Dean Approval',
        'Faculty Suggestion'
    ]
    return sectionNames

@cache
def determinePartNames():
    """Definuje zakladni typy casti pozadavku a udrzuje je v pameti"""
    partNames = [
        'Personal Information',
        'Leave Details',
        'Approvals'
    ]
    return partNames

@cache
def determineItemNames():
    """Definuje zakladni typy polozek pozadavku a udrzuje je v pameti"""
    itemNames = [
        'Name',
        'Group',
        'Program',
        'Description',
        'Name of Department',
        'Head of Department',
        'Name of Dean',
        'Dean Approval'
    ]
    return itemNames


# def funcResultingUsers():
#     return [
#         {"id": "024aea76-1ee8-4fd3-9b62-17aad9d07dc6", "name": "Dang Quy Tai", "email": "quytai.dang@unob.cz", "create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()}
#     ]

#do it manual way

def funcResultingRequests():
    return [
        {"id": "493aeecc-95d7-11ed-a1eb-0242ac120002", "name": "STC contest application form", "creator_id":"024aea76-1ee8-4fd3-9b62-17aad9d07dc6", "create_at": datetime.datetime.now(), "lastchange":datetime.datetime.now(),"status": "pending"}
    ]

# order can be used in representing forms, sections, ...(UI)
def funcResultingSections():
    return [
        {"request_id": "493aeecc-95d7-11ed-a1eb-0242ac120002", "id": "78fe6a49-3e4f-4aab-bd55-83b822ec140c", "name": "Submission", "order": 1, "create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now(), "status":"submitted"},
        {"request_id": "493aeecc-95d7-11ed-a1eb-0242ac120002", "id": "26b1c646-0a2f-4508-b3e7-56aebe56b017", "name": "Teacher Approval", "order": 2, "create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now(), "status":"approved"},
        {"request_id": "493aeecc-95d7-11ed-a1eb-0242ac120002", "id": "64d485b0-3a45-4b93-9f01-3d59301cefe3", "name": "Dean Approval", "order": 3, "create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now(), "status":"pending"}
    ]

def funcResultingParts():
    return [
        {"section_id": "78fe6a49-3e4f-4aab-bd55-83b822ec140c", "id": "6622876c-cf64-4e6d-a970-4ce63d95c393", "name": "Student Part", "order": 1, "create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},
        {"section_id": "26b1c646-0a2f-4508-b3e7-56aebe56b017", "id": "ddceaf79-5637-49d0-b4f0-d88f4b8dcf9f", "name": "Teacher Part", "order": 2, "create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},
        {"section_id": "64d485b0-3a45-4b93-9f01-3d59301cefe3", "id": "44c685d6-04e1-4fff-9ce6-764b7bc11c93", "name": "Dean Part", "order": 3, "create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()}
    ]

def funcResultingItems():
    return [
        {"part_id": "6622876c-cf64-4e6d-a970-4ce63d95c393", "id": "02727e57-412e-4986-965d-c369beebac48", "name": "Name", "value": "Dang Quy Tai","order":1 ,"create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},
        {"part_id": "6622876c-cf64-4e6d-a970-4ce63d95c393", "id": "10815df6-ad4b-45ca-8957-3528a31bb67f", "name": "Specialization", "value": "Kyberneticka bezpecnost","order":2 , "create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},
        {"part_id": "6622876c-cf64-4e6d-a970-4ce63d95c393", "id": "f451e384-4e5b-40d6-a49f-59df996f3d66", "name": "Group", "value": "23-5KB-C","order":3 , "create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},
        {"part_id": "6622876c-cf64-4e6d-a970-4ce63d95c393", "id": "f9b5b5a5-5b1f-4b9f-9b1f-5b1f4b9f9b1f", "name": "Program", "value": "Mg","order":4, "create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},
        {"part_id": "6622876c-cf64-4e6d-a970-4ce63d95c393", "id": "fe85ac55-b30c-4f15-bba5-9f020764779c", "name": "email", "value": "quytai.dang@unob.cz","order":5, "create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},
        {"part_id": "6622876c-cf64-4e6d-a970-4ce63d95c393", "id": "d378df0f-f659-4b59-9e78-9d250c6496cf", "name": "Description", "value": "I send you my application for STC contest", "order":6,"create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},
        {"part_id": "6622876c-cf64-4e6d-a970-4ce63d95c393", "id": "f9b5b5a5-5b1f-4b9f-9b1f-5b1f4b9faadf", "name": "Status", "value": "submitted", "order":7,"create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},

        {"part_id": "ddceaf79-5637-49d0-b4f0-d88f4b8dcf9f", "id": "8df55c6f-3109-4b37-a1c7-3de1dfd1e404", "name": "Name", "value": "Petr Frantis","order":1, "create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},
        {"part_id": "ddceaf79-5637-49d0-b4f0-d88f4b8dcf9f", "id": "b26dcf77-99d2-4d61-b811-e9b8d35ef2f7", "name": "Department", "value": "K209", "order":2,"create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},
        {"part_id": "ddceaf79-5637-49d0-b4f0-d88f4b8dcf9f", "id": "a0b5b5a5-5b1f-4b9f-9b1f-5b1f4b9f9b1f", "name": "email", "value": "petr.fratis@unob.cz","order":3, "create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},
        {"part_id": "ddceaf79-5637-49d0-b4f0-d88f4b8dcf9f", "id": "c26dcf77-99d2-4d61-b811-e9b8d35ef2f7", "name": "Description", "value": "I have received your application. Application has been approved. I agree to be your supervisor", "order":4,"create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},
        {"part_id": "ddceaf79-5637-49d0-b4f0-d88f4b8dcf9f", "id": "d26dcf77-99d2-4d61-b811-e9b8d35ef2a7", "name": "Status", "value": "approved","order":5, "create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},

        {"part_id": "44c685d6-04e1-4fff-9ce6-764b7bc11c93", "id": "cb84f761-1478-4cad-9196-e3c7242d89b2", "name": "Name", "value": "Frantisek Vojkovsky","order":1, "create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},
        {"part_id": "44c685d6-04e1-4fff-9ce6-764b7bc11c93", "id": "d26dcf77-99d2-4d61-b811-e9b8d35ef2f7", "name": "Department", "value": "K111", "order":2,"create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},
        {"part_id": "44c685d6-04e1-4fff-9ce6-764b7bc11c93", "id": "d0b5b5a5-5b1f-4b9f-9b1f-5b1f4b9f9b1f", "name": "email", "value": "frantisek.vojkovsky@unob.cz","order":3, "create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},
        {"part_id": "44c685d6-04e1-4fff-9ce6-764b7bc11c93", "id": "e26dcf77-99d2-4d61-b811-e9b8d35ef2f7", "name": "Description", "value": "From the dean's office: your application will be on a waiting list. The list of contestants will be announced on January 10, 2023", "order":4,"create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},
        {"part_id": "44c685d6-04e1-4fff-9ce6-764b7bc11c93", "id": "f26dcf77-99d2-4d61-b811-e9b8d35ef2f7", "name": "Status", "value": "pending", "order":5,"create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()},
    ]

async def randomData(asyncSessionMaker):
    # await putPredefinedStructuresIntoTable(asyncSessionMaker, UserModel, funcResultingUsers)
    await putPredefinedStructuresIntoTable(asyncSessionMaker, RequestModel, funcResultingRequests)
    await putPredefinedStructuresIntoTable(asyncSessionMaker, SectionModel, funcResultingSections)
    await putPredefinedStructuresIntoTable(asyncSessionMaker, PartModel, funcResultingParts)
    await putPredefinedStructuresIntoTable(asyncSessionMaker, ItemModel, funcResultingItems)

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

async def putPredefinedStructuresIntoTable(asyncSessionMaker, DBModel, structureFunction):
    """Zabezpeci prvotni inicicalizaci zaznamu v databazi
       DBModel zprostredkovava tabulku,
       structureFunction() dava data, ktera maji byt ulozena, predpoklada se list of dicts, pricemz dict obsahuje elementarni datove typy
    """

    tableName = DBModel.__tablename__
    # column names
    cols = [col.name for col in DBModel.metadata.tables[tableName].columns]

    def mapToCols(item):
        """z item vybere jen atributy, ktere jsou v DBModel, zbytek je ignorovan"""
        result = {}
        for col in cols:
            value = item.get(col, None)
            if value is None:
                continue
            result[col] = value
        return result

    # ocekavane typy 
    externalIdTypes = structureFunction()
    
    #dotaz do databaze
    stmt = select(DBModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = list(dbSet.scalars())
    
    #extrakce dat z vysledku dotazu
    #vezmeme si jen atribut id, id je typu uuid, tak jej zkovertujeme na string
    idsInDatabase = [f'{row.id}' for row in dbRows]

    # zjistime, ktera id nejsou v databazi
    unsavedRows = list(filter(lambda row: not(f'{row["id"]}' in idsInDatabase), externalIdTypes))

    async def saveChunk(rows):
        # pro vsechna neulozena id vytvorime entity
        # omezime se jen na atributy, ktere jsou definovane v modelu
        mappedUnsavedRows = list(map(mapToCols, rows))
        rowsToAdd = [DBModel(**row) for row in mappedUnsavedRows]

        # a vytvorene entity jednou operaci vlozime do databaze
        async with asyncSessionMaker() as session:
            async with session.begin():
                session.add_all(rowsToAdd)
            await session.commit()

    if len(unsavedRows) > 0:
        # je co ukladat
        if '_chunk' in unsavedRows[0]:
            # existuje informace o rozfazovani ukladani do tabulky
            nextPhase =  [*unsavedRows]
            while len(nextPhase) > 0:
                #zjistime nejmensi cislo poradi ukladani 
                chunkNumber = min(map(lambda item: item['_chunk'], nextPhase))
                #filtrujeme radky, ktere maji toto cislo
                toSave = list(filter(lambda item: item['_chunk'] == chunkNumber, nextPhase))
                #ostatni nechame na pozdeji
                nextPhase = list(filter(lambda item: item['_chunk'] != chunkNumber, nextPhase))
                #ulozime vybrane
                await saveChunk(toSave)
        else:
            # vsechny zaznamy mohou byt ulozeny soucasne
            await saveChunk(unsavedRows)


    # jeste jednou se dotazeme do databaze
    stmt = select(DBModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = dbSet.scalars()
    
    #extrakce dat z vysledku dotazu
    idsInDatabase = [f'{row.id}' for row in dbRows]

    # znovu zaznamy, ktere dosud ulozeny nejsou, mely by byt ulozeny vsechny, takze prazdny list
    unsavedRows = list(filter(lambda row: not(f'{row["id"]}' in idsInDatabase), externalIdTypes))

    # ted by melo byt pole prazdne
    if not(len(unsavedRows) == 0):
        print('SOMETHING is REALLY WRONG')

    #print(structureFunction(), 'On the input')
    #print(dbRowsDicts, 'Defined in database')
    # nyni vsechny entity mame v pameti a v databazi synchronizovane
    #print(structureFunction())
    pass