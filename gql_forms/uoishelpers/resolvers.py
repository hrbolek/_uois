import uuid
import sqlalchemy
import strawberry  # strawberry-graphql==0.119.0

from strawberry.types.types import TypeDefinition
from strawberry.utils.inspect import get_func_args
from graphql import GraphQLObjectType, GraphQLError
from functools import partial
from typing import cast

import datetime #I changed it
from typing import Any, Coroutine, Callable, Awaitable, Union, List, Optional

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta as BaseModel

from contextlib import asynccontextmanager


@asynccontextmanager
async def withInfo(info):
    """Context manager for session created
    from info.context['asyncSessionMaker']."""
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass


# def entities_resolver(self, root, info, representations):
#     """Allows to call appropriate GQL model for reverence resolving.
#     Implements ability to use single query to database with multiple results."""
#     results = []
#     typeDict = {}
#     for index, representation in enumerate(representations):
#         type_name = representation.pop("__typename")
#         type_ = self.schema_converter.type_map[type_name]
#         typeRow = typeDict.get(type_name, None)
#         if typeRow is None:
#             typeRow = {"type": type_, "questions": [], "indexes": [], "results": []}
#             typeDict[type_name] = typeRow
#             definition = cast(TypeDefinition, type_.definition)
#             keyNames = list(representation.keys())
#             # keyValues = list(representation.values())
#             if hasattr(definition.origin, "resolve_references") and (
#                 len(keyNames) == 1
#             ):
#                 keyName = keyNames[0]
#                 typeRow["lazy"] = True
#                 # typeRow['solved'] = False

#                 resolve_references = definition.origin.resolve_references

#                 func_args = get_func_args(resolve_references)

#                 def getResult():
#                     keyValues = typeRow["questions"]
#                     kwargs = {}
#                     kwargs[keyName] = list(map(lambda item: item[keyName], keyValues))
#                     # TODO: use the same logic we use for other resolvers
#                     if "info" in func_args:
#                         kwargs["info"] = info
#                     return resolve_references(**kwargs)

#                 if keyName not in func_args:
#                     result = GraphQLError(
#                         f"Got confused while trying use resolve_references for {definition.origin}. Resolver resolve_references has not a prameter {keyNames[0]}"
#                     )
#                     get_result = lambda: [result] * len(typeRow["questions"])
#                 # get_result = partial(resolve_references, **kwargs)
#                 else:
#                     get_result = getResult
#                 typeRow["get_result"] = get_result
#             elif hasattr(definition.origin, "resolve_reference"):
#                 typeRow["lazy"] = False

#                 resolve_reference = definition.origin.resolve_reference

#                 func_args = get_func_args(resolve_reference)

#                 # TODO: use the same logic we use for other resolvers
#                 if "info" in func_args:

#                     def getResult(representation):
#                         return resolve_references(info=info, **representation)

#                 else:
#                     getResult = representation

#                 typeRow["get_result"] = getResult
#             else:
#                 from strawberry.arguments import convert_argument

#                 typeRow["lazy"] = False
#                 strawberry_schema = info.schema.extensions["strawberry-definition"]
#                 config = strawberry_schema.config
#                 scalar_registry = strawberry_schema.schema_converter.scalar_registry

#                 # get_result = partial(
#                 #     convert_argument,
#                 #     representation,
#                 #     type_=definition.origin,
#                 #     scalar_registry=scalar_registry,
#                 #     config=config,
#                 # )

#                 def create_get_result(
#                     convert_argument,
#                     type_=definition.origin,
#                     scalar_registry=scalar_registry,
#                     config=config,
#                 ):

#                     return lambda representation: convert_argument(
#                         representation,
#                         type_=definition.origin,
#                         scalar_registry=scalar_registry,
#                         config=config,
#                     )

#                 typeRow["get_result"] = create_get_result(
#                     convert_argument,
#                     type_=definition.origin,
#                     scalar_registry=scalar_registry,
#                     config=config,
#                 )
#         typeRow["indexes"].append(index)
#         typeRow["questions"].append(representation)

#     async def awaitableWrapper(index, row):
#         semaphore = row["semaphore"]
#         listOfIndexes = row["indexes"]
#         indexOf = listOfIndexes.index(index)
#         async with semaphore:
#             listOfResults = row["results"]
#             if inspect.isawaitable(listOfResults):
#                 listOfResults = await listOfResults
#                 row["results"] = listOfResults
#             singleResult = listOfResults[indexOf]
#         return singleResult

#     indexedResults = []
#     for entityName, row in typeDict.items():
#         if row["lazy"]:
#             row["semaphore"] = asyncio.BoundedSemaphore(1)

#             get_result = row["get_result"]
#             result = get_result()
#             row["results"] = result
#             indexedResults.extend(
#                 [(index, awaitableWrapper(index, row)) for index in row["indexes"]]
#             )
#         else:
#             get_result = row["get_result"]
#             row["results"] = [get_result(item) for item in row["questions"]]
#             indexedResults.extend(
#                 [
#                     (index, result)
#                     for index, result in zip(row["indexes"], row["results"])
#                 ]
#             )

#     indexedResults.sort(key=lambda a: a[0])
#     results = list(map(lambda item: item[1], indexedResults))
#     return results


def update(destination, source=None, extraValues={}):
    """Updates destination's attributes with source's attributes.
    Attributes with value None are not updated."""
    if source is not None:
        for name in dir(source):
            if name.startswith("_"):
                continue
            value = getattr(source, name)
            if value is not None:
                setattr(destination, name, value)

    for name, value in extraValues.items():
        setattr(destination, name, value)

    return destination


async def putSingleEntityToDb(session, entity):
    """Asynchronně uloží entitu do databáze,
    entita musí být definována jako instance modelu (SQLAlchemy)"""
    async with session.begin():
        session.add(entity)
    await session.commit()
    return entity


def createFilterInputType(rootName, names=[]):
    assert not (len(names) == 0), "There must be some names"
    # {'where': {'_or': [{'name': {'_eq': 5}}, {'name': {'_eq': 4}}]}}

    def createCustomInput(attributeName):
        result = type(f"{rootName}By_{attributeName}", (object,), {})
        result.__annotations__ = dict(
            (op, Optional[str]) for op in ["_eq", "_le", "_lt", "_ge", "_gt"]
        )
        for op in ["_eq", "_le", "_lt", "_ge", "_gt"]:
            setattr(result, op, None)
        return strawberry.input(result)  # this is decoration

    customInputFilters = dict(
        (name, createCustomInput(name))
        for name in names)

    AllAttributes = type(f"{rootName}AllAttributes", (object,), {})
    for name in names:
        setattr(AllAttributes, name, None)
    AllAttributes.__annotations__ = dict(
        (name, Optional[customInputFilters[name]]) for name in names
    )
    AllAttributes = strawberry.input(AllAttributes)

    Filter = type(f"{rootName}Filter", (object,), {})
    Filter.__annotations__ = {
        "_or": Optional[List[AllAttributes]],
        "_and": Optional[List[AllAttributes]],
        **dict((name, Optional[customInputFilters[name]]) for name in names),
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

    columnTypes = dict(
        (item.columns[0].type, item.columns[0].name)
        for item in mapper.column_attrs
    )

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
            "_eq": "__eq__",
            "_gt": "__gt__",
            "_lt": "__lt__",
            "_ge": "__ge__",
            "_le": "__le__",
        }

        foundValue = None
        if not (queryName is None):
            foundValue = getattr(query, queryName)

            comparedItem = None
            for key, value in methodMaps.items():
                if hasattr(foundValue, key):
                    comparedItem = value
                    break

            return getattr(DBModel, methodMaps[key])(comparedItem)

        return (DBModel.id == DBModel.id) # will this work?

    def createWhereLambda(where):        
        return DBModel.id == DBModel.id  # will this work?

    def createWhereLambda(where):
        pass

    async def FullResolver(
        session, skip: Optional[int] = 0, limit: Optional[int] = 10, where=None
    ) -> List[DBModel]:
        stmtWithFilter = stmt.offset(skip).limit(limit)
        dbSet = await session.execute(stmtWithFilter)
        result = dbSet.scalars()
        return result

    return FullResolver


def createEntityGetterWR(
    DBModel: BaseModel, options=None, redis=None
) -> Callable[[AsyncSession, int, int], Awaitable[Union[BaseModel, None]]]:
    """Předkonfiguruje dotaz do databáze na vektor entit

    Parameters
    ----------
    DBModel : BaseModel
        class representing SQLAlchlemy model - table where record will be found
    options : any
        possible to use joinedload from SQLAlchemy
        for extending the query (select with join)

    Returns
    -------
    Callable[[AsyncSession, int, int], Awaitable[DBModel]]
        asynchronous function for query into database
    """
    assert options is None, "options cannot be used"
    assert redis is not None, "redis must be defined"

    stmt = select(DBModel)

    mapper = sqlalchemy.inspect(DBModel)
    columnNames = dict(
        (item.columns[0].name, item.columns[0].type)
        for item in mapper.column_attrs
    )

    print(columnNames)

    predefinedSerialisers = {
        sqlalchemy.Boolean: lambda value: f"{value}",
        sqlalchemy.String: lambda value: value,
        sqlalchemy.DateTime: lambda value: f"{value}",
        uuid.UUID: lambda value: f"{value}",
        sqlalchemy.BigInteger: lambda value: value,
    }

    serialisers = {}
    for colName, colType in columnNames.items():
        serialisers[colName] = predefinedSerialisers.get(
            colType, lambda value: f"{value}"
        )

    def convertModelToJSON(model: DBModel):
        result = dict(
            (name, serialisers[name](getattr(model, name)))
            for name in columnNames.keys()
        )
        return result

    def convertJSONToModel(jsonData):
        result = DBModel()
        for columnName, columnType in columnNames.items():
            setattr(
                columnName,
                serialisers[columnName](jsonData.get(columnName, None))
            )
        return result

    def envelopeItem(row):
        itemAsJson = convertModelToJSON(row)
        # redis.hset(itemAsJson['id'], json.dumps(itemAsJson))
        redis.hset(f"{row.id}", mapping=itemAsJson)
        # redis.set(f'{row.id}', itemAsJson)
        return row

    def envelopeSequence(scalars):
        for item in scalars:
            yield envelopeItem(item)

    async def resultedFunction(session, skip, limit) -> Union[DBModel, None]:
        """Předkonfigurovaný dotaz bez filtru"""
        stmtWithFilter = stmt.offset(skip).limit(limit)

        dbSet = await session.execute(stmtWithFilter)
        result = dbSet.scalars()
        return envelopeSequence(result)

    return resultedFunction


def createEntityGetter(
    DBModel: BaseModel, options=None
) -> Callable[[AsyncSession, int, int], Awaitable[Union[BaseModel, None]]]:
    """Předkonfiguruje dotaz do databáze na vektor entit

    Parameters
    ----------
    DBModel : BaseModel
        class representing SQLAlchlemy model - table where record will be found
    options : any
        possible to use joinedload from SQLAlchemy
        for extending the query (select with join)

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


# r = redis.Redis(host='redis', decode_responses=True)
def createEntityByIdGetterWR(
    DBModel: BaseModel, options=None, redis=None
) -> Callable[[AsyncSession, int, int], Awaitable[Union[BaseModel, None]]]:
    """Předkonfiguruje dotaz do databáze na entitu podle id

    Parameters
    ----------
    DBModel : BaseModel
        class representing SQLAlchlemy model - table where record will be found
    options : any
        possible to use joinedload from SQLAlchemy
        for extending the query (select with join)

    Returns
    -------
    Callable[[AsyncSession, int, int], Awaitable[DBModel]]
        asynchronous function for query into database
    """
    assert options is None, "options cannot be used"
    assert redis is not None, "redis must be defined"

    stmt = select(DBModel)

    mapper = sqlalchemy.inspect(DBModel)
    columnNames = dict(
        (item.columns[0].name, item.columns[0].type)
        for item in mapper.column_attrs
    )

    # print(columnNames)

    predefinedSerialisers = {
        sqlalchemy.Boolean: lambda value: f"{value}",
        sqlalchemy.String: lambda value: value,
        sqlalchemy.DateTime: lambda value: f"{value}",
        # sqlalchemy.dialects.postgresql.UUID(as_uuid=True): lambda value: f"{value}",
        uuid.UUID: lambda value: f"{value}",
        sqlalchemy.BigInteger: lambda value: value,
    }

    serialisers = {}
    for colName, colType in columnNames.items():
        serialisers[colName] = predefinedSerialisers.get(
            colType, lambda value: f"{value}"
        )

    def convertModelToJSON(model: DBModel):
        result = dict(
            (name, serialisers[name](getattr(model, name)))
            for name in columnNames.keys()
        )
        # result = json.dumps(result)
        # result= result.encode('ascii')
        return result

    def convertJSONToModel(jsonData):
        result = DBModel()
        for columnName, columnType in columnNames.items():
            setattr(
                columnName,
                serialisers[columnName](jsonData.get(columnName, None))
            )
        return result

    def envelopeItem(row):
        itemAsJson = convertModelToJSON(row)
        # redis.hset(itemAsJson['id'], json.dumps(itemAsJson))
        rowId = itemAsJson["id"]
        redis.hset(rowId, mapping=itemAsJson)
        redis.expire(rowId, 30)
        # redis.set(f'{row.id}', itemAsJson)
        return row

    async def resultedFunction(session, id) -> Union[DBModel, None]:
        """Předkonfigurovaný dotaz bez filtru"""

        if redis.exists(id):
            redisResult = redis.hgetall(id)

            return convertJSONToModel(redisResult)
        else:
            stmtWithFilter = stmt.filter_by(id=id)

            dbSet = await session.execute(stmtWithFilter)
            result = next(dbSet.scalars(), None)
            return envelopeItem(result)

    return resultedFunction


def createEntityByIdGetter(
    DBModel: BaseModel, options=None
) -> Callable[[AsyncSession, uuid.UUID], Awaitable[Union[BaseModel, None]]]:
    """Předkonfiguruje dotaz do databáze na entitu podle id

    Parameters
    ----------
    DBModel : BaseModel
        class representing SQLAlchlemy model - table where record will be found
    options : any
        possible to use joinedload from SQLAlchemy
        for extending the query (select with join)

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


def create1NGetter(
    ResultedDBModel: BaseModel, foreignKeyName, options=None, filters=None
) -> Callable[[AsyncSession, uuid.UUID], Awaitable[List[BaseModel]]]:
    """Vytvori resolver pro relaci 1:N (M:N)
       Dotazujeme se na cizi entitu,
       ktera obsahuje foreingKey s patricnou hodnotou
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
        asynchronous function representing the resolver
        for 1:N (or N:M) relations on particular entity
    """
    if options is None:
        stmt = select(ResultedDBModel)
    else:
        if isinstance(options, list):
            stmt = select(ResultedDBModel).options(*options)
        else:
            stmt = select(ResultedDBModel).options(options)

    if filters is not None:
        if isinstance(filters, list):
            stmt = stmt.filter(*filters)
        else:
            stmt = stmt.filter(filters)

    async def ExecuteAndGetList(session: AsyncSession, stmt):
        """ "Sdilena funkce pro resolvery"""
        dbSet = await session.execute(stmt)
        result = dbSet.scalars()
        return result

    async def resultedFunction(
        session: AsyncSession,
        id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
        filters=None,
    ) -> List[ResultedDBModel]:
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
        stmtWithFilter = stmt
        if filters is not None:
            if isinstance(filters, list):
                stmtWithFilter = stmtWithFilter.filter(*filters)
            else:
                stmtWithFilter = stmtWithFilter.filter(filters)

        filterQuery = {foreignKeyName: id}
        stmtWithFilter = (
            stmtWithFilter.filter_by(**filterQuery).offset(skip).limit(limit)
        )
        return await ExecuteAndGetList(session, stmtWithFilter)

    async def resultedFunctionWithFilters(
        session: AsyncSession, id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[ResultedDBModel]:
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
        stmtWithFilter = (
            stmt.filter_by(**filterQuery).
            offset(skip).
            limit(limit)
        )
        return await ExecuteAndGetList(session, stmtWithFilter)

    # if filters is None:
    #     return resultedFunction
    # else:
    #     return resultedFunctionWithFilters
    return resultedFunction


def createUpdateResolver(
    DBModel: BaseModel, safe=False
) -> Callable[[AsyncSession, uuid.UUID, dict], Awaitable[BaseModel]]:
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

    async def resolveUpdate(
        session: AsyncSession, id: uuid.UUID, data: dict, extraAttributes={}
    ) -> Awaitable[DBModel]:
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

    async def resolveUpdateSafe(
        session: AsyncSession, id: uuid.UUID, data: dict, extraAttributes={}
    ) -> Awaitable[DBModel]:
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

        if dbRecord.lastchange == data.lastchange:
            data.lastchange = datetime.datetime.now()
            result = update(dbRecord, data, extraAttributes)
            await session.commit()
        else:
            # someone updated meanwhile, return currentRecord
            result = dbRecord

        return result

    return resolveUpdateSafe if safe else resolveUpdate


def createInsertResolver(
    DBModel: BaseModel,
) -> Callable[[AsyncSession, BaseModel, dict], Awaitable[BaseModel]]:
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

    async def resolveInsert(
        session,
        data,
        extraAttributes={}
    ) -> Awaitable[DBModel]:
        """Inserts a new record into database with given data

        Parameters
        ----------
        session : AsyncSession
            asynchronous session object which allows the update
        data : class
            datastructure holding the data for the update, could be None
        extraAttributes : dict
            extra key-values to be set in the new record,
            they are prioritized thus they can ovewrite data
        Returns
        ----------
        DBModel
            datastructure saved in database
        """
        dbRecord = DBModel()
        result = await putSingleEntityToDb(
            session, update(dbRecord, data, extraAttributes)
        )
        await session.commit()
        return result

    return resolveInsert