
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload

from gql_ug.DBDefinitions import BaseModel, UserModel, GroupModel, MembershipModel, RoleModel
from gql_ug.DBDefinitions import GroupTypeModel, RoleTypeModel

async def putSingleEntitytToDb(session, entity):
    """Asynchronně uloží entitu do databáze, entita musí být definována jako instance modelu (SQLAlchemy)"""
    async with session.begin():
        session.add(entity)
    await session.commit()
    return entity

def createEntityByIdGetter(DBModel: BaseModel, options=None, filters=None) -> Callable[[any, any], Awaitable[BaseModel]]:
    """Předkonfiguruje dotaz do databáze na entitu podle id"""
    
    if options is None:
        stmt = select(DBModel)
    else:
        if isinstance(options, list):
            stmt = select(DBModel).options(*options)
        else:
            stmt = select(DBModel).options(options)

    async def resultedFunction(session, id) -> Union[DBModel, None]:
        """Předkonfigurovaný dotaz bez filtru"""
        stmtWithFilter = stmt.filter_by(id=id)

        dbSet = await session.execute(stmtWithFilter)
        result = next(dbSet.scalars(), None)
        return result

    async def resultedFunctionWithFilter(session, id) -> Union[DBModel, None]:
        """Předkonfigurovaný dotaz s filtry"""
        stmtWithFilter = stmt.filter_by(**filters, id=id)

        dbSet = await session.execute(stmtWithFilter)
        result = next(dbSet.scalars(), None)
        return result

    if filters is None:
        return resultedFunction
    else:
        return resultedFunctionWithFilter

def create1NGetter(ResultedDBModel: BaseModel, foreignKeyName, options=None, filters=None) -> Callable[[any, str], Awaitable[BaseModel]]:
    """Dotazujeme se na cizi entitu, ktera obsahuje foreingKey s patricnou hodnotou
       Ocekavanym navratem je vektor hodnot
    """
    if options is None:
        stmt = select(ResultedDBModel)
    else:
        if isinstance(options, list):
            stmt = select(ResultedDBModel).options(*options)
        else:
            stmt = select(ResultedDBModel).options(options)

    async def resultedFunction(session, id) -> List[ResultedDBModel]:
        """Predkonfigurovany dotaz bez filtru"""
        filterQuery = {foreignKeyName: id}
        stmtWithFilter = stmt.filter_by(**filterQuery)
        dbSet = await session.execute(stmtWithFilter)
        result = dbSet.scalars()
        return result

    async def resultedFunctionWithFilters(session, id) -> List[ResultedDBModel]:
        """Predkonfigurovany dotaz s filtrem"""
        filterQuery = {**filters, foreignKeyName: id}
        stmtWithFilter = stmt.filter_by(**filterQuery)
        dbSet = await session.execute(stmtWithFilter)
        result = dbSet.scalars()
        return result

    if filters is None:
        return resultedFunction
    else:
        return resultedFunctionWithFilters

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery
## user resolvers
resolveUserById = createEntityByIdGetter(UserModel)
resolveMembershipForUser = create1NGetter(MembershipModel, foreignKeyName='user_id', options=joinedload(MembershipModel.group))
resolveRolesForUser = create1NGetter(RoleModel, foreignKeyName='user_id', options=joinedload(RoleModel.roletype))

## group resolvers
resolveGroupById = createEntityByIdGetter(GroupModel)
resolveMembershipForGroup = create1NGetter(MembershipModel, foreignKeyName='group_id', options=joinedload(MembershipModel.user))
resolveSubgroupsForGroup = create1NGetter(GroupModel, foreignKeyName='mastergroup_id')
resolveMastergroupForGroup = createEntityByIdGetter(GroupModel)
resolveRolesForGroup = create1NGetter(RoleModel, foreignKeyName='group_id')

# grouptype resolvers
resolveGroupTypeById = createEntityByIdGetter(GroupTypeModel)
resolveGroupForGroupType = create1NGetter(GroupModel, foreignKeyName='grouptype_id')

## roletype resolvers
resolveRoleTypeById = createEntityByIdGetter(RoleTypeModel)
resolveRoleForRoleType = create1NGetter(RoleModel, foreignKeyName='roletype_id')

## role resolvers
resolverRoleById = createEntityByIdGetter(RoleModel)

async def resolveAllRoleTypes(session):
    stmt = select(RoleTypeModel)
    dbSet = await session.execute(stmt)
    result = dbSet.scalars()
    return result
