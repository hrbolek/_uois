from doctest import master
from functools import cache
from gql_surveys.DBDefinitions import BaseModel

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


from gql_surveys.DBDefinitions import (
    BaseModel,
    QuestionTypeModel,
    QuestionModel,
    AnswerModel,
    SurveyModel,
)


@cache
def determineQuestionTypes():
    questionTypes = [
        {"id": "ad0f53fb-240b-47de-ab1d-871bbde6f973", "name": "Uzavřené"},
        {"id": "949d74a2-63b1-4478-82f1-e025d8bc6c8b", "name": "Otevřené"},
        {"id": "2a6a1731-1efa-4644-a1d8-5848e4b29ce5", "name": "Škála"},
    ]
    return questionTypes


import datetime

def get_demodata():
    userID1 = "8188a23c-8fd4-11ed-a6d4-0242ac110002"
    userID2 = "81701780-8fd4-11ed-a6d4-0242ac110002"
    questionTypes = determineQuestionTypes()
    result = {
        "surveyquestiontypes": questionTypes,
        "surveys": [
            {"id": "910d54a9-7f2e-41ca-b811-3c600ef82fda", "name": "Studentské hodnocení"}
        ],
        "surveyquestions": [
            {
                "id": "5b7e4ae7-9bb9-4e2f-829b-c2763ac1092e",
                "name": "Jak hodnotíte předmět xy",
                "order": 1,
                "lastchange": datetime.datetime.now(),
                "survey_id": "910d54a9-7f2e-41ca-b811-3c600ef82fda",
                "type_id": "2a6a1731-1efa-4644-a1d8-5848e4b29ce5",
            },  # škála
            {
                "id": "984120da-ab92-44bd-9389-5f47ed9b3225",
                "name": "Jak hodnotíte výuku předmětu xy",
                "order": 2,
                "lastchange": datetime.datetime.now(),
                "survey_id": "910d54a9-7f2e-41ca-b811-3c600ef82fda",
                "type_id": "949d74a2-63b1-4478-82f1-e025d8bc6c8b",
            },  # otevřené
            {
                "id": "2b27adcc-0b7e-40c4-a430-8e0aa551ae3e",
                "name": "Který předmět považujete za nejvíc přínosný?",
                "order": 3,
                "lastchange": datetime.datetime.now(),
                "survey_id": "910d54a9-7f2e-41ca-b811-3c600ef82fda",
                "type_id": "ad0f53fb-240b-47de-ab1d-871bbde6f973",
            },  # uzavřené
        ],
        "surveyanswers": [
            # user 1
            {
                "id": "ad0f53fb-240b-47de-ab1d-871bbde6f972",
                "value": "8",
                "aswered": True,
                "expired": False,
                "user_id": userID1,
                "question_id": "5b7e4ae7-9bb9-4e2f-829b-c2763ac1092e",
            },
            {
                "id": "dd7dc78f-534d-4c33-a979-2dfd41a53a84",
                "value": "OK",
                "aswered": True,
                "expired": False,
                "user_id": userID1,
                "question_id": "984120da-ab92-44bd-9389-5f47ed9b3225",
            },
            {
                "id": "bb0cd1b9-15ba-4f80-a6a0-7a9dc65deb13",
                "value": "Analýza informačních zdrojů",
                "aswered": True,
                "expired": False,
                "user_id": userID1,
                "question_id": "2b27adcc-0b7e-40c4-a430-8e0aa551ae3e",
            },
            # user 2
            {
                "id": "e054d1a5-f259-429d-9f7a-f35d55caf2ab",
                "value": None,
                "aswered": False,
                "expired": False,
                "user_id": userID2,
                "question_id": "5b7e4ae7-9bb9-4e2f-829b-c2763ac1092e",
            },
            {
                "id": "600a7008-44b6-46e9-a546-d934731a0603",
                "value": None,
                "aswered": True,
                "expired": False,
                "user_id": userID2,
                "question_id": "984120da-ab92-44bd-9389-5f47ed9b3225",
            },
            {
                "id": "ed33c145-c295-41c2-be49-5037837ee974",
                "value": None,
                "aswered": True,
                "expired": False,
                "user_id": userID2,
                "question_id": "2b27adcc-0b7e-40c4-a430-8e0aa551ae3e",
            },
        ]
    }

    return result


