
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb




## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################



###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################
from gql_empty.DBDefinitions import BaseModel, RequestModel, SectionModel, PartModel, ItemModel, UserModel


## request resolvers
resolveRequestById = createEntityByIdGetter(RequestModel)
resolveRequestAll = createEntityGetter(RequestModel)
resolveSectionsForRequest = create1NGetter(SectionModel, foreignKeyName='request_id', options=joinedload(SectionModel.parts))
resolveUserForRequest = createEntityByIdGetter(UserModel)

resolverUpdateRequest = createUpdateResolver(RequestModel)
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
resolvePartsForSection = create1NGetter(PartModel, foreignKeyName='section_id', options=joinedload(PartModel.items))
resolveRequestForSection = createEntityByIdGetter(RequestModel)

resolverUpdateSection = createUpdateResolver(SectionModel)


