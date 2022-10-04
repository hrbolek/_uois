
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from gql_ug.DBDefinitions import BaseModel, UserModel, GroupModel, MembershipModel, RoleModel
from gql_ug.DBDefinitions import GroupTypeModel, RoleTypeModel


def update(destination, source=None, extraValues={}):
    """Updates destination's attributes with source's attributes. Attributes with value None are not updated."""
    if source is not None:
        for name in dir(source):
            if name.startswith('_'):
                continue
            value = getattr(source, name)
            if value is not None:
                setattr(destination, name, value)
        
    for name, value in extraValues.items():
        setattr(destination, name, value)

    return destination

async def putSingleEntityToDb(session, entity):
    """Asynchronně uloží entitu do databáze, entita musí být definována jako instance modelu (SQLAlchemy)"""
    async with session.begin():
        session.add(entity)
    await session.commit()
    return entity

def createEntityByIdGetter(DBModel: BaseModel, options=None) -> Callable[[AsyncSession, uuid.UUID], Awaitable[BaseModel]]:
    """Předkonfiguruje dotaz do databáze na entitu podle id
    
    Parameters
    ----------
    DBModel : BaseModel
        class representing SQLAlchlemy model - table where record will be found
    options : any
        possible to use joinedload from SQLAlchemy for extending the query (select with join)

    Returns
    -------
    Callable[[AsyncSession, uuid.UUID], Awaitable[DBModel]]
        asynchronous function for query into database
    """
    
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

    return resultedFunction

def create1NGetter(ResultedDBModel: BaseModel, foreignKeyName, options=None, filters=None) -> Callable[[AsyncSession, uuid.UUID], Awaitable[List[BaseModel]]]:
    """Vytvori resolver pro relaci 1:N (M:N)
       Dotazujeme se na cizi entitu, ktera obsahuje foreingKey s patricnou hodnotou
       Ocekavanym navratem je vektor hodnot

    Parameters
    ----------
    ResultedDBModel : BaseModel
        class representing a model (SQLAlchemy) for result
    foreignKeyName : str
        name of foreignkey used for filtering entities
    options : any
        parameters for options parameters, usually joinedload from SQLAlchemy
    filters : dict
        set of filters applied to query

    Returns
    -------
    Callable[[AsyncSession, uuid.UUID], Awaitable[List[BaseModel]]]
        asynchronous function representing the resolver for 1:N (or N:M) relations on particular entity
    """
    if options is None:
        stmt = select(ResultedDBModel)
    else:
        if isinstance(options, list):
            stmt = select(ResultedDBModel).options(*options)
        else:
            stmt = select(ResultedDBModel).options(options)

    async def ExecuteAndGetList(session: AsyncSession, stmt):
        """"Sdilena funkce pro resolvery"""
        dbSet = await session.execute(stmt)
        result = dbSet.scalars()
        return result

    async def resultedFunction(session: AsyncSession, id: uuid.UUID) -> List[ResultedDBModel]:
        """Predkonfigurovany dotaz bez filtru
        
        Parameters
        ----------
        session : AsyncSession
            session for DB (taken from SQLAlchemy)
        id: uuid.UUID
            key value used for foreign key

        Returns
        -------
        List[ResultedDBModel]
            vector of entities (1:N or M:N)
        """
        filterQuery = {foreignKeyName: id}
        stmtWithFilter = stmt.filter_by(**filterQuery)
        return await ExecuteAndGetList(session, stmtWithFilter)

    async def resultedFunctionWithFilters(session: AsyncSession, id: uuid.UUID) -> List[ResultedDBModel]:
        """Predkonfigurovany dotaz s filtrem
        
        Parameters
        ----------
        session : AsyncSession
            session for DB (taken from SQLAlchemy)
        id: uuid.UUID
            key value used for foreign key

        Returns
        -------
        List[ResultedDBModel]
            vector of entities (1:N or M:N)
        """
        filterQuery = {**filters, foreignKeyName: id}
        stmtWithFilter = stmt.filter_by(**filterQuery)
        return await ExecuteAndGetList(session, stmtWithFilter)

    if filters is None:
        return resultedFunction
    else:
        return resultedFunctionWithFilters

def createUpdateResolver(DBModel):
    """Create update asynchronous resolver for DBmodel (SQLAlchemy)
    
    Parameters
    ----------
    DBModel : BaseModel
        the model (SQLAlchemy) which table contains a record being updated

    Returns
    ----------
    Callable[[session, id, data], awaitable]
        async function for update
    """
    async def resolveUpdate(session, id, data):
        """Updates a record with id=id according give data

        Parameters
        ----------
        DBModel : BaseModel
            the model (SQLAlchemy) which table contains a record being updated
        session : AsyncSession
            asynchronous session object which allows the update
        data : class
            datastructure holding the data for the update

        Returns
        ----------
        DBModel
            datastructure with updated items
        """
        stmt = select(DBModel).filter_by(id=id)
        dbSet = await session.execute(stmt)
        dbRecord = dbSet.scalars().first()
        result = update(dbRecord, data)
        await session.commit()
        return result
    return resolveUpdate

def createInsertResolver(DBModel):
    """Create insert asynchronous resolver for DBmodel (SQLAlchemy)
    
    Parameters
    ----------
    DBModel : BaseModel
        the model (SQLAlchemy) which table contains a record being inserted

    Returns
    ----------
    Callable[[session, id, data], awaitable]
        async function for update
    """
    async def resolveInsert(session, data, extraAttributes):
        """Inserts a new record into database with given data

        Parameters
        ----------
        session : AsyncSession
            asynchronous session object which allows the update
        data : class
            datastructure holding the data for the update, could be None
        extraAttributes : dict
            extra key-values to be set in the new record, they are prioritized thus they can ovewrite data
        Returns
        ----------
        DBModel
            datastructure saved in database
        """
        dbRecord = DBModel()
        result = await putSingleEntityToDb(session, update(dbRecord, data, extraAttributes=extraAttributes))
        return result
    return resolveInsert


## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery
## user resolvers
resolveUserById = createEntityByIdGetter(UserModel)
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
resolveGroupForGroupType = create1NGetter(GroupModel, foreignKeyName='grouptype_id')

## roletype resolvers
resolveRoleTypeById = createEntityByIdGetter(RoleTypeModel)
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