async def randomSurveyData(session):
    userID1 = "8188a23c-8fd4-11ed-a6d4-0242ac110002"
    userID2 = "81701780-8fd4-11ed-a6d4-0242ac110002"
    users = [
        {"id": userID1},  # user 1
        {"id": userID2},  # user 2
    ]
    surveys = [
        {"id": "910d54a9-7f2e-41ca-b811-3c600ef82fda", "name": "Studentské hodnocení"}
    ]
    questions = [
        {
            "id": "5b7e4ae7-9bb9-4e2f-829b-c2763ac1092e",
            "name": "Jak hodnotíte předmět xy",
            "order": 1,
            "lastchange": datetime.datetime.now(),
            "survey_id": "910d54a9-7f2e-41ca-b811-3c600ef82fda",
            "type_id": "2a6a1731-1efa-4644-a1d8-5848e4b29ce5",
        },  # škála
        {
            "id": "984120da-ab92-44bd-9389-5f47ed9b3225",
            "name": "Jak hodnotíte výuku předmětu xy",
            "order": 2,
            "lastchange": datetime.datetime.now(),
            "survey_id": "910d54a9-7f2e-41ca-b811-3c600ef82fda",
            "type_id": "949d74a2-63b1-4478-82f1-e025d8bc6c8b",
        },  # otevřené
        {
            "id": "2b27adcc-0b7e-40c4-a430-8e0aa551ae3e",
            "name": "Který předmět považujete za nejvíc přínosný?",
            "order": 3,
            "lastchange": datetime.datetime.now(),
            "survey_id": "910d54a9-7f2e-41ca-b811-3c600ef82fda",
            "type_id": "ad0f53fb-240b-47de-ab1d-871bbde6f973",
        },  # uzavřené
    ]
    answers = [
        # user 1
        {
            "id": "ad0f53fb-240b-47de-ab1d-871bbde6f973",
            "value": "8",
            "aswered": True,
            "expired": False,
            "user_id": userID1,
            "question_id": "5b7e4ae7-9bb9-4e2f-829b-c2763ac1092e",
        },
        {
            "id": "dd7dc78f-534d-4c33-a979-2dfd41a53a84",
            "value": "OK",
            "aswered": True,
            "expired": False,
            "user_id": userID1,
            "question_id": "984120da-ab92-44bd-9389-5f47ed9b3225",
        },
        {
            "id": "bb0cd1b9-15ba-4f80-a6a0-7a9dc65deb13",
            "value": "Analýza informačních zdrojů",
            "aswered": True,
            "expired": False,
            "user_id": userID1,
            "question_id": "2b27adcc-0b7e-40c4-a430-8e0aa551ae3e",
        },
        # user 2
        {
            "id": "e054d1a5-f259-429d-9f7a-f35d55caf2ab",
            "value": None,
            "aswered": False,
            "expired": False,
            "user_id": userID2,
            "question_id": "5b7e4ae7-9bb9-4e2f-829b-c2763ac1092e",
        },
        {
            "id": "600a7008-44b6-46e9-a546-d934731a0603",
            "value": None,
            "aswered": True,
            "expired": False,
            "user_id": userID2,
            "question_id": "984120da-ab92-44bd-9389-5f47ed9b3225",
        },
        {
            "id": "ed33c145-c295-41c2-be49-5037837ee974",
            "value": None,
            "aswered": True,
            "expired": False,
            "user_id": userID2,
            "question_id": "2b27adcc-0b7e-40c4-a430-8e0aa551ae3e",
        },
    ]
    asyncSessionMaker = lambda: session
    #await putPredefinedStructuresIntoTable(asyncSessionMaker, UserModel, lambda: users)
    await putPredefinedStructuresIntoTable(
        asyncSessionMaker, SurveyModel, lambda: surveys
    )
    await putPredefinedStructuresIntoTable(
        asyncSessionMaker, QuestionModel, lambda: questions
    )
    await putPredefinedStructuresIntoTable(
        asyncSessionMaker, AnswerModel, lambda: answers
    )
    return surveys[0]["id"]


async def SystemInitialization(asyncSessionMaker):
    await putPredefinedStructuresIntoTable(
        asyncSessionMaker, QuestionTypeModel, determineQuestionTypes
    )


async def putPredefinedStructuresIntoTable(
    asyncSessionMaker, DBModel, structureFunction
):
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

    # dotaz do databaze
    stmt = select(DBModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = list(dbSet.scalars())

    # extrakce dat z vysledku dotazu
    # vezmeme si jen atribut id, id je typu uuid, tak jej zkovertujeme na string
    idsInDatabase = [f"{row.id}" for row in dbRows]

    # zjistime, ktera id nejsou v databazi
    unsavedRows = list(
        filter(lambda row: not (f'{row["id"]}' in idsInDatabase), externalIdTypes)
    )

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
        if "_chunk" in unsavedRows[0]:
            # existuje informace o rozfazovani ukladani do tabulky
            nextPhase = [*unsavedRows]
            while len(nextPhase) > 0:
                # zjistime nejmensi cislo poradi ukladani
                chunkNumber = min(map(lambda item: item["_chunk"], nextPhase))

                print(tableName, "chunkNumber", chunkNumber)

                # filtrujeme radky, ktere maji toto cislo
                toSave = list(
                    filter(lambda item: item["_chunk"] == chunkNumber, nextPhase)
                )
                # ostatni nechame na pozdeji
                nextPhase = list(
                    filter(lambda item: item["_chunk"] != chunkNumber, nextPhase)
                )
                # ulozime vybrane
                await saveChunk(toSave)
        else:
            # vsechny zaznamy mohou byt ulozeny soucasne
            await saveChunk(unsavedRows)

    # jeste jednou se dotazeme do databaze
    stmt = select(DBModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = dbSet.scalars()

    # extrakce dat z vysledku dotazu
    idsInDatabase = [f"{row.id}" for row in dbRows]

    # znovu zaznamy, ktere dosud ulozeny nejsou, mely by byt ulozeny vsechny, takze prazdny list
    unsavedRows = list(
        filter(lambda row: not (f'{row["id"]}' in idsInDatabase), externalIdTypes)
    )

    # ted by melo byt pole prazdne
    if not (len(unsavedRows) == 0):
        print("SOMETHING is REALLY WRONG")

    # print(structureFunction(), 'On the input')
    # print(dbRowsDicts, 'Defined in database')
    # nyni vsechny entity mame v pameti a v databazi synchronizovane
    # print(structureFunction())
    pass
