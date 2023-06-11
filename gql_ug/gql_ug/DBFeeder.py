from functools import cache
from gql_ug.DBDefinitions import (
    GroupTypeModel, 
    RoleTypeModel,
    RoleCategoryModel,
    UserModel,
    GroupModel,
    MembershipModel,
    RoleModel,
)


import uuid

import random
import itertools

def uuidStr():
    return f"{uuid.uuid1()}"

@cache
def determineRoleTypes():
    """Definuje zakladni typy roli a udrzuje je v pameti"""
    roleTypes = [
        {
            "name": "rektor",
            "name_en": "rector",
            "id": "ae3f0d74-6159-11ed-b753-0242ac120003",
        },
        {
            "name": "prorektor",
            "name_en": "vicerector",
            "id": "ae3f2886-6159-11ed-b753-0242ac120003",
        },
        {
            "name": "děkan",
            "name_en": "dean",
            "id": "ae3f2912-6159-11ed-b753-0242ac120003",
        },
        {
            "name": "proděkan",
            "name_en": "vicedean",
            "id": "ae3f2980-6159-11ed-b753-0242ac120003",
        },
        {
            "name": "vedoucí katedry",
            "name_en": "head of department",
            "id": "ae3f29ee-6159-11ed-b753-0242ac120003",
        },
        {
            "name": "vedoucí učitel",
            "name_en": "leading teacher",
            "id": "ae3f2a5c-6159-11ed-b753-0242ac120003",
        },
        {
            "name": "garant",
            "name_en": "grant",
            "id": "5f0c247e-931f-11ed-9b95-0242ac110002",
        },
        {
            "name": "garant (zástupce)",
            "name_en": "grant (deputy)",
            "id": "5f0c2532-931f-11ed-9b95-0242ac110002",
        },
        {
            "name": "garant předmětu",
            "name_en": "subject's grant",
            "id": "5f0c255a-931f-11ed-9b95-0242ac110002",
        },
        {
            "name": "přednášející",
            "name_en": "lecturer",
            "id": "5f0c2578-931f-11ed-9b95-0242ac110002",
        },
        {
            "name": "cvičící",
            "name_en": "trainer",
            "id": "5f0c2596-931f-11ed-9b95-0242ac110002",
        },
    ]
    return roleTypes

import datetime

@cache
def determineGroupTypes():
    """Definuje zakladni typy skupin a udrzuje je v pameti"""
    groupTypes = [
        {
            "name": "univerzita",
            "name_en": "university",
            "ex_type": "100",
            "id": "cd49e152-610c-11ed-9f29-001a7dda7110",
        },
        {
            "name": "fakulta",
            "name_en": "faculty",
            "ex_type": "300",
            "id": "cd49e153-610c-11ed-bf19-001a7dda7110",
        },
        {
            "name": "ústav",
            "name_en": "institute",
            "ex_type": "400",
            "id": "cd49e154-610c-11ed-bdbf-001a7dda7110",
        },
        {
            "name": "centrum",
            "name_en": "centre",
            "ex_type": "410",
            "id": "cd49e155-610c-11ed-bdbf-001a7dda7110",
        },
        {
            "name": "katedra",
            "name_en": "department",
            "ex_type": "500",
            "id": "cd49e155-610c-11ed-844e-001a7dda7110",
        },
        {
            "name": "oddělení",
            "name_en": "section",
            "ex_type": "600",
            "id": "cd49e156-610c-11ed-87ef-001a7dda7110",
        },
        {
            "name": "studijní skupina",
            "name_en": "study group",
            "ex_type": "001",
            "id": "cd49e157-610c-11ed-9312-001a7dda7110",
        },
        {
            "name": "stalý stav",
            "name_en": "all teachers",
            "ex_type": "200",
            "id": "cd49e157-610c-11ed-9f29-001a7dda7110",
        },
        {
            "name": "studenti",
            "name_en": "all students",
            "ex_type": "002",
            "id": "0eb35718-615b-11ed-b753-0242ac120003",
        },
        {
            "id": "b1bedec8-931f-11ed-9b95-0242ac110002",
            "name": "garance programu",
            "name_en": "program grants",
        },
        {
            "id": "b1bedf72-931f-11ed-9b95-0242ac110002",
            "name": "garance předmětu",
            "name_en": "subject grants",
        },
    ]

    return groupTypes

