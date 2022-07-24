from doctest import master
from functools import cache
from gql_ug.DBDefinitions import BaseModel, UserModel, GroupModel, MembershipModel, RoleModel
from gql_ug.DBDefinitions import GroupTypeModel, RoleTypeModel

import random
import itertools
from functools import cache

@cache
def determineRoleTypes():
    """Definuje zakladni typy roli a udrzuje je v pameti"""
    roleTypes = [
        {'name': 'rector'},
        {'name': 'vicerector'},

        {'name': 'dean'},
        {'name': 'vicedean'},

        {'name': 'head of department'},
        {'name': 'leading teacher'}
        ]
    return roleTypes

@cache
def determineGroupTypes():
    """Definuje zakladni typy skupin a udrzuje je v pameti"""
    groupTypes = [
        {'name': 'university'},
        {'name': 'faculty'},
        {'name': 'centre'},
        {'name': 'institute'},
        {'name': 'department'},
        {'name': 'study group'},
        {'name': 'all teachers'},
        {'name': 'all students'}
    ]
    return groupTypes

def randomUniversity(name):
    """Generuje strukturu skupin na urovni univerzity (fakulty, katedry) a jejich akademicke pracovniky ve forme json"""
    result = {
        'name': f'University {name}', 
        'grouptype': {'name': 'university'},
        'subgroups': [
            randomFaculty(i+1) for i in range(random.randint(3, 5))
        ],
        'roles': [],
        'users': []
        }
    
    result['users'] = [
        user 
        for subgroup in result['subgroups'] 
        for user in subgroup['users']
    ]

    universityRoles = [
        {'name': 'rector'},
        {'name': 'vicerector'},
        {'name': 'vicerector'},
        {'name': 'vicerector'},
        {'name': 'vicerector'},
    ]

    dbRoles = determineRoleTypes()
    universityRolesLinkedToDb = [
        next(filter(lambda dbrole: dbrole['name'] == role['name'], dbRoles)) for role in universityRoles
    ]
    result['roles'] = [
        {
            'roletype': role,
            'user': random.choice(result['users']),
            'group': result
        } for role in universityRolesLinkedToDb
    ]

    return result

def randomFaculty(index):
    """Generuje """
    result = {
        'name': f'Faculty {index}', 
        'grouptype': {'name': 'faculty'},
        'subgroups': [
            randomDepartment(index, i + 1) for i in range(random.randint(8, 15))
        ],
        'roles': [],
        'users': []
    }

    result['users'] = [
        user 
        for subgroup in result['subgroups'] 
        for user in subgroup['users']
    ]

    facultyRoles = [
        {'name': 'dean'},
        {'name': 'vicedean'},
        {'name': 'vicedean'},
        {'name': 'vicedean'},
    ]

    dbRoles = determineRoleTypes()
    facultyRolesLinkedToDb = [
        next(filter(lambda dbrole: dbrole['name'] == role['name'], dbRoles)) for role in facultyRoles
    ]
    result['roles'] = [
        {
            'roletype': role,
            'user': random.choice(result['users']),
            'group': result
        } for role in facultyRolesLinkedToDb
    ]
    #result['users'] = itertools.chain(map(result['subgroups'], lambda group: group['users']))
    return result

def randomDepartment(indexA, indexB):
    """"""
    result = {
        'name': f'Department {indexA}-{indexB}', 
        'grouptype': {'name': 'department'},
        'subgroups': [],
        'roles': [],
        'users': [
            randomUser() for i in range(random.randint(15, 20))
        ]
    }
    result['roles'].append(
        {
            'roletype': {'name': 'head of department'}, 
            'user': random.choice(result['users']),
            'group': result
        })
    return result

def randomUser():
    """Nahodny uzivatel"""
    surNames = [
        'Novák', 'Nováková', 'Svobodová', 'Svoboda', 'Novotná',
        'Novotný', 'Dvořáková', 'Dvořák', 'Černá', 'Černý', 
        'Procházková', 'Procházka', 'Kučerová', 'Kučera', 'Veselá',
        'Veselý', 'Horáková', 'Krejčí', 'Horák', 'Němcová', 
        'Marková', 'Němec', 'Pokorná', 'Pospíšilová','Marek'
    ]

    names = [
        'Jiří', 'Jan', 'Petr', 'Jana', 'Marie', 'Josef',
        'Pavel', 'Martin', 'Tomáš', 'Jaroslav', 'Eva',
        'Miroslav', 'Hana', 'Anna', 'Zdeněk', 'Václav',
        'Michal', 'František', 'Lenka', 'Kateřina',
        'Lucie', 'Jakub', 'Milan', 'Věra', 'Alena'
    ]

    name1 = random.choice(names)
    name2 = random.choice(names)
    name3 = random.choice(surNames)
    return {'name': f'{name1} {name2}', 'surname': f'{name3}', 'email': f'{name1}.{name2}.{name3}@university.world'}

from sqlalchemy.future import select

async def createSystemDataStructureRoleTypes(asyncSessionMaker):
    """Zabezpeci prvotni inicicalizaci typu roli v databazi"""
    # ocekavane typy roli
    roleTypes = determineRoleTypes()
    
    #dotaz do databaze
    stmt = select(RoleTypeModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRoleTypes = dbSet.scalars()
    
    #extrakce dat z vysledku dotazu
    dbRoleTypes = [
        {'name': role.name, 'id': role.id} for role in dbRoleTypes
        ]

    print('roletypes found in database')
    print(dbRoleTypes)

    roleTypeNamesInDatabase = [roleType['name'] for roleType in dbRoleTypes]

    unsavedRoleTypes = list(filter(lambda roleType: not(roleType['name'] in roleTypeNamesInDatabase), roleTypes))
    print('roletypes not found in database')
    print(unsavedRoleTypes)

    RoleTypeModelToAdd = [RoleTypeModel(name = roleType['name']) for roleType in unsavedRoleTypes]
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
    
    #extrakce dat z vysledku dotazu
    dbRoleTypes = [
        {'name': role.name, 'id': role.id} for role in dbRoleTypes
        ]

    print('roletypes found in database')
    print(dbRoleTypes)

    roleTypeNamesInDatabase = [roleType['name'] for roleType in dbRoleTypes]

    unsavedRoleTypes = list(filter(lambda roleType: not(roleType['name'] in roleTypeNamesInDatabase), roleTypes))

    # ted by melo byt pole prazdne
    print('roletypes not found in database')
    print(unsavedRoleTypes)
    if not(len(unsavedRoleTypes) == 0):
        print('SOMETHING is REALLY WRONG')

    # a ted maly hack, doplnime IDcka do cache
    for roleType in roleTypes:
        roleTypeName = roleType['name']
        dbRecords = list(filter(lambda item: (item['name'] == roleTypeName), dbRoleTypes))
        assert len(dbRecords) == 1, f'Nalezen {len(dbRecords)} pocet zaznamu :('
        roleType['id'] = dbRecords[0]['id']

    # test hacku
    print('Role types in database')
    print(determineRoleTypes())
    pass

async def createSystemDataStructureGroupTypes(asyncSessionMaker):
    """Zabezpeci inicializaci zakladnich typu skupin v databazi"""
    # ocekavane typy skupin
    groupTypes = determineGroupTypes()

    #dotaz do databaze
    stmt = select(GroupTypeModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbGroupTypes = dbSet.scalars()
    
    #extrakce dat z vysledku dotazu
    dbGroupTypes = [
        {'name': groupType.name, 'id': groupType.id} for groupType in dbGroupTypes
        ]

    print('grouptypes found in database')
    print(dbGroupTypes)

    groupTypeNamesInDatabase = [groupType['name'] for groupType in dbGroupTypes]

    unsavedGroupTypes = list(filter(lambda groupType: not(groupType['name'] in groupTypeNamesInDatabase), groupTypes))
    print('grouptypes not found in database')
    print(unsavedGroupTypes)

    GroupTypeModelToAdd = [GroupTypeModel(name = groupType['name']) for groupType in unsavedGroupTypes]
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
    
    #extrakce dat z vysledku dotazu
    dbGroupTypes = [
        {'name': groupType.name, 'id': groupType.id} for groupType in dbGroupTypes
        ]

    print('grouptypes found in database')
    print(dbGroupTypes)

    groupTypeNamesInDatabase = [groupType['name'] for groupType in dbGroupTypes]

    unsavedGroupTypes = list(filter(lambda groupType: not(groupType['name'] in groupTypeNamesInDatabase), groupTypes))
    assert len(unsavedGroupTypes) == 0, "Neco je fakt spatne :("

    # a ted maly hack, doplnime IDcka do cache
    for groupType in groupTypes:
        groupTypeName = groupType['name']
        dbRecords = list(filter(lambda item: (item['name'] == groupTypeName), dbGroupTypes))
        assert len(dbRecords) == 1, f'Nalezen {len(dbRecords)} pocet zaznamu :('
        groupType['id'] = dbRecords[0]['id']

    # test hacku
    print('Group types in database')
    print(determineGroupTypes())

def getTypeIdFromGroupTypeName(groupTypeName):
    """vrati Id nalezejici prislusnemu nazvu typu skupiny"""
    for groupType in determineGroupTypes():
        if groupType['name'] == groupTypeName:
            return groupType['id']
    return None

def getTypeIdFromRoleTypeName(roleTypeName):
    """vrati Id nalezejici prislusnemu nazvu typu role"""
    for roleType in determineRoleTypes():
        if roleType['name'] == roleTypeName:
            return roleType['id']
    return None

async def randomDataStructure(session, name):
    """Ziska JSON popisujici nahodnou univerzitu a vytvori ji v databazi (session)"""
    print('randomDataStructure BEGIN')
    university = randomUniversity(name)

    # seznam vsech nahodne vygenerovanych uzivatelu
    users = university['users']
    usersToAdd = [UserModel(**user) for user in users]
    # pridat seznam do databaze
    async with session.begin():
        session.add_all(usersToAdd)
    await session.commit()

    # extrahovat idcka prirazena databazi a uchovat je v puvodni strukture
    for uA, uB in zip(users, usersToAdd):
        uA['id'] = uB.id

    # vytvorit skupinu univerzita
    university['grouptype']['id'] = getTypeIdFromGroupTypeName(university['grouptype']['name'])
    print(university['grouptype'])
    universityDbRecord = GroupModel(name=university['name'], grouptype_id=university['grouptype']['id']) 
    async with session.begin():
        session.add(universityDbRecord)
    await session.commit()
    university['id'] = universityDbRecord.id

    # vytvorit vsechny skupiny na univerzite (fakulty, katedry)

    # generator dvojic, (nadrizenaSkupina, podrizenaSkupina)
    def allGroups(masterGroup):
        for subGroup in masterGroup['subgroups']:
            yield masterGroup, subGroup
            for duo in allGroups(subGroup):
                yield duo

    groupDuoCollection = list(allGroups(university))
    # vse projdeme a vytvorime v databazi
    for masterGroup, subGroup in groupDuoCollection:
        subGroup['grouptype']['id'] = getTypeIdFromGroupTypeName(subGroup['grouptype']['name'])
        groupDbRecord = GroupModel(name=subGroup['name'], grouptype_id=subGroup['grouptype']['id'], mastergroup_id=masterGroup['id'])
        async with session.begin():
            session.add(groupDbRecord)
        await session.commit()
        # poznamename si idcko (subGroup muze byt masterGroup)
        subGroup['id'] = groupDbRecord.id

    # vsechny skupiny rekurzivne
    def allGroups2(masterGroup):
        yield masterGroup
        for subGroup in masterGroup['subgroups']:
            for group in allGroups2(subGroup):
                yield group

    # projdeme vsechny skupiny a vytvorime uzivatele
    for group in allGroups2(university):
        memmbershipsToAdd = [
            MembershipModel(group_id=group['id'], user_id=user['id'], valid=True) 
                for user in group['users']
            ]
        async with session.begin():
            session.add_all(memmbershipsToAdd)
        await session.commit()
        pass

    def allRoles(group):
        for role in group['roles']:
            yield role
        for subGroup in group['subgroups']:
            for role in allRoles(subGroup):
                yield role

    rolesToAdd = [
        RoleModel(
            user_id=role['user']['id'], 
            group_id=role['group']['id'], 
            roletype_id=getTypeIdFromRoleTypeName(role['roletype']['name']))
        for role in allRoles(university)
    ]
    async with session.begin():
        session.add_all(rolesToAdd)
    await session.commit()

    return university['id']