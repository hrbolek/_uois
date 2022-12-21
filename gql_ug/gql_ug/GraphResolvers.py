
from ast import Call
from curses import keyname
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

from gql_ug.DBDefinitions import BaseModel, UserModel, GroupModel, MembershipModel, RoleModel
from gql_ug.DBDefinitions import GroupTypeModel, RoleTypeModel

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery
## user resolvers
resolveUserById = createEntityByIdGetter(UserModel)
resolveUserAll = createEntityGetter(UserModel)
resolveMembershipForUser = create1NGetter(MembershipModel, foreignKeyName='user_id', options=joinedload(MembershipModel.group))
resolveRolesForUser = create1NGetter(RoleModel, foreignKeyName='user_id', options=joinedload(RoleModel.roletype))

resolverUpdateUser = createUpdateResolver(UserModel)
resolveInsertUser = createInsertResolver(UserModel)

async def resolveUsersByThreeLetters(session: AsyncSession, validity = None, letters: str = '') -> List[UserModel]:
    if len(letters) < 3:
        return []
    stmt = select(UserModel).where((UserModel.name + ' ' + UserModel.surname).like(f'%{letters}%'))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()

## group resolvers
resolveGroupById = createEntityByIdGetter(GroupModel)
resolveGroupAll = createEntityGetter(GroupModel)
resolveMembershipForGroup = create1NGetter(MembershipModel, foreignKeyName='group_id', options=joinedload(MembershipModel.user))
resolveSubgroupsForGroup = create1NGetter(GroupModel, foreignKeyName='mastergroup_id')
resolveMastergroupForGroup = createEntityByIdGetter(GroupModel)
resolveRolesForGroup = create1NGetter(RoleModel, foreignKeyName='group_id')

resolveUpdateGroup = createUpdateResolver(GroupModel)
resolveInsertGroup = createInsertResolver(GroupModel)

async def resolveGroupsByThreeLetters(session: AsyncSession, validity = None, letters: str = '') -> List[GroupModel]:
    if len(letters) < 3:
        return []
    stmt = select(GroupModel).where(GroupModel.name.like(f'%{letters}%'))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()


## membership resolvers
resolveUpdateMembership = createUpdateResolver(MembershipModel)
resolveInsertMembership = createInsertResolver(MembershipModel)
resolveMembershipById = createEntityByIdGetter(MembershipModel)

# grouptype resolvers
resolveGroupTypeById = createEntityByIdGetter(GroupTypeModel)
resolveGroupTypeAll = createEntityGetter(GroupTypeModel)
resolveGroupForGroupType = create1NGetter(GroupModel, foreignKeyName='grouptype_id')

## roletype resolvers
resolveRoleTypeById = createEntityByIdGetter(RoleTypeModel)
resolveRoleTypeAll = createEntityGetter(RoleTypeModel)
resolveRoleForRoleType = create1NGetter(RoleModel, foreignKeyName='roletype_id')

## role resolvers
resolverRoleById = createEntityByIdGetter(RoleModel)

resolveUpdateRole = createUpdateResolver(RoleModel)
resolveInsertRole = createInsertResolver(RoleModel)


async def resolveAllRoleTypes(session):
    stmt = select(RoleTypeModel)
    dbSet = await session.execute(stmt)
    result = dbSet.scalars()
    return result

async def resolveUserByRoleTypeAndGroup(session, groupId, roleTypeId):
    stmt = select(UserModel).join(RoleModel).where(RoleModel.group_id == groupId).where(RoleModel.roletype_id == roleTypeId)
    dbSet = await session.execute(stmt)
    result = dbSet.scalars()
    return result


from uoishelpers.feeders import ImportModels, ExportModels
import json
import datetime
class ExportEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return f'{obj}'
        if isinstance(obj, datetime.datetime):
            return f'{obj}'
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

async def export_ug(session):
    sessionMaker = lambda:session
    jsonData = await ExportModels(sessionMaker, DBModels=[UserModel, GroupModel, MembershipModel, GroupTypeModel, RoleModel, RoleTypeModel])
    with open('./extradata/ug_data.json', 'w') as f:
        json.dump(jsonData, f, cls=ExportEncoder)

    return 'ok'

def datetime_parser(json_dict):
    for (key, value) in json_dict.items():
        if key in ['startdate', 'enddate']:
            dateValue = datetime.datetime.fromisoformat(value)
            dateValueWOtzinfo = dateValue.replace(tzinfo=None)
            json_dict[key] = dateValueWOtzinfo
    return json_dict

import concurrent.futures
import asyncio

from gql_ug.DBDefinitions import ComposeConnectionString, startEngine

import re


async def putPredefinedStructuresIntoTable(asyncSessionMaker, DBModel, structureFunction):
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
    
    #dotaz do databaze
    stmt = select(DBModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = list(dbSet.scalars())
    
    #extrakce dat z vysledku dotazu
    #vezmeme si jen atribut id, id je typu uuid, tak jej zkovertujeme na string
    idsInDatabase = [f'{row.id}' for row in dbRows]

    # zjistime, ktera id nejsou v databazi
    unsavedRows = list(filter(lambda row: not(f'{row["id"]}' in idsInDatabase), externalIdTypes))

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
        if '_chunk' in unsavedRows[0]:
            # existuje informace o rozfazovani ukladani do tabulky
            nextPhase =  [*unsavedRows]
            while len(nextPhase) > 0:
                #zjistime nejmensi cislo poradi ukladani 
                chunkNumber = min(map(lambda item: item['_chunk'], nextPhase))
                #filtrujeme radky, ktere maji toto cislo
                toSave = list(filter(lambda item: item['_chunk'] == chunkNumber, nextPhase))
                #ostatni nechame na pozdeji
                nextPhase = list(filter(lambda item: item['_chunk'] != chunkNumber, nextPhase))
                #ulozime vybrane
                await saveChunk(toSave)
        else:
            # vsechny zaznamy mohou byt ulozeny soucasne
            await saveChunk(unsavedRows)


    # jeste jednou se dotazeme do databaze
    stmt = select(DBModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = dbSet.scalars()
    
    #extrakce dat z vysledku dotazu
    idsInDatabase = [f'{row.id}' for row in dbRows]

    # znovu zaznamy, ktere dosud ulozeny nejsou, mely by byt ulozeny vsechny, takze prazdny list
    unsavedRows = list(filter(lambda row: not(f'{row["id"]}' in idsInDatabase), externalIdTypes))

    # ted by melo byt pole prazdne
    if not(len(unsavedRows) == 0):
        print('SOMETHING is REALLY WRONG')

    #print(structureFunction(), 'On the input')
    #print(dbRowsDicts, 'Defined in database')
    # nyni vsechny entity mame v pameti a v databazi synchronizovane
    #print(structureFunction())
    pass

async def ImportModels(sessionMaker, DBModels, jsonData):
    """imports all data from json structure
        DBModels contains a list of sqlalchemy models
        jsonData data to import
    """

    # create index of all models, key is a table name, value is a model (sqlalchemy model)
    modelIndex = dict((DBModel.__tablename__, DBModel) for DBModel in DBModels)

    for tableName, DBModel in modelIndex.items(): # iterate over all models
        # get the appropriate data

        listData = jsonData.get(tableName, None)
        if listData is None:
            # data does not exists for current model
            print(f'table {tableName} has no data to import', flush=True)
            continue


        print('table', tableName, flush=True)
        # save data - all rows into a table, if a row with same id exists, do not save it nor update it
        await putPredefinedStructuresIntoTable(sessionMaker, DBModel, lambda: listData)
        print(f'table {tableName} import finished', flush=True)

# def runImport(sessionMaker, DBModels):
#     print('runImport Enter', flush=True)
#     asyncio.run(asyncImport(sessionMaker, DBModels))
#     print('runImport Leave', flush=True)

# def runImport2():
#     print('runImport Enter', flush=True)
#     try:
#         newLoop = asyncio.new_event_loop()
#         newLoop.run_until_complete(asyncImport())
#         #asyncio.run(asyncImport())
#     except Exception as e:
#         print('Error', e, flush=True)
#     print('runImport Leave', flush=True)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
async def import_ug(sessionMaker):

    async def backgroundTask():
        DBModels = [RoleTypeModel, GroupTypeModel, UserModel, GroupModel, MembershipModel, RoleModel]
        print('asyncImport have DBModels', flush=True)
        with open('./extradata/ug_data.json', 'r') as f:
            jsonData = json.load(f, object_hook=datetime_parser)
        print('data in json', flush=True)
        try:
            await ImportModels(sessionMaker, 
                DBModels=DBModels,
                jsonData=jsonData)
        except Exception as e:
            print(e)
        print('*'*30, flush=True)
        print('data in DB', flush=True)
        print('*'*30, flush=True)
    #sessionMaker = lambda:session

    print('import Enter', flush=True)

    currentLoop = asyncio.get_running_loop()
    currentLoop.create_task(backgroundTask())

    #executor.submit(runImport2)
    #executor.submit(runImport, sessionMaker, [UserModel, GroupModel, MembershipModel, RoleModel, RoleTypeModel, GroupTypeModel])
    print('import Leave', executor, flush=True)
        
    return 'ok'