def get_demodata():

    roleTypes = determineRoleTypes()
    groupTypes = determineGroupTypes()

    result = {
        # 'roletypes': [
        #     {'name': 'rektor', 'name_en': 'rector', 'id': 'ae3f0d74-6159-11ed-b753-0242ac120003'},
        #     {'name': 'prorektor', 'name_en': 'vicerector', 'id': 'ae3f2886-6159-11ed-b753-0242ac120003'},
        #     {'name': 'děkan', 'name_en': 'dean', 'id': 'ae3f2912-6159-11ed-b753-0242ac120003'},
        #     {'name': 'proděkan', 'name_en': 'vicedean', 'id': 'ae3f2980-6159-11ed-b753-0242ac120003'},
        #     {'name': 'vedoucí katedry', 'name_en': 'head of department', 'id': 'ae3f29ee-6159-11ed-b753-0242ac120003'},
        # ],
        # 'grouptypes': [
        #     {"name": "univerzita", "name_en": "university", "ex_type": "100", "id": "cd49e152-610c-11ed-9f29-001a7dda7110"},
        #     {"name": "fakulta", "name_en": "faculty", "ex_type": "300", "id": "cd49e153-610c-11ed-bf19-001a7dda7110"},
        #     {"name": "katedra", "name_en": "department", "ex_type": "500", "id": "cd49e155-610c-11ed-844e-001a7dda7110"},
        #     {"name": "studijní skupina", "name_en": "study group", "ex_type": "001", "id": "cd49e157-610c-11ed-9312-001a7dda7110"},
        # ],
        "roletypes": [*roleTypes],
        "rolecategories": [
            {"id": "a36fc45f-700a-4d09-966e-1d309e3deed4", "name": "obecné role", "name": "general roles"}
        ],
        "grouptypes": [*groupTypes],
        "users": [
            {
                "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
                "name": "John",
                "surname": "Newbie",
                "email": "john.newbie@world.com"
            },
            {
                "id": "2d9dc868-a4a2-11ed-b9df-0242ac120003",
                "name": "Julia",
                "surname": "Newbie",
                "email": "julia.newbie@world.com",
            },
            {
                "id": "2d9dc9a8-a4a2-11ed-b9df-0242ac120003",
                "name": "Johnson",
                "surname": "Newbie",
                "email": "johnson.newbie@world.com",
            },
            {
                "id": "2d9dcbec-a4a2-11ed-b9df-0242ac120003",
                "name": "Jepeto",
                "surname": "Newbie",
                "email": "jepeto.newbie@world.com",
            },
        ],
        "groups": [
            {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni",
                "lastchange": datetime.datetime.now(),
                "valid": True,
                "grouptype_id": "cd49e152-610c-11ed-9f29-001a7dda7110",
                "mastergroup_id": None,
            },
            {
                "id": "2d9dced0-a4a2-11ed-b9df-0242ac120003",
                "name": "Fac",
                "lastchange": datetime.datetime.now(),
                "valid": True,
                "grouptype_id": "cd49e153-610c-11ed-bf19-001a7dda7110",
                "mastergroup_id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
            },
            {
                "id": "2d9dd1c8-a4a2-11ed-b9df-0242ac120003",
                "name": "Dep",
                "lastchange": datetime.datetime.now(),
                "valid": True,
                "grouptype_id": "cd49e155-610c-11ed-844e-001a7dda7110",
                "mastergroup_id": "2d9dced0-a4a2-11ed-b9df-0242ac120003",
            },
            {
                "id": "2d9dd2ea-a4a2-11ed-b9df-0242ac120003",
                "name": "St",
                "lastchange": datetime.datetime.now(),
                "valid": False,
                "grouptype_id": "cd49e157-610c-11ed-9312-001a7dda7110",
                "mastergroup_id": "2d9dced0-a4a2-11ed-b9df-0242ac120003",
            },
        ],
        "memberships": [
            {
                "id": "7cea8596-a4a2-11ed-b9df-0242ac120003",
                "user_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
                "group_id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "valid": True
            }
        ],
        "roles": [
            {
                "id": "7cea8802-a4a2-11ed-b9df-0242ac120003",
                "user_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
                "group_id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "roletype_id": "ae3f0d74-6159-11ed-b753-0242ac120003",
                "startdate": datetime.datetime.now(),
                "enddate": datetime.datetime.now(),
                "valid": True,
            }
        ],
    }
    return result

from uoishelpers.feeders import ImportModels

def randomUniversity(name):
    """Generuje strukturu skupin na urovni univerzity (fakulty, katedry) a jejich akademicke pracovniky ve forme json"""
    result = {
        "name": f"{name}",
        "grouptype": {"name": "univerzita"},
        "valid": True,
        "subgroups": [randomFaculty(i + 1) for i in range(random.randint(3, 5))],
        "roles": [],
        "users": [],
    }

    result["users"] = [
        user for subgroup in result["subgroups"] for user in subgroup["users"]
    ]

    universityRoles = [
        {"name": "rektor"},
        {"name": "prorektor"},
        {"name": "prorektor"},
        {"name": "prorektor"},
        {"name": "prorektor"},
    ]

    dbRoles = determineRoleTypes()
    universityRolesLinkedToDb = [
        next(filter(lambda dbrole: dbrole["name"] == role["name"], dbRoles))
        for role in universityRoles
    ]
    result["roles"] = [
        {"roletype": role, "user": random.choice(result["users"]), "group": result, "valid": True }
        for role in universityRolesLinkedToDb
    ]

    return result


def randomFaculty(index):
    """Generuje"""
    result = {
        "name": f"Faculty {index}",
        "grouptype": {"name": "fakulta"},
        "valid": True,
        "subgroups": [
            randomDepartment(index, i + 1) for i in range(random.randint(8, 15))
        ],
        "roles": [],
        "users": [],
    }

    studentGroups = [randomStudyGroup(dep) for dep in result["subgroups"]]
    result["subgroups"].extend(studentGroups)

    result["users"] = [
        user for subgroup in result["subgroups"] for user in subgroup["users"]
    ]

    facultyRoles = [
        {"name": "děkan"},
        {"name": "proděkan"},
        {"name": "proděkan"},
        {"name": "proděkan"},
    ]

    dbRoles = determineRoleTypes()
    facultyRolesLinkedToDb = [
        next(filter(lambda dbrole: dbrole["name"] == role["name"], dbRoles))
        for role in facultyRoles
    ]
    result["roles"] = [
        {"roletype": role, "user": random.choice(result["users"]), "group": result, "valid": True }
        for role in facultyRolesLinkedToDb
    ]
    # result['users'] = itertools.chain(map(result['subgroups'], lambda group: group['users']))
    return result


def randomStudyGroup(department):
    result = {
        "name": department["name"].replace("Department", "Studenti"),
        "grouptype": {"name": "studijní skupina"},
        "valid": True,
        "subgroups": [],
        "roles": [],
        "users": [randomUser() for i in range(random.randint(15, 20))],
    }
    return result


def randomDepartment(indexA, indexB):
    """"""
    result = {
        "name": f"Department {indexA}-{indexB}",
        "grouptype": {"name": "katedra"},
        "valid": True,
        "subgroups": [],
        "roles": [],
        "users": [randomUser() for i in range(random.randint(15, 20))],
    }
    result["roles"].append(
        {
            "roletype": {"name": "vedoucí katedry"},
            "user": random.choice(result["users"]),
            "group": result,
            "valid": True,
        }
    )
    return result


def randomUser():
    """Nahodny uzivatel"""
    surNames = [
        "Novák",
        "Nováková",
        "Svobodová",
        "Svoboda",
        "Novotná",
        "Novotný",
        "Dvořáková",
        "Dvořák",
        "Černá",
        "Černý",
        "Procházková",
        "Procházka",
        "Kučerová",
        "Kučera",
        "Veselá",
        "Veselý",
        "Horáková",
        "Krejčí",
        "Horák",
        "Němcová",
        "Marková",
        "Němec",
        "Pokorná",
        "Pospíšilová",
        "Marek",
    ]

    names = [
        "Jiří",
        "Jan",
        "Petr",
        "Jana",
        "Marie",
        "Josef",
        "Pavel",
        "Martin",
        "Tomáš",
        "Jaroslav",
        "Eva",
        "Miroslav",
        "Hana",
        "Anna",
        "Zdeněk",
        "Václav",
        "Michal",
        "František",
        "Lenka",
        "Kateřina",
        "Lucie",
        "Jakub",
        "Milan",
        "Věra",
        "Alena",
    ]

    name1 = random.choice(names)
    name2 = random.choice(names)
    name3 = random.choice(surNames)
    return {
        "name": f"{name1} {name2}",
        "surname": f"{name3}",
        "email": f"{name1}.{name2}.{name3}@university.world",
        "valid": True,
    }


from sqlalchemy.future import select


async def createSystemDataStructureRoleTypes(asyncSessionMaker):
    """Zabezpeci prvotni inicicalizaci typu roli v databazi"""
    # ocekavane typy roli
    roleTypes = determineRoleTypes()

    # dotaz do databaze
    stmt = select(RoleTypeModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRoleTypes = dbSet.scalars()

    # extrakce dat z vysledku dotazu
    dbRoleTypes = [{"name": role.name, "id": role.id} for role in dbRoleTypes]

    print("roletypes found in database")
    print(dbRoleTypes)

    roleTypeNamesInDatabase = [roleType["name"] for roleType in dbRoleTypes]

    unsavedRoleTypes = list(
        filter(
            lambda roleType: not (roleType["name"] in roleTypeNamesInDatabase),
            roleTypes,
        )
    )
    print("roletypes not found in database")
    print(unsavedRoleTypes)

    RoleTypeModelToAdd = [
        RoleTypeModel(
            name_en=roleType["name_en"], name=roleType["name"], id=roleType["id"]
        )
        for roleType in unsavedRoleTypes
    ]
    print(RoleTypeModelToAdd)
    print(len(RoleTypeModelToAdd))

    async with asyncSessionMaker() as session:
        async with session.begin():
            session.add_all(RoleTypeModelToAdd)
        await session.commit()

    # jeste jednou se dotazeme do databaze
    stmt = select(RoleTypeModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRoleTypes = dbSet.scalars()

    # extrakce dat z vysledku dotazu
    dbRoleTypes = [
        {"name": role.name, "name_en": role.name_en, "id": role.id}
        for role in dbRoleTypes
    ]

    print("roletypes found in database")
    print(dbRoleTypes)

    roleTypeNamesInDatabase = [roleType["name"] for roleType in dbRoleTypes]

    unsavedRoleTypes = list(
        filter(
            lambda roleType: not (roleType["name"] in roleTypeNamesInDatabase),
            roleTypes,
        )
    )

    # ted by melo byt pole prazdne
    print("roletypes not found in database")
    print(unsavedRoleTypes)
    if not (len(unsavedRoleTypes) == 0):
        print("SOMETHING is REALLY WRONG")

    # a ted maly hack, doplnime IDcka do cache
    for roleType in roleTypes:
        roleTypeName = roleType["name"]
        dbRecords = list(
            filter(lambda item: (item["name"] == roleTypeName), dbRoleTypes)
        )
        assert len(dbRecords) == 1, f"Nalezen {len(dbRecords)} pocet zaznamu :("
        roleType["id"] = dbRecords[0]["id"]
        roleType["name_en"] = dbRecords[0]["name_en"]

    # test hacku
    print("Role types in database")
    print(determineRoleTypes())
    pass


async def putPredefinedStructuresIntoTable(asyncSessionMaker, DBModel, datadict):

    tableName = DBModel.__tablename__
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

    stmt = select(DBModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = dbSet.scalars()

    idsInDb = list(map(lambda item: f"{item.id}", dbRows))
    whatToAdd = list(filter(lambda item: item["id"] not in idsInDb, datadict))
    models = list(map(lambda item: DBModel(**mapToCols(item)), whatToAdd))

    async with asyncSessionMaker() as session:
        async with session.begin():
            session.add_all(models)
        await session.commit()

    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = dbSet.scalars()

    report = list(map(lambda item: {"id": f"{item.id}", "name": item.name}, dbRows))
    print("*" * 30)
    print("* data in table ", DBModel)
    print("*" * 30)
    for item in report:
        print(item)
    print("*" * 30)


async def predefineAllDataStructures(asyncSessionMaker):
    await putPredefinedStructuresIntoTable(
        asyncSessionMaker, RoleTypeModel, determineRoleTypes()
    )
    await putPredefinedStructuresIntoTable(
        asyncSessionMaker, GroupTypeModel, determineGroupTypes()
    )
    pass


async def createSystemDataStructureGroupTypes(asyncSessionMaker):
    """Zabezpeci inicializaci zakladnich typu skupin v databazi"""
    # ocekavane typy skupin
    groupTypes = determineGroupTypes()

    # dotaz do databaze
    stmt = select(GroupTypeModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbGroupTypes = dbSet.scalars()

    # extrakce dat z vysledku dotazu
    dbGroupTypes = [
        {"name": groupType.name, "name_en": groupType.name_en, "id": groupType.id}
        for groupType in dbGroupTypes
    ]

    print("grouptypes found in database")
    print(dbGroupTypes)

    groupTypeNamesInDatabase = [groupType["name"] for groupType in dbGroupTypes]

    unsavedGroupTypes = list(
        filter(
            lambda groupType: not (groupType["name"] in groupTypeNamesInDatabase),
            groupTypes,
        )
    )
    print("grouptypes not found in database")
    print(unsavedGroupTypes)

    GroupTypeModelToAdd = [
        GroupTypeModel(
            name_en=groupType["name_en"], name=groupType["name"], id=groupType["id"]
        )
        for groupType in unsavedGroupTypes
    ]
    print(GroupTypeModelToAdd)
    print(len(GroupTypeModelToAdd))

    async with asyncSessionMaker() as session:
        async with session.begin():
            session.add_all(GroupTypeModelToAdd)
        await session.commit()

    # a ted opakovany dotaz
    stmt = select(GroupTypeModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbGroupTypes = dbSet.scalars()

    # extrakce dat z vysledku dotazu
    dbGroupTypes = [
        {"name": groupType.name, "name_en": groupType.name_en, "id": groupType.id}
        for groupType in dbGroupTypes
    ]

    print("grouptypes found in database")
    print(dbGroupTypes)

    groupTypeNamesInDatabase = [groupType["name"] for groupType in dbGroupTypes]

    unsavedGroupTypes = list(
        filter(
            lambda groupType: not (groupType["name"] in groupTypeNamesInDatabase),
            groupTypes,
        )
    )
    assert len(unsavedGroupTypes) == 0, "Neco je fakt spatne :("

    # a ted maly hack, doplnime IDcka do cache
    for groupType in groupTypes:
        groupTypeName = groupType["name"]
        dbRecords = list(
            filter(lambda item: (item["name"] == groupTypeName), dbGroupTypes)
        )
        assert len(dbRecords) == 1, f"Nalezen {len(dbRecords)} pocet zaznamu :("
        groupType["id"] = dbRecords[0]["id"]
        groupType["name_en"] = dbRecords[0]["name_en"]

    # test hacku
    print("Group types in database")
    print(determineGroupTypes())


def getTypeIdFromGroupTypeName(groupTypeName):
    """vrati Id nalezejici prislusnemu nazvu typu skupiny"""
    for groupType in determineGroupTypes():
        if groupType["name"] == groupTypeName:
            return groupType["id"]
    return None


def getTypeIdFromRoleTypeName(roleTypeName):
    """vrati Id nalezejici prislusnemu nazvu typu role"""
    for roleType in determineRoleTypes():
        if roleType["name"] == roleTypeName:
            return roleType["id"]
    return None


async def randomDataStructure(session, name):
    """Ziska JSON popisujici nahodnou univerzitu a vytvori ji v databazi (session)"""
    print("randomDataStructure BEGIN")
    university = randomUniversity(name)

    # seznam vsech nahodne vygenerovanych uzivatelu
    users = university["users"]
    usersToAdd = [UserModel(**user) for user in users]
    # pridat seznam do databaze
    async with session.begin():
        session.add_all(usersToAdd)
    await session.commit()

    # extrahovat idcka prirazena databazi a uchovat je v puvodni strukture
    for uA, uB in zip(users, usersToAdd):
        uA["id"] = uB.id

    # vytvorit skupinu univerzita
    university["grouptype"]["id"] = getTypeIdFromGroupTypeName(
        university["grouptype"]["name"]
    )
    print(university["grouptype"])
    universityDbRecord = GroupModel(
        name=university["name"], grouptype_id=university["grouptype"]["id"]
    )
    async with session.begin():
        session.add(universityDbRecord)
    await session.commit()
    university["id"] = universityDbRecord.id

    # vytvorit vsechny skupiny na univerzite (fakulty, katedry)

    # generator dvojic, (nadrizenaSkupina, podrizenaSkupina)
    def allGroups(masterGroup):
        for subGroup in masterGroup["subgroups"]:
            yield masterGroup, subGroup
            for duo in allGroups(subGroup):
                yield duo

    groupDuoCollection = list(allGroups(university))
    # vse projdeme a vytvorime v databazi
    for masterGroup, subGroup in groupDuoCollection:
        subGroup["grouptype"]["id"] = getTypeIdFromGroupTypeName(
            subGroup["grouptype"]["name"]
        )
        groupDbRecord = GroupModel(
            name=subGroup["name"],
            grouptype_id=subGroup["grouptype"]["id"],
            mastergroup_id=masterGroup["id"],
        )
        async with session.begin():
            session.add(groupDbRecord)
        await session.commit()
        # poznamename si idcko (subGroup muze byt masterGroup)
        subGroup["id"] = groupDbRecord.id

    # vsechny skupiny rekurzivne
    def allGroups2(masterGroup):
        yield masterGroup
        for subGroup in masterGroup["subgroups"]:
            for group in allGroups2(subGroup):
                yield group

    # projdeme vsechny skupiny a vytvorime uzivatele
    for group in allGroups2(university):
        memmbershipsToAdd = [
            MembershipModel(group_id=group["id"], user_id=user["id"], valid=True)
            for user in group["users"]
        ]
        async with session.begin():
            session.add_all(memmbershipsToAdd)
        await session.commit()
        pass

    def allRoles(group):
        for role in group["roles"]:
            yield role
        for subGroup in group["subgroups"]:
            for role in allRoles(subGroup):
                yield role

    rolesToAdd = [
        RoleModel(
            user_id=role["user"]["id"],
            group_id=role["group"]["id"],
            roletype_id=getTypeIdFromRoleTypeName(role["roletype"]["name"]),
            valid=True
        )
        for role in allRoles(university)
    ]
    async with session.begin():
        session.add_all(rolesToAdd)
    await session.commit()

    return university["id"]


async def createUniversity(session, id, name):
    """Vytvori prazdnou univerzitu v databazi (session)"""

    university = {
        "id": id,
        "name": name,
        "valid": True,
        "grouptype": {"name": "univerzita"},
        "subgroups": [],
        "roles": [],
        "users": [],
    }

    university["grouptype"]["id"] = getTypeIdFromGroupTypeName(
        university["grouptype"]["name"]
    )
    print(university["grouptype"])
    universityDbRecord = GroupModel(
        name=university["name"], grouptype_id=university["grouptype"]["id"]
    )
    async with session.begin():
        session.add(universityDbRecord)
    await session.commit()
    university["id"] = universityDbRecord.id
    return university["id"]


from gql_ug.GraphResolvers import (
    resolveGroupById,
    resolveUserById,
    resolveMembershipById,
)


async def importUg(session, data):
    ids = {}
    for group in data["groups"]:
        id = group.get("id", None)
        if id is None:
            raise Exception(f"id must be defined on group {group}")
        else:
            groupRecord = await resolveGroupById(session, id)
            if not groupRecord is None:
                raise Exception(f"there already exists group with id {id}")
            elif id in ids:
                raise Exception(
                    f"this import has multiple use of id {id} see {ids[id]}"
                )
            else:
                ids[id] = {"id": id, "type": "group", "name": group["name"]}

    for user in data["users"]:
        id = user.get("id", None)
        if id is None:
            raise Exception(f"id must be defined on user {user}")
        else:
            userRecord = await resolveUserById(session, id)
            if not userRecord is None:
                raise Exception(f"there already exists user with id {id}")
            elif id in ids:
                raise Exception(
                    f"this import has multiple use of id {id} see {ids[id]}"
                )
            else:
                ids[id] = {"id": id, "type": "user", "name": user["email"]}

    for membership in data["memberships"]:
        id = membership.get("id", None)
        if id is None:
            raise Exception(f"id must be defined on membership {membership}")
        else:
            membershipRecord = await resolveMembershipById(session, id)
            if not membershipRecord is None:
                raise Exception(f"there already exists membership with id {id}")
            elif id in ids:
                raise Exception(
                    f"this import has multiple use of id {id} see {ids[id]}"
                )
            else:
                ids[id] = {"id": id, "type": "membership", "name": membership["id"]}

    def justThoseKeys(data, keys):
        result = {}
        for key in keys:
            if key in data:
                result[key] = data[key]
        return result

    groupKeys = ["id", "name", "grouptype_id", "mastergroup_id", "valid"]
    groupsToAdd = [
        GroupModel(**justThoseKeys(group, groupKeys)) for group in data["groups"]
    ]

    userKeys = ["id", "name", "surname", "email", "valid"]
    usersToAdd = [UserModel(**justThoseKeys(user, userKeys)) for user in data["users"]]

    membershipKeys = ["id", "group_id", "user_id", "valid"]
    membershipsToAdd = [
        MembershipModel(**justThoseKeys(membership, membershipKeys))
        for membership in data["memberships"]
    ]

    allEntitites = groupsToAdd + usersToAdd + membershipsToAdd

    async with session.begin():
        session.add_all(allEntitites)
    await session.commit()

    pass




import os
import json
from uoishelpers.feeders import ImportModels
import datetime

def get_demodata():
    def datetime_parser(json_dict):
        for (key, value) in json_dict.items():
            if key in ["startdate", "enddate", "lastchange", "created"]:
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
            GroupTypeModel, 
            RoleCategoryModel,
            RoleTypeModel,
        ]
    else:
        dbModels = [
            GroupTypeModel, 
            RoleCategoryModel,
            RoleTypeModel,
            UserModel,
            GroupModel,
            MembershipModel,
            RoleModel,
        ]

    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass