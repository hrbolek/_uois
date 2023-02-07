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
        if resultCache.get('result', None) is None:
            resultCache['result'] = await asyncFunc()
        return resultCache['result']
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
        {'id': '282e67ec-6d9e-11ed-a1eb-0242ac120002', 'name': 'typeA'},
        {'id': '282e6e86-6d9e-11ed-a1eb-0242ac120002', 'name': 'typeB'},
        {'id': '282e7002-6d9e-11ed-a1eb-0242ac120002', 'name': 'typeC'},
    ]
    return data

@cache
def types2():
    # krome id a name, lze mit i dalsi prvky, napriklad cizi klice...
    data = [
        {'id': '4b883614-6d9e-11ed-a1eb-0242ac120002', 'name': 'typeX'},
        {'id': '4b8838a8-6d9e-11ed-a1eb-0242ac120002', 'name': 'typeY'},
        {'id': '4b883a38-6d9e-11ed-a1eb-0242ac120002', 'name': 'typeZ'},
    ]
    return data

@cache
def prgforms():
    result = [
        {'id': '19018d2c-930e-11ed-9b95-0242ac110002', 'name': 'prezenční', 'name_en': 'present'},
        {'id': '19019286-930e-11ed-9b95-0242ac110002', 'name': 'distanční', 'name_en': 'distant'},
        {'id': '19019704-930e-11ed-9b95-0242ac110002', 'name': 'kombinovaný', 'name_en': 'combined'}
    ]
    return result

@cache
def prglanguages():
    result = [
        {'id': '36e9a40a-930e-11ed-9b95-0242ac110002', 'name': 'čeština', 'name_en': 'czech'},
        {'id': '36e9aa04-930e-11ed-9b95-0242ac110002', 'name': 'angličtina', 'name_en': 'english'},
    ]
    return result

@cache
def prglevels():
    result = [
        {'id': '5c5495ce-930e-11ed-9b95-0242ac110002', 'priority': 1, 'name': 'magisterský', 'name_en': 'MSc.', 'length': 5},
        {'id': '5c549aec-930e-11ed-9b95-0242ac110002', 'priority': 2, 'name': 'magisterský navazující na bakalářský', 'name_en': 'MSc.', 'length': 2},
        {'id': '5c549cae-930e-11ed-9b95-0242ac110002', 'priority': 1, 'name': 'bakalářský', 'name_en': 'Bac.', 'length': 3},
        {'id': '79530a3e-930e-11ed-9b95-0242ac110002', 'priority': 3, 'name': 'doktorský', 'name_en': 'PhD.', 'length': 3},
        {'id': '795313da-930e-11ed-9b95-0242ac110002', 'priority': 3, 'name': 'doktorský', 'name_en': 'PhD.', 'length': 4},
    ]
    return result

@cache
def prgtitles():
    result = [
        {'id': 'd1431644-930e-11ed-9b95-0242ac110002', 'name': 'Ing.', 'name_en': ''},
        {'id': 'd1431bd0-930e-11ed-9b95-0242ac110002', 'name': 'Mgr.', 'name_en': ''},
        {'id': 'd1431d9c-930e-11ed-9b95-0242ac110002', 'name': 'Bc.', 'name_en': ''},
        {'id': 'dc5bd804-930e-11ed-9b95-0242ac110002', 'name': 'Ph.D.', 'name_en': ''},
        {'id': '2509ab28-95e2-11ed-a1eb-0242ac120002', 'name': 'MUDr.', 'name_en': ''},
        {'id': 'dc5bdd68-930e-11ed-9b95-0242ac110002', 'name': 'doc.', 'name_en': ''},
        {'id': 'dc5bdf3e-930e-11ed-9b95-0242ac110002', 'name': 'prof.', 'name_en': ''},
    ]
    return result

@cache
def lessontypes():
    result = [
        {'id': 'e2b7c66a-95e1-11ed-a1eb-0242ac120002', 'name': 'cvičení', 'name_en': ''},
        {'id': 'e2b7cbf6-95e1-11ed-a1eb-0242ac120002', 'name': 'přednáška', 'name_en': ''},
        {'id': 'e2b7cfac-95e1-11ed-a1eb-0242ac120002', 'name': 'laboratorní cvičení', 'name_en': ''},
        {'id': 'e2b7d1fa-95e1-11ed-a1eb-0242ac120002', 'name': 'seminář', 'name_en': ''},
        {'id': 'e2b7d48e-95e1-11ed-a1eb-0242ac120002', 'name': 'konzultace', 'name_en': ''},
        {'id': 'e2b7d88a-95e1-11ed-a1eb-0242ac120002', 'name': 'polní výcvik', 'name_en': ''},
    ]
    return result

@cache
def prgtypes():
    result = [
        {'id': 'fd4f0980-9315-11ed-9b95-0242ac110002', 'name': 'bakalářský prezenční 3 roky čeština', 'title_id': 'd1431d9c-930e-11ed-9b95-0242ac110002',
        'form_id': '19018d2c-930e-11ed-9b95-0242ac110002', 'language_id': '36e9a40a-930e-11ed-9b95-0242ac110002', 'level_id': '5c549cae-930e-11ed-9b95-0242ac110002'} ,
        {'id': 'fd4f1d4e-9315-11ed-9b95-0242ac110002', 'name': 'bakalářský kombinovaný 3 roky čeština', 'title_id': 'd1431d9c-930e-11ed-9b95-0242ac110002',
        'form_id': '19019704-930e-11ed-9b95-0242ac110002', 'language_id': '36e9a40a-930e-11ed-9b95-0242ac110002', 'level_id': '5c549cae-930e-11ed-9b95-0242ac110002'} ,
        {'id': 'fd4f1eb6-9315-11ed-9b95-0242ac110002', 'name': 'magisterský navazující na bakalářský prezenční 2 roky čeština', 'title_id': 'd1431644-930e-11ed-9b95-0242ac110002',
        'form_id': '19018d2c-930e-11ed-9b95-0242ac110002', 'language_id': '36e9a40a-930e-11ed-9b95-0242ac110002', 'level_id': '5c5495ce-930e-11ed-9b95-0242ac110002'} ,
        {'id': 'fd4f1f4c-9315-11ed-9b95-0242ac110002', 'name': 'magisterský navazující na bakalářský kombinovaný 2 roky čeština', 'title_id': 'd1431644-930e-11ed-9b95-0242ac110002',
        'form_id': '19019704-930e-11ed-9b95-0242ac110002', 'language_id': '36e9a40a-930e-11ed-9b95-0242ac110002', 'level_id': '5c5495ce-930e-11ed-9b95-0242ac110002'} ,
        {'id': 'fd4f1fba-9315-11ed-9b95-0242ac110002', 'name': 'doktorský prezenční 4 roky čeština', 'title_id': 'dc5bd804-930e-11ed-9b95-0242ac110002',
        'form_id': '19018d2c-930e-11ed-9b95-0242ac110002', 'language_id': '36e9a40a-930e-11ed-9b95-0242ac110002', 'level_id': '79530a3e-930e-11ed-9b95-0242ac110002'} ,
        {'id': 'fd4f2028-9315-11ed-9b95-0242ac110002', 'name': 'doktorský kombinovaný 4 roky čeština', 'title_id': 'dc5bd804-930e-11ed-9b95-0242ac110002',
        'form_id': '19019704-930e-11ed-9b95-0242ac110002', 'language_id': '36e9a40a-930e-11ed-9b95-0242ac110002', 'level_id': '79530a3e-930e-11ed-9b95-0242ac110002'} ,
        {'id': 'fd4f2082-9315-11ed-9b95-0242ac110002', 'name': 'magisterský prezenční 5 let čeština', 'title_id': 'd1431644-930e-11ed-9b95-0242ac110002',
        'form_id': '19018d2c-930e-11ed-9b95-0242ac110002', 'language_id': '36e9a40a-930e-11ed-9b95-0242ac110002', 'level_id': '5c5495ce-930e-11ed-9b95-0242ac110002'} ,
        {'id': 'fd4f20dc-9315-11ed-9b95-0242ac110002', 'name': 'magisterský prezenční 6 let čeština', 'title_id': '2509ab28-95e2-11ed-a1eb-0242ac120002',
        'form_id': '19018d2c-930e-11ed-9b95-0242ac110002', 'language_id': '36e9a40a-930e-11ed-9b95-0242ac110002', 'level_id': '5c5495ce-930e-11ed-9b95-0242ac110002'} ,
    ]
    return result

###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################
from gql_granting.DBDefinitions import ProgramFormTypeModel, ProgramLanguageTypeModel, ProgramLevelTypeModel, ProgramTitleTypeModel, ProgramTypeModel
from gql_granting.DBDefinitions import LessonTypeModel
import asyncio
async def predefineAllDataStructures(asyncSessionMaker):   
    await asyncio.gather(
       putPredefinedStructuresIntoTable(asyncSessionMaker, ProgramFormTypeModel, prgforms), # prvni
       putPredefinedStructuresIntoTable(asyncSessionMaker, ProgramLanguageTypeModel, prglanguages), # prvni
       putPredefinedStructuresIntoTable(asyncSessionMaker, ProgramLevelTypeModel, prglevels), # prvni
       putPredefinedStructuresIntoTable(asyncSessionMaker, ProgramTitleTypeModel, prgtitles),
       putPredefinedStructuresIntoTable(asyncSessionMaker, ProgramTypeModel, prgtypes),
       putPredefinedStructuresIntoTable(asyncSessionMaker, LessonTypeModel, lessontypes),
    )
    return

async def putPredefinedStructuresIntoTable(asyncSessionMaker, DBModel, structureFunction):
    """Zabezpeci prvotni inicicalizaci typu externích ids v databazi
       DBModel zprostredkovava tabulku, je to sqlalchemy model
       structureFunction() dava data, ktera maji byt ulozena
    """
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

    print(structureFunction, 'external id types found in database')
    print(dbRowsDicts)

    # vytahneme si vektor (list) id, ten pouzijeme pro operator in nize
    idsInDatabase = [row['id'] for row in dbRowsDicts]

    # zjistime, ktera id nejsou v databazi
    unsavedRows = list(filter(lambda row: not(row['id'] in idsInDatabase), externalIdTypes))
    print(structureFunction, 'external id types not found in database')
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