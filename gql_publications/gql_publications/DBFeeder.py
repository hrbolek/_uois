from functools import cache
from gql_publications.DBDefinitions import (
    PublicationCategoryModel,
    PublicationTypeModel,
    PublicationModel,
    AuthorModel,
    SubjectModel
)

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
# zde definujte sva systemova data
#
###########################################################################################################################


@cache
def types1():
    # krome id a name, lze mit i dalsi prvky, napriklad cizi klice...
    data = [
        {"id": "282e67ec-6d9e-11ed-a1eb-0242ac120002", "name": "typeA"},
        {"id": "282e6e86-6d9e-11ed-a1eb-0242ac120002", "name": "typeB"},
        {"id": "282e7002-6d9e-11ed-a1eb-0242ac120002", "name": "typeC"},
    ]
    return data


@cache
def types2():
    # krome id a name, lze mit i dalsi prvky, napriklad cizi klice...
    data = [
        {"id": "4b883614-6d9e-11ed-a1eb-0242ac120002", "name": "typeX"},
        {"id": "4b8838a8-6d9e-11ed-a1eb-0242ac120002", "name": "typeY"},
        {"id": "4b883a38-6d9e-11ed-a1eb-0242ac120002", "name": "typeZ"},
    ]
    return data


###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################

import asyncio

def get_demodata(asyncSessionMaker):
    pass

async def predefineAllDataStructures(asyncSessionMaker):
    #
    # asyncio.gather(
    #   putPredefinedStructuresIntoTable(asyncSessionMaker, Types1Model, types1), # prvni
    #   putPredefinedStructuresIntoTable(asyncSessionMaker, Types1Model, types2)  # druha ...
    # )
    #
    #
    return


async def putPredefinedStructuresIntoTable(
    asyncSessionMaker, DBModel, structureFunction
):
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
    dbRowsDicts = [{"name": row.name, "id": f"{row.id}"} for row in dbRows]

    print(structureFunction, "external id types found in database")
    print(dbRowsDicts)

    # vytahneme si vektor (list) id, ten pouzijeme pro operator in nize
    idsInDatabase = [row["id"] for row in dbRowsDicts]

    # zjistime, ktera id nejsou v databazi
    unsavedRows = list(
        filter(lambda row: not (row["id"] in idsInDatabase), externalIdTypes)
    )
    print(structureFunction, "external id types not found in database")
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
    dbRowsDicts = [{"name": row.name, "id": f"{row.id}"} for row in dbRows]

    print(structureFunction, "found in database")
    print(dbRowsDicts)

    # znovu id, ktera jsou uz ulozena
    idsInDatabase = [row["id"] for row in dbRowsDicts]

    # znovu zaznamy, ktere dosud ulozeny nejsou, mely by byt ulozeny vsechny, takze prazdny list
    unsavedRows = list(
        filter(lambda row: not (row["id"] in idsInDatabase), externalIdTypes)
    )

    # ted by melo byt pole prazdne
    print(structureFunction, "not found in database")
    print(unsavedRows)
    if not (len(unsavedRows) == 0):
        print("SOMETHING is REALLY WRONG")

    print(structureFunction, "Defined in database")
    # nyni vsechny entity mame v pameti a v databazi synchronizovane
    print(structureFunction())
    pass


from gql_publications.DBDefinitions import (
    BaseModel,
    PublicationModel,
    AuthorModel,
    PublicationTypeModel,
)

limit = 10
import uuid


def randomUUID():
    userIDs = [uuid.uuid4() for _ in range(limit)]
    return userIDs


def randomAuthor(id):
    return {
        "id": id,
        "user_id": random.choice(authorIDs),
        "publication_id": random.choice(publicationIDs),
        "order": randomOrder(),
        "share": randomShare(),
        "externalId": "",
    }


def randomPublicationName():
    publicationNames = [
        "Database systems",
        "Data Mining",
        "Algorithms and Data Structures",
        "Web Data Mining",
        "Zaklady siti",
        "Telekomunikacni technika",
    ]
    return random.choice(publicationNames)


def randomReference():

    return "Monografie: FINKE, Manfred. Sulzbach im 17. Jahrhundert : zur Kulturgeschichte einer süddeutschen Residenz. Regensburg : Friedrich Pustet, 1998. 404 s. ISBN 3-7917-1596-8."


def randomPlace():
    places = ["Brno", "Praha", "Ostrava", "Plzen", "Olomouc"]
    return random.choice(places)


def randomPublishedDate():
    defualt_date = date(2015, 6, 3)
    return defualt_date + timedelta(days=random.randint(1, 100))


def randomShare():
    return int(100 / (random.randint(1, 4)))


def randomOrder():
    return random.randint(1, 2)


def randomPublicationTypes(ids):
    types = [
        "Skripta",
        "Clanek v odbornem periodiku",
        "Konferencni prispevek",
        "Clanek",
        "Recenze",
    ]

    return [{"id": id, "type": type} for id, type in zip(ids, types)]


def randomPublications(id):
    return {
        "id": id,
        "name": randomPublicationName(),
        "publication_type_id": random.choice(publicationTypesIds),
        "place": randomPlace(),
        "published_date": randomPublishedDate(),
        "reference": randomReference(),
        "valid": True,
        "externalId": "",
    }


from sqlalchemy.future import select


def createDataStructurePublications():
    publications = [randomPublications(id) for id in publicationIDs]
    return publications


def createDataStructureAuthors():
    authors = [randomAuthor(id) for id in authorIDs]
    return authors


def createDataStructurePublicationTypes():
    publicationsTypes = randomPublicationTypes(publicationTypesIds)
    return publicationsTypes


userIDs = randomUUID()
authorIDs = randomUUID()
publicationIDs = randomUUID()
publicationTypesIds = randomUUID()


# with open('publications_dataset.json', 'w') as outfile:
#     json.dump(dataset, outfile,cls=UUIDEncoder)

from sqlalchemy.future import select


async def randomDataStructure(session):

    publication_types = createDataStructurePublicationTypes()
    publicationsTypesToAdd = [
        PublicationTypeModel(**record) for record in publication_types
    ]

    async with session.begin():
        session.add_all(publicationsTypesToAdd)
    await session.commit()

    publications = createDataStructurePublications()
    publicationsToAdd = [PublicationModel(**record) for record in publications]
    async with session.begin():
        session.add_all(publicationsToAdd)
    await session.commit()

    authors = createDataStructureAuthors()
    authorsToAdd = [AuthorModel(**record) for record in authors]
    async with session.begin():
        session.add_all(authorsToAdd)
    await session.commit()


import os
import json
from uoishelpers.feeders import ImportModels
import datetime

def get_demodata():
    def datetime_parser(json_dict):
        for (key, value) in json_dict.items():
            if key in ["startdate", "enddate", "lastchange", "created", "published_date"]:
                dateValue = datetime.datetime.fromisoformat(value)
                dateValueWOtzinfo = dateValue.replace(tzinfo=None)
                json_dict[key] = dateValueWOtzinfo
        return json_dict


    with open("./systemdata.json", "r") as f:
        jsonData = json.load(f, object_hook=datetime_parser)

    return jsonData

async def initDB(asyncSessionMaker):

    defaultNoDemo = "False"
    if defaultNoDemo == os.environ.get("DEMO", defaultNoDemo):
        dbModels = [
            PublicationCategoryModel,
            PublicationTypeModel,
            PublicationModel,
        ]
    else:
        dbModels = [
            PublicationCategoryModel,
            PublicationTypeModel,
            PublicationModel,
            AuthorModel,
            SubjectModel
        ]

    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass