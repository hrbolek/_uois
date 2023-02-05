from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery
# zde definujte sve resolvery s pomoci funkci vyse tyto pouzijete v GraphTypeDefinitions
###########################################################################################################################

from gql_forms.DBDefinitions import BaseModel, RequestModel, SectionModel, PartModel, ItemModel, UserModel


## request resolvers

# it will use for form the table if y know the id , u can extract it from the database
resolveRequestById = createEntityByIdGetter(RequestModel)
resolveRequestAll = createEntityGetter(RequestModel)
resolveRequestByUser = create1NGetter(RequestModel, foreignKeyName='creator_id')

# allow u to retrieves which are related to the request if i have the request id 
resolveSectionsForRequest = create1NGetter(SectionModel, foreignKeyName='request_id')

resolveUpdateRequest = createUpdateResolver(RequestModel)
resolveInsertRequest = createInsertResolver(RequestModel)

"""Function for searching requests by three letters"""
async def resolveRequestsByThreeLetters(session: AsyncSession, validity = None, letters: str = '') -> List[RequestModel]:
    if len(letters) < 3:
        return []
    stmt = select(RequestModel).where(RequestModel.name.like(f'%{letters}%'))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()

## section resolvers
resolveSectionById = createEntityByIdGetter(SectionModel)
resolveSectionAll = createEntityGetter(SectionModel)

resolvePartsForSection = create1NGetter(PartModel, foreignKeyName='section_id')

resolveUpdateSection = createUpdateResolver(SectionModel)
resolveInsertSection = createInsertResolver(SectionModel)

async def resolveRequestsByStatus(session: AsyncSession, status: str)->List[RequestModel]:
    """ This function resolves requests from a database based on the status specified
 Inputs: 
   session: AsyncSession - an asynchronous session object for interacting with the database
   status: str - a string specifying the status to filter the requests
Output:
    List[RequestModel] - a list of RequestModel objects representing the resolved requests"""
    stmt = select(RequestModel)
    stmtWithFilter = stmt.filter_by(status= status)
    dbSet = await session.execute(stmtWithFilter)
    result= dbSet.scalars()
    return result
    
## part resolvers
resolvePartById = createEntityByIdGetter(PartModel)
resolvePartAll = createEntityGetter(PartModel)

resolveItemsForPart = create1NGetter(ItemModel, foreignKeyName='part_id')

resolveUpdatePart = createUpdateResolver(PartModel)
resolveInsertPart = createInsertResolver(PartModel)

## item resolvers
resolveItemById = createEntityByIdGetter(ItemModel)
resolveItemAll = createEntityGetter(ItemModel)

resolveUpdateItem = createUpdateResolver(ItemModel)
resolveInsertItem = createInsertResolver(ItemModel)

# async def resolveDeleteItem(session: AsyncSession, id: uuid.UUID):
#     deletedItem= session.get(ItemModel,id)
#     session.delete(deletedItem)
#     session.commit()

## user resolvers
resolveUserById = createEntityByIdGetter(UserModel)
resolveUserAll = createEntityGetter(UserModel)

resolveUpdateUser = createUpdateResolver(UserModel)
resolveInsertUser = createInsertResolver(UserModel)
