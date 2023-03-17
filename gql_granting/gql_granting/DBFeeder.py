from doctest import master
from functools import cache
from gql_granting.DBDefinitions import BaseModel, StudyProgramModel, SubjectModel, StudyLanguageModel, SemesterModel, \
    ClassificationModel, StudyThemeModel, StudyThemeItemModel, ThemeTypeModel
import uuid
import random
import datetime
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
def determineStudyPrograms():
    # Returns list of study programs
    data = [
        {
            'id': '4b883614-6d9e-11ed-a1eb-0242ac120002',
            'type': 'Master',
            'study_duration': 5,
            'type_of_study': 'Military',
            'name': 'Kybernetická bezpečnost',
            'lastchange': datetime.datetime,
        },
        {
            'id': '4b883614-6d5e-11ed-a1eb-0242ac120405',
            'type': 'Master',
            'study_duration': 5,
            'type_of_study': 'Civilian',
            'name': 'Kybernetická bezpečnost',
            'lastchange': datetime.datetime,
        }
    ]
    return data


@cache
def determineSubjects():
    # returns list of subjects
    data = [
        {
            'id': '4b773614-6d9e-11ed-a1eb-0242ac120099',
            'name': 'Analýza informačních zdrojů',
            'program_id': '4b883614-6d9e-11ed-a1eb-0242ac120002',
            'language_id': '4b883614-6d9e-11ed-a1eb-0242ac120003',
            'lastchange': datetime.datetime,
        }
    ]
    return data


@cache
def determineStudyLanguage():
    # returns list of languages
    data = [
        {
            'id': '4b883614-6d9e-11ed-a1eb-0242ac120003',
            'name': 'Česky',
            'semester_id': '4b883614-6d9e-11ed-a1eb-0242ac120004',
            'lastchange': datetime.datetime,
        }
    ]
    return data


@cache
def determineSemester():
    # returns list of languages
    data = [
        {
            'id': '4b883614-6d9e-11ed-a1eb-0242ac120004',
            'semester_number': 5,
            'credits': 30,
            'subject_id': '4b773614-6d9e-11ed-a1eb-0242ac120099',
            'classification_id': '4b773614-6d9e-11ed-a1eb-0242ac120088',
            'lastchange': datetime.datetime,
        }
    ]
    return data


@cache
def determineClassification():
    # returns list of classifications
    data = [
        {
            'id': '4b773614-6d9e-11ed-a1eb-0242ac120088',
            'name': 'Zkouška',
            'lastchange': datetime.datetime,
        },
        {
            'id': '4b773614-6d9e-11ed-a1eb-0242ac120077',
            'name': 'Zápočet',
            'lastchange': datetime.datetime,
        },
        {
            'id': '4b773614-6d9e-11ed-a1eb-0242ac120066',
            'name': 'Klasifikovaný zápočet',
            'lastchange': datetime.datetime,
        }
    ]
    return data


@cache
def determineTheme():
    # returns list of themes
    data = [
        {
            'id': '4b883614-6d9e-11ed-a1eb-0242ac120010',
            'name': 'Úvodní hodina',
            'semester_id': '4b883614-6d9e-11ed-a1eb-0242ac120004',
            'lastchange': datetime.datetime,
        },
        {
            'id': '4b883614-6d9e-11ed-a1eb-0242ac120011',
            'name': 'Analýza informací',
            'semester_id': '4b883614-6d9e-11ed-a1eb-0242ac120004',
            'lastchange': datetime.datetime,
        }
    ]
    return data


@cache
def determineThemeItem():
    # returns list of theme items
    data = [
        {
            'id': '4b883614-6d9e-12ed-a1eb-0242ac120012',
            'theme_id': '4b883614-6d9e-11ed-a1eb-0242ac120010',
            'type_id': '4b883614-6d9e-11ed-a1eb-0242ac120987',
            'semester_id': '4b883614-6d9e-11ed-a1eb-0242ac120004',
            'lessons': 5,
            'lastchange': datetime.datetime,
        }
    ]
    return data


def determineThemeTypes():
    # returns list of theme types
    data = [
        {
            'id': '4b883614-6d9e-11ed-a1eb-0242ac120987',
            'name': 'Neco',
            'semester_id': '4b883614-6d9e-11ed-a1eb-0242ac120004',
            'lastchange': datetime.datetime,
        }
    ]
    return data


###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################

import asyncio


async def ensureAllTypes(asyncSessionMaker):
    done = await asyncio.gather(
        putPredefinedStructuresIntoTable(
            asyncSessionMaker, StudyProgramModel, determineStudyPrograms
        ),
        putPredefinedStructuresIntoTable(
            asyncSessionMaker, SubjectModel, determineSubjects
        ),
        putPredefinedStructuresIntoTable(
            asyncSessionMaker, StudyLanguageModel, determineStudyLanguage
        ),
        putPredefinedStructuresIntoTable(
            asyncSessionMaker, SemesterModel, determineSemester
        ),
        putPredefinedStructuresIntoTable(
            asyncSessionMaker, ClassificationModel, determineClassification
        ),
        putPredefinedStructuresIntoTable(
            asyncSessionMaker, StudyThemeModel, determineTheme
        ),
        putPredefinedStructuresIntoTable(
            asyncSessionMaker, StudyThemeItemModel, determineThemeItem
        ),
        putPredefinedStructuresIntoTable(
            asyncSessionMaker, ThemeTypeModel, determineThemeTypes
        ),
    )
    return


async def putPredefinedStructuresIntoTable(asyncSessionMaker, DBModel, structureFunction):
    """Zabezpeci prvotni inicicalizaci typu externích ids v databazi
       DBModel zprostredkovava tabulku, je to sqlalchemy model
       structureFunction() dava data, ktera maji byt ulozena
    """
    # ocekavane typy 
    externalIdTypes = structureFunction()

    # dotaz do databaze
    stmt = select(DBModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = list(dbSet.scalars())

    # extrakce dat z vysledku dotazu
    # vezmeme si jen atributy name a id, id je typu uuid, tak jej zkovertujeme na string
    dbRowsDicts = [
        {'name': row.name, 'id': f'{row.id}'} for row in dbRows
    ]

    print(structureFunction, 'external id types found in database')
    print(dbRowsDicts)

    # vytahneme si vektor (list) id, ten pouzijeme pro operator in nize
    idsInDatabase = [row['id'] for row in dbRowsDicts]

    # zjistime, ktera id nejsou v databazi
    unsavedRows = list(filter(lambda row: not (row['id'] in idsInDatabase), externalIdTypes))
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

    # extrakce dat z vysledku dotazu
    dbRowsDicts = [
        {'name': row.name, 'id': f'{row.id}'} for row in dbRows
    ]

    print(structureFunction, 'found in database')
    print(dbRowsDicts)

    # znovu id, ktera jsou uz ulozena
    idsInDatabase = [row['id'] for row in dbRowsDicts]

    # znovu zaznamy, ktere dosud ulozeny nejsou, mely by byt ulozeny vsechny, takze prazdny list
    unsavedRows = list(filter(lambda row: not (row['id'] in idsInDatabase), externalIdTypes))

    # ted by melo byt pole prazdne
    print(structureFunction, 'not found in database')
    print(unsavedRows)
    if not (len(unsavedRows) == 0):
        print('SOMETHING is REALLY WRONG')

    print(structureFunction, 'Defined in database')
    # nyni vsechny entity mame v pameti a v databazi synchronizovane
    print(structureFunction())
    pass
