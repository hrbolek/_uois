from doctest import master
from functools import cache
from gql_forms.DBDefinitions import BaseModel, UserModel, RequestModel, SectionModel, PartModel, ItemModel
import random
import itertools
from functools import cache
from sqlalchemy.future import select
import datetime
from sqlalchemy.future import select

def singleCall(asyncFunc):
    """A decorator that allows the decorated function to be called (selected) only once. The return value is remembered and returned on subsequent calls.
       The decorated function is asynchronous.
    """
    resultCache = {}
    async def result():
        if resultCache.get('result', None) is None:
            resultCache['result'] = await asyncFunc()
        return resultCache['result']
    return result

###########################################################################################################################
#
# CRUD Ops-Create: define functions, which fill data into your tables
#
###########################################################################################################################

async def createBasicDataStructure():
    print()

# def funcResultingUsers():
#     return [
#         {"id": "024aea76-1ee8-4fd3-9b62-17aad9d07dc6", "name": "Dang Quy Tai", "email": "quytai.dang@unob.cz", "create_at":datetime.datetime.now(), "lastchange":datetime.datetime.now()}
#     ]
#we did it manual way

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


async def putPredefinedStructuresIntoTable(asyncSessionMaker, DBModel, structureFunction):
    """Function to Secures the initial initialization of the record in the database
       DBModel mediates the table,
       structureFunction() gives the data to be stored, a list of dicts is assumed, where dict contains elementary data types
    """

    tableName = DBModel.__tablename__
    # column names
    cols = [col.name for col in DBModel.metadata.tables[tableName].columns]

    def mapToCols(item):
        """selects from item only the attributes that are in DBModel, the rest is ignored"""
        result = {}
        for col in cols:
            value = item.get(col, None)
            if value is None:
                continue
            result[col] = value
        return result

    # valued types 
    externalIdTypes = structureFunction()
    
    #query the database
    stmt = select(DBModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = list(dbSet.scalars())
    
    #extracting data from query results
    #we take only the id attribute, id is of uuid type, so we convert it to string
    idsInDatabase = [f'{row.id}' for row in dbRows]

    # find out which ids are not in the database
    unsavedRows = list(filter(lambda row: not(f'{row["id"]}' in idsInDatabase), externalIdTypes))

    async def saveChunk(rows):
        # create entities for all unstored ids
        # we limit the attributes that are defined in the model
        mappedUnsavedRows = list(map(mapToCols, rows))
        rowsToAdd = [DBModel(**row) for row in mappedUnsavedRows]

        # and insert the created entities into the database with one operation
        async with asyncSessionMaker() as session:
            async with session.begin():
                session.add_all(rowsToAdd)
            await session.commit()

    if len(unsavedRows) > 0:
        #is what to store
        if '_chunk' in unsavedRows[0]:
            # there is information about saving into a table
            nextPhase =  [*unsavedRows]
            while len(nextPhase) > 0:
                #find the smallest storage order number 
                chunkNumber = min(map(lambda item: item['_chunk'], nextPhase))
                #filter rows that have this number
                toSave = list(filter(lambda item: item['_chunk'] == chunkNumber, nextPhase))
                #others we'll leave for later
                nextPhase = list(filter(lambda item: item['_chunk'] != chunkNumber, nextPhase))
                #ulozime vybrane
                await saveChunk(toSave)
        else:
            # all records can be saved at the same time
            await saveChunk(unsavedRows)


    #query the database again
    stmt = select(DBModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = dbSet.scalars()
    
    #extracting data from query results
    idsInDatabase = [f'{row.id}' for row in dbRows]

    # again records that are not yet saved should all be saved, so a empty list
    unsavedRows = list(filter(lambda row: not(f'{row["id"]}' in idsInDatabase), externalIdTypes))

    # now the field maybe empty
    if not(len(unsavedRows) == 0):
        print('SOMETHING is REALLY WRONG')
    pass