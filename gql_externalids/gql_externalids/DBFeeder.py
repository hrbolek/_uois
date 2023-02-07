from doctest import master
from functools import cache
from gql_externalids.DBDefinitions import BaseModel, ExternalIdTypeModel

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
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################


@cache
def determineExternalIdsTypes():
    """Definuje zakladni typy externich Id a udrzuje je v pameti.
    Pozor, data se v databazi mohou zmenit! Pouzivat obezretne!
    """

    idTypes = [
        {"name": "UOApl", "id": "1db4ac10-67e8-11ed-9022-0242ac120002"},
        {"name": "VVP", "id": "1db4b020-67e8-11ed-9022-0242ac120002"},
        {"name": "SCOPUS", "id": "1db4b188-67e8-11ed-9022-0242ac120002"},
        {"name": "WoS", "id": "1db4b2be-67e8-11ed-9022-0242ac120002"},
        {"name": "ResearcherId", "id": "1db4b3d6-67e8-11ed-9022-0242ac120002"},
    ]
    return idTypes


from sqlalchemy.future import select


async def createSystemDataStructureExternalIdTypes(asyncSessionMaker):
    """Zabezpeci prvotni inicicalizaci typu externích ids v databazi"""
    # ocekavane typy
    externalIdTypes = determineExternalIdsTypes()

    # dotaz do databaze
    stmt = select(ExternalIdTypeModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = list(dbSet.scalars())

    # extrakce dat z vysledku dotazu
    # vezmeme si jen atributy name a id, id je typu uuid, tak jej zkovertujeme na string
    dbRowsDicts = [{"name": row.name, "id": f"{row.id}"} for row in dbRows]

    print("external id types found in database")
    print(dbRowsDicts)

    # vytahneme si vektor (list) id, ten pouzijeme pro operator in nize
    idsInDatabase = [row["id"] for row in dbRowsDicts]

    # zjistime, ktera id nejsou v databazi
    unsavedRows = list(
        filter(lambda row: not (row["id"] in idsInDatabase), externalIdTypes)
    )
    print("external id types not found in database")
    print(unsavedRows)

    # pro vsechna neulozena id vytvorime entity
    rowsToAdd = [
        ExternalIdTypeModel(name=row["name"], id=row["id"]) for row in unsavedRows
    ]
    print(rowsToAdd)
    print(len(rowsToAdd))

    # a vytvorene entity jednou operaci vlozime do databaze
    async with asyncSessionMaker() as session:
        async with session.begin():
            session.add_all(rowsToAdd)
        await session.commit()

    # jeste jednou se dotazeme do databaze
    stmt = select(ExternalIdTypeModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = dbSet.scalars()

    # extrakce dat z vysledku dotazu
    dbRowsDicts = [{"name": row.name, "id": f"{row.id}"} for row in dbRows]

    print("roletypes found in database")
    print(dbRowsDicts)

    # znovu id, ktera jsou uz ulozena
    idsInDatabase = [row["id"] for row in dbRowsDicts]

    # znovu zaznamy, ktere dosud ulozeny nejsou, mely by byt ulozeny vsechny, takze prazdny list
    unsavedRows = list(
        filter(lambda row: not (row["id"] in idsInDatabase), externalIdTypes)
    )

    # ted by melo byt pole prazdne
    print("roletypes not found in database")
    print(unsavedRows)
    if not (len(unsavedRows) == 0):
        print("SOMETHING is REALLY WRONG")

    print("External id types in database")
    # nyni vsechny entity mame v pameti a v databazi synchronizovane
    print(determineExternalIdsTypes())
    pass
