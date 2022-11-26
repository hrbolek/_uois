from gql_projects.DBDefinitions import BaseModel, ProjectModel, ProjectTypeModel, FinanceModel, FinanceTypeModel, MilestoneModel, GroupModel

import uuid
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

def determineProjectTypes():
    """Definuje zakladni typy roli"""
    projectTypes = [ 
        {'name': 'shortTerm'},
        {'name': 'mediumTerm'},
        {'name': 'longTerm'},
    ]
    return projectTypes

def determineFinanceTypes():
    """Definuje zakladni typy financi"""
    financeTypes = [ 
        {'name': 'travel_expenses'},
        {'name': 'accomodation_expenses'},
        {'name': 'other_expenses'},
    ]
    return financeTypes

def randomProject(name):
    """Náhodný projekt"""
    result = {
        'id': f'{uuid.uuid1()}',
        'name': f'{name}',
        #'startDate': randomDate()
        #'endDate': randomDate()
        'milestones' : [
            #randomMilestone(i+1) for i in range(random.randint(3, 5))
        ],
    }
    return result

def randomMilestone(index):
    """Náhodný milestone"""
    result = {
        'name': f'Milestone {index}'
        #'startDate': randomDate(),
        #'endDAte' :  randomDate(),

    }
    return result
    
def randomFinance():
    """Náhodné finance"""
    result = {
        'name':'',
        'amount': random.randint(100, 20000),
    }
    return result

async def putPredefinedStructuresIntoTable(asyncSessionMaker, DBModel, structureFunction):
    """Zabezpeci prvotni inicicalizaci typu externích ids v databazi
       DBModel zprostredkovava tabulku,
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