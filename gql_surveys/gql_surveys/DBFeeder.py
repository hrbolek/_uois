from doctest import master
from functools import cache
from gql_surveys.DBDefinitions import BaseModel, UserModel

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

from gql_surveys.DBDefinitions import BaseModel, UserModel, QuestionTypeModel, QuestionModel, AnswerModel, SurveyModel

@cache
def determineQuestionTypes():
    questionType = [
        {'id': 'ad0f53fb-240b-47de-ab1d-871bbde6f973','name': 'Uzavřené'}, 
        {'id': '949d74a2-63b1-4478-82f1-e025d8bc6c8b','name': 'Otevřené'},
        {'id': '2a6a1731-1efa-4644-a1d8-5848e4b29ce5','name': 'Škála'}
    ]
    return questionType


async def randomSurveyData(session):
    users=[
        {'id': '78681d58-bc51-4548-8d72-867b748cdd58'}, #user 1
        {'id': '417ab772-bc07-4a01-8ef3-f8fef9a17042'}, #user 2
    ]
    surveys=[{'id': '910d54a9-7f2e-41ca-b811-3c600ef82fda', 'name': 'Studentské hodnocení'}]
    questions=[ 
        {'id': '5b7e4ae7-9bb9-4e2f-829b-c2763ac1092e', 'name': 'Jak hodnotíte předmět xy', 'order': 1, 'lastchange': datetime.datetime.now(),
        'survey_id': '910d54a9-7f2e-41ca-b811-3c600ef82fda', 'type_id': '2a6a1731-1efa-4644-a1d8-5848e4b29ce5'}, #škála
        {'id': '984120da-ab92-44bd-9389-5f47ed9b3225', 'name': 'Jak hodnotíte výuku předmětu xy', 'order': 2, 'lastchange': datetime.datetime.now(),
        'survey_id': '910d54a9-7f2e-41ca-b811-3c600ef82fda', 'type_id': '949d74a2-63b1-4478-82f1-e025d8bc6c8b'}, #otevřené
        {'id': '2b27adcc-0b7e-40c4-a430-8e0aa551ae3e', 'name': 'Který předmět považujete za nejvíc přínosný?', 'order': 3, 'lastchange': datetime.datetime.now(),
        'survey_id': '910d54a9-7f2e-41ca-b811-3c600ef82fda', 'type_id': 'ad0f53fb-240b-47de-ab1d-871bbde6f973'}, #uzavřené
    ]
    answers=[
        #user 1
        {'id': 'ad0f53fb-240b-47de-ab1d-871bbde6f973', 'value': '8', 'aswered': True, 'expired': False, 
        'user_id': '78681d58-bc51-4548-8d72-867b748cdd58', 'question_id': '5b7e4ae7-9bb9-4e2f-829b-c2763ac1092e'},
        {'id': 'dd7dc78f-534d-4c33-a979-2dfd41a53a84', 'value': 'OK', 'aswered': True, 'expired': False, 
        'user_id': '78681d58-bc51-4548-8d72-867b748cdd58', 'question_id': '984120da-ab92-44bd-9389-5f47ed9b3225'},
        {'id': 'bb0cd1b9-15ba-4f80-a6a0-7a9dc65deb13', 'value': 'Analýza informačních zdrojů', 'aswered': True, 'expired': False, 
        'user_id': '78681d58-bc51-4548-8d72-867b748cdd58', 'question_id': '2b27adcc-0b7e-40c4-a430-8e0aa551ae3e'},
        #user 2
        {'id': 'e054d1a5-f259-429d-9f7a-f35d55caf2ab', 'value': None, 'aswered': False, 'expired': False, 
        'user_id': '417ab772-bc07-4a01-8ef3-f8fef9a17042', 'question_id': '5b7e4ae7-9bb9-4e2f-829b-c2763ac1092e'},
        {'id': '600a7008-44b6-46e9-a546-d934731a0603', 'value': None, 'aswered': True, 'expired': False, 
        'user_id': '417ab772-bc07-4a01-8ef3-f8fef9a17042', 'question_id': '984120da-ab92-44bd-9389-5f47ed9b3225'},
        {'id': 'ed33c145-c295-41c2-be49-5037837ee974', 'value': None, 'aswered': True, 'expired': False, 
        'user_id': '417ab772-bc07-4a01-8ef3-f8fef9a17042', 'question_id': '2b27adcc-0b7e-40c4-a430-8e0aa551ae3e'},
    ] 
    asyncSessionMaker = lambda:session
    await putPredefinedStructuresIntoTable(asyncSessionMaker, UserModel, lambda:users)
    await putPredefinedStructuresIntoTable(asyncSessionMaker, SurveyModel, lambda:surveys)
    await putPredefinedStructuresIntoTable(asyncSessionMaker, QuestionModel, lambda:questions)
    await putPredefinedStructuresIntoTable(asyncSessionMaker, AnswerModel, lambda:answers)
    return surveys[0]["id"]


async def SystemInitialization(asyncSessionMaker):
    await putPredefinedStructuresIntoTable(asyncSessionMaker, QuestionTypeModel, determineQuestionTypes)


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