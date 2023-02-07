from gql_projects.DBDefinitions import (
    BaseModel,
    ProjectModel,
    ProjectTypeModel,
    FinanceModel,
    FinanceTypeModel,
    MilestoneModel,
    GroupModel,
)

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
        if resultCache.get("result", None) is None:
            resultCache["result"] = await asyncFunc()
        return resultCache["result"]

    return result


###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################


def determineProjectTypes():
    """Definuje zakladni typy roli"""
    projectTypes = [
        {"name": "shortTerm"},
        {"name": "mediumTerm"},
        {"name": "longTerm"},
    ]
    return projectTypes


def determineFinanceTypes():
    """Definuje zakladni typy financi"""
    financeTypes = [
        {"name": "travel_expenses"},
        {"name": "accomodation_expenses"},
        {"name": "other_expenses"},
    ]
    return financeTypes


def randomProject(name):
    """Náhodný projekt"""
    result = {
        "id": f"{uuid.uuid1()}",
        "name": f"{name}",
        #'startDate': randomDate()
        #'endDate': randomDate()
        "milestones": [
            # randomMilestone(i+1) for i in range(random.randint(3, 5))
        ],
    }
    return result


def randomMilestone(index):
    """Náhodný milestone"""
    result = {
        "name": f"Milestone {index}"
        #'startDate': randomDate(),
        #'endDAte' :  randomDate(),
    }
    return result


def randomFinance():
    """Náhodné finance"""
    result = {
        "name": "",
        "amount": random.randint(100, 20000),
    }
    return result


async def putPredefinedStructuresIntoTable(
    asyncSessionMaker, DBModel, structureFunction
):
    """Zabezpeci prvotni inicicalizaci typu externích ids v databazi
    DBModel zprostredkovava tabulku,
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


###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################


def randomUUID(limit):
    userIDs = [uuid.uuid4() for _ in range(limit)]
    return userIDs


def randomStartDate():
    base = date(2020, 1, 1)
    return base + timedelta(days=random.randint(1, 50))


def randomEndDate(startDate):
    return startDate + timedelta(days=random.randint(50, 100))


def randomProjectName():
    names = ["Informacni system", "Lesaci", "Wow grind", "SPZ", "Vault of Incarnates"]
    return random.choice(names)


projectTypesIDs = randomUUID(3)
financeTypesIDs = randomUUID(3)
projectIDs = randomUUID(2)
financeIDs = randomUUID(10)
milestoneIDs = randomUUID(10)
groupIDs = randomUUID(1)


def determineProjectTypes():
    """Definuje zakladni typy roli"""
    projectTypes = [
        {"id": projectTypesIDs[0], "name": "shortTerm"},
        {"id": projectTypesIDs[1], "name": "mediumTerm"},
        {"id": projectTypesIDs[2], "name": "longTerm"},
    ]
    return projectTypes


def determineFinanceTypes():
    """Definuje zakladni typy financi"""
    financeTypes = [
        {"id": financeTypesIDs[0], "name": "travelExpenses"},
        {"id": financeTypesIDs[1], "name": "accomodationExpenses"},
        {"id": financeTypesIDs[2], "name": "otherExpenses"},
    ]
    return financeTypes


def randomProject(id):
    """Nahodny projekt"""
    startDate = randomStartDate()
    return {
        "id": id,
        "name": randomProjectName(),
        "startDate": startDate,
        "endDate": randomEndDate(startDate),
        "projectType_id": random.choice(projectTypesIDs),
        "group_id": random.choice(groupIDs),
    }


def randomFinance(id, index):
    """Nahodne finance"""
    return {
        "id": id,
        "name": f"Finance {index}",
        "amount": random.randint(100, 20000),
        "project_id": random.choice(projectIDs),
        "financeType_id": random.choice(financeTypesIDs),
    }


def randomMilestone(id, index):
    """Nahodny milestone"""
    return {
        "id": id,
        "name": f"Milestone {index}",
        "date": randomStartDate(),
        "project_id": random.choice(projectIDs),
    }


def randomGroup(id):
    """Nahodna group"""
    return {"id": id}


def createDataStructureProjectTypes():
    projectTypes = determineProjectTypes()
    return projectTypes


def createDataStructureFinanceTypes():
    financeTypes = determineFinanceTypes()
    return financeTypes


def createDataStructureProjects():
    projects = [randomProject(id) for id in projectIDs]
    return projects


def createDataStructureFinances():
    index = 1
    finances = []
    for id in financeIDs:
        finances.append(randomFinance(id, index))
        index = index + 1

    return finances


def createDataStructureMilestones():
    index = 1
    milestones = []
    for id in milestoneIDs:
        milestones.append(randomMilestone(id, index))
        index = index + 1

    return milestones


def createDataStructureGroups():
    groups = [randomGroup(id) for id in groupIDs]
    return groups


async def randomDataStructure(session):

    projectTypes = createDataStructureProjectTypes()
    projectTypesToAdd = [ProjectTypeModel(**record) for record in projectTypes]
    async with session.begin():
        session.add_all(projectTypesToAdd)
    await session.commit()

    financeTypes = createDataStructureFinanceTypes()
    financeTypesToAdd = [FinanceTypeModel(**record) for record in financeTypes]
    async with session.begin():
        session.add_all(financeTypesToAdd)
    await session.commit()

    projects = createDataStructureProjects()
    projectsToAdd = [ProjectModel(**record) for record in projects]
    async with session.begin():
        session.add_all(projectsToAdd)
    await session.commit()

    finances = createDataStructureFinances()
    financesToAdd = [FinanceModel(**record) for record in finances]
    async with session.begin():
        session.add_all(financesToAdd)
    await session.commit()

    milestones = createDataStructureMilestones()
    milestonesToAdd = [MilestoneModel(**record) for record in milestones]
    async with session.begin():
        session.add_all(milestonesToAdd)
    await session.commit()

    groups = createDataStructureGroups()
    groupsToAdd = [GroupModel(**record) for record in groups]
    async with session.begin():
        session.add_all(groupsToAdd)
    await session.commit()
