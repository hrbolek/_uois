
from ast import Call
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

async def import_ug(session):
    sessionMaker = lambda:session
    with open('./extradata/ug_data.json', 'r') as f:
        jsonData = json.load(f)
        await ImportModels(sessionMaker, 
            DBModels=[UserModel, GroupModel, MembershipModel, GroupTypeModel, RoleModel, RoleTypeModel],
            jsonData=jsonData)
    return 'ok'
