from typing import Any, Coroutine, Callable, Awaitable, Union, List, Optional
import uuid

import sqlalchemy
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta as BaseModel

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


import strawberry # strawberry-graphql==0.119.0
def createFilterInputType(rootName, names=[]):
    assert not(len(names) == 0), "There must be some names"
    # {'where': {'_or': [{'name': {'_eq': 5}}, {'name': {'_eq': 4}}]}}
    
    def createCustomInput(attributeName):
        result = type(f'{rootName}By_{attributeName}', (object, ), {})
        result.__annotations__ = dict((op, Optional[str]) for op in ['_eq', '_le', '_lt', '_ge', '_gt'])
        for op in ['_eq', '_le', '_lt', '_ge', '_gt']:
            setattr(result, op, None)
        return strawberry.input(result) # this is decoration

    customInputFilters = dict((name, createCustomInput(name)) for name in names)
    
    
    AllAttributes = type(f'{rootName}AllAttributes', (object, ), {})
    for name in names:
        setattr(AllAttributes, name, None)
    AllAttributes.__annotations__ = dict((name, Optional[customInputFilters[name]]) for name in names)
    AllAttributes = strawberry.input(AllAttributes)
    
    Filter = type(f'{rootName}Filter', (object, ), {})
    Filter.__annotations__ = {
        '_or': Optional[List[AllAttributes]],
        '_and': Optional[List[AllAttributes]],
        **dict((name, Optional[customInputFilters[name]]) for name in names)
    }
    Filter._or = None
    Filter._and = None
    for name in names:
        setattr(Filter, name, None)
    Filter = strawberry.input(Filter)

    return Filter

def createEntityGetterWithFilter(DBModel: BaseModel):

    stmt = select(DBModel)
    mapper = sqlalchemy.inspect(DBModel)
    
    columnTypes = dict((item.columns[0].type, item.columns[0].name) for item in mapper.column_attrs)

    def createOrLambda(query):
        pass

    def createNamedLambda(query):
        # for queryName, queryValue in query.items():
        #    break # decomposition, hack, get first key and its value

        queryName = None
        for key, value in columnTypes.items():
            if hasattr(query, key):
                queryName = key
                break

        methodMaps = {
            '_eq': '__eq__',
            '_gt': '__gt__',
            '_lt': '__lt__',
            '_ge': '__ge__',
            '_le': '__le__',
        }

        foundValue = None
        if not(queryName is None):
            foundValue = getattr(query, queryName)

            comparedItem = None
            for key, value in methodMaps.items():
                if hasattr(foundValue, key):
                    comparedItem = value
                    break

            return getattr(DBModel, methodMaps[key])(comparedItem)

        return (DBModel.id == DBModel.id) # will this work?


        



    def createWhereLambda(where):        
        pass

    async def FullResolver(session, skip: Optional[int] = 0, limit: Optional[int] = 10, where = None) -> List[DBModel]:
        stmtWithFilter = stmt.offset(skip).limit(limit)
        dbSet = await session.execute(stmtWithFilter)
        result = dbSet.scalars()
        return result

    return FullResolver



def createEntityGetter(DBModel: BaseModel, options=None) -> Callable[[AsyncSession, int, int], Awaitable[Union[BaseModel, None]]]:
    """Předkonfiguruje dotaz do databáze na vektor entit
    
    Parameters
    ----------
    DBModel : BaseModel
        class representing SQLAlchlemy model - table where record will be found
    options : any
        possible to use joinedload from SQLAlchemy for extending the query (select with join)

    Returns
    -------
    Callable[[AsyncSession, int, int], Awaitable[DBModel]]
        asynchronous function for query into database
    """
    
    if options is None:
        stmt = select(DBModel)
    else:
        if isinstance(options, list):
            stmt = select(DBModel).options(*options)
        else:
            stmt = select(DBModel).options(options)

    async def resultedFunction(session, skip, limit) -> Union[DBModel, None]:
        """Předkonfigurovaný dotaz bez filtru"""
        stmtWithFilter = stmt.offset(skip).limit(limit)

        dbSet = await session.execute(stmtWithFilter)
        result = dbSet.scalars()
        return result

    return resultedFunction


def createEntityByIdGetter(DBModel: BaseModel, options=None) -> Callable[[AsyncSession, uuid.UUID], Awaitable[Union[BaseModel, None]]]:
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

def createUpdateResolver(DBModel: BaseModel) -> Callable[[AsyncSession, uuid.UUID, dict], Awaitable[BaseModel]]:
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
    async def resolveUpdate(session: AsyncSession, id: uuid.UUID, data: dict, extraAttributes={}) -> Awaitable[DBModel]:
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
        result = update(dbRecord, data, extraAttributes)
        await session.commit()
        return result
    return resolveUpdate

def createInsertResolver(DBModel: BaseModel) -> Callable[[AsyncSession, BaseModel, dict], Awaitable[BaseModel]]:
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
    async def resolveInsert(session, data, extraAttributes={}) -> Awaitable[DBModel]:
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
        result = await putSingleEntityToDb(session, update(dbRecord, data, extraAttributes))
        await session.commit()
        return result
    return resolveInsert