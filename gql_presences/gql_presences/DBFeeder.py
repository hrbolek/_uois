from doctest import master
from functools import cache
from gql_presences.DBDefinitions import BaseModel, PresenceModel, PresenceTypeModel, ContentModel, TaskModel

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

@cache
def determinePresenceTypes():
    """Definuje zakladni typy přítomnosti a udrzuje je v pameti"""
    presenceTypes = [
        {'name': 'přítomen', 'name_en': 'present', 'id': 'a6ca5364-7abd-11ed-a1eb-0242ac120002'},

        #doplnit zbytek UUID
        {'name': 'absent', 'name_en': 'absent', 'id': 'a6ca574c-7abd-11ed-a1eb-0242ac120002'},
        {'name': 'nemoc', 'name_en': 'sick leave', 'id': 'a6ca5b7a-7abd-11ed-a1eb-0242ac120002'},

        {'name': 'ŘD', 'name_en': 'official leave', 'id': 'a6ca5d0a-7abd-11ed-a1eb-0242ac120002'},
        {'name': 'služba', 'name_en': 'guard duty', 'id': 'a6ca5ee0-7abd-11ed-a1eb-0242ac120002'},
        

        {'name': 'NV', 'name_en': 'compensatory leave', 'id': 'a6ca6264-7abd-11ed-a1eb-0242ac120002'},
        ]
    return presenceTypes


@cache
def determineTasks():
    """Determinuje základní úlohy"""

    tasks = [
        {
            'brief_des': 'create adatabase for presence',
            'detailed_des': 'create data structures, which define presence at an event, presence types at an event, specified content and tasks for the event ',
            'reference': 'presence',
            'date_of_entry': randomDate(),
            'date_of_submission': randomDate(),
            'date_of_fulfillment': randomDate(),
            'id': '1fdd0994-7b0f-11ed-a1eb-0242ac120002'
        },

        {
            'brief_des': 'create a database for a user',
            'detailed_des': 'create data structures, which define a user (name, surname, email, etc.), who has a certain role in a group at the university ',
            'reference': 'user',
            'date_of_entry': randomDate(),
            'date_of_submission': randomDate(),
            'date_of_fulfillment': randomDate(),
            'id': '1fdd0c28-7b0f-11ed-a1eb-0242ac120002'
        },
        
        {
            'brief_des': 'create a database for an event',
            'detailed_des': 'create data structures, which define an event, event type(classes, test, etc), what time it is, its location (area, building, classroom) ',
            'reference': 'event',
            'date_of_entry': randomDate(),
            'date_of_submission': randomDate(),
            'date_of_fulfillment': randomDate(),
            'id': '1fdd0e12-7b0f-11ed-a1eb-0242ac120002'
        },

        ]
    tasks = []
    return tasks

@cache
def determineContents():

    """Define základní typy obsahu na události"""

    contents = [
        {
            'brief_des': 'INF / LESSON',
            'detailed_des': 'students will learn advanced programming techniques, such as creating your own simple database ',
            'id': '0ea557e6-7b12-11ed-a1eb-0242ac120002'
        },

        {
            'brief_des': 'INF / EXAM',
            'detailed_des': 'Students will have to define data structures for a school ',
            'id': '0ea55a84-7b12-11ed-a1eb-0242ac120002'
        },

        {
            'brief_des': 'INF / CREDIT TEST',
            'detailed_des': 'Students will have to create an ER-Diagram ',
            'id': '0ea558b7-7b12-11ed-a1eb-0242ac120002'
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

    #return {day,'/', month,'/', year}
    return datetime.date(year, month, day)



import asyncio
from gql_presences.DBDefinitions import PresenceTypeModel
async def predefineAllDataStructures(asyncSessionMaker):
    #
    asyncio.gather(
       putPredefinedStructuresIntoTable(asyncSessionMaker,PresenceTypeModel,determinePresenceTypes),
       putPredefinedStructuresIntoTable(asyncSessionMaker,TaskModel,determineTasks),
       putPredefinedStructuresIntoTable(asyncSessionMaker,ContentModel,determineContents)
     )
    #
    #
    
    return
# vytvořit async def 
# bude se volat akorát TaskModel a ContentModel
"""Zabezpeci prvotni inicicalizaci typu externích ids v databazi
       DBModel zprostredkovava tabulku, je to sqlalchemy model
       structureFunction() dava data, ktera maji byt ulozena
    """


async def putPredefinedStructuresIntoTable(asyncSessionMaker, DBModel, structureFunction):
    
    # ocekavane typy 
    externalIdTypes = structureFunction()
    
    #dotaz do databaze
    stmt = select(DBModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = list(dbSet.scalars())
    
    #extrakce dat z vysledku dotazu
    #vezmeme si jen atributy name a id, id je typu uuid, tak jej zkovertujeme na string
    dbRowsDicts = [
        {'name': row.name, 'id': f'{row.id}'} for row in dbRows
        ]

    print(structureFunction, 'id types found in database')
    print(dbRowsDicts)

    # vytahneme si vektor (list) id, ten pouzijeme pro operator in nize
    idsInDatabase = [row['id'] for row in dbRowsDicts]

    # zjistime, ktera id nejsou v databazi
    unsavedRows = list(filter(lambda row: not(row['id'] in idsInDatabase), externalIdTypes))
    print(structureFunction, 'id types not found in database')
    print(unsavedRows)

    # pro vsechna neulozena id vytvorime entity
    rowsToAdd = [DBModel(**row) for row in unsavedRows]
    print(rowsToAdd)
    print(len(rowsToAdd))

    # a vytvorene entity jednou operaci vlozime do databaze
    async with asyncSessionMaker() as session:
        async with session.begin():
            session.add_all(rowsToAdd)
        await session.commit()

    # jeste jednou se dotazeme do databaze
    stmt = select(DBModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = dbSet.scalars()
    
    #extrakce dat z vysledku dotazu
    dbRowsDicts = [
        {'name': row.name, 'id': f'{row.id}'} for row in dbRows
        ]

    print(structureFunction, 'found in database')
    print(dbRowsDicts)

    # znovu id, ktera jsou uz ulozena
    idsInDatabase = [row['id'] for row in dbRowsDicts]

    # znovu zaznamy, ktere dosud ulozeny nejsou, mely by byt ulozeny vsechny, takze prazdny list
    unsavedRows = list(filter(lambda row: not(row['id'] in idsInDatabase), externalIdTypes))

    # ted by melo byt pole prazdne
    print(structureFunction, 'not found in database')
    print(unsavedRows)
    if not(len(unsavedRows) == 0):
        print('SOMETHING is REALLY WRONG')

    print(structureFunction, 'Defined in database')
    # nyni vsechny entity mame v pameti a v databazi synchronizovane
    print(structureFunction())
    pass

