from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import (
    create1NGetter,
    createEntityByIdGetter,
    createEntityGetter,
    createInsertResolver,
    createUpdateResolver,
)
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
from gql_forms.DBDefinitions import (
    BaseModel,
    RequestModel,
    FormModel,
    SectionModel,
    PartModel,
    
    ItemModel,
    ItemTypeModel,
    ItemCategoryModel,

    FormCategoryModel,
    FormTypeModel,

    HistoryModel
)


## request resolvers,
# it will use for form the table if y know the id , u can extract it from the database
requestselect = select(RequestModel)
formtypeselect = select(FormTypeModel)
formcategorySelect = select(FormCategoryModel)

itemcategoryselect = select(ItemCategoryModel)
itemtypeselect = select(ItemTypeModel)

resolveRequestById = createEntityByIdGetter(RequestModel)
# try to get from the database ..of request u can gert multiblae request
resolveRequestAll = createEntityGetter(RequestModel)

resolveRequestByUser = create1NGetter(RequestModel, foreignKeyName="creator_id")

# allow u to retry which are related to the request if i have the request id
# resolveSectionsForRequest = create1NGetter(SectionModel, foreignKeyName='request_id', options=joinedload(SectionModel.parts))
resolveSectionsForRequest = create1NGetter(SectionModel, foreignKeyName="request_id")
# #
# resolveUserForRequest = createEntityByIdGetter(UserModel)
# bith allow update request maske cration of request model
resolverUpdateRequest = createUpdateResolver(RequestModel)
resolveInsertRequest = createInsertResolver(RequestModel)

"""Function for searching requests by three letters"""


async def resolveRequestsByThreeLetters(
    session: AsyncSession, validity=None, letters: str = ""
) -> List[RequestModel]:
    if len(letters) < 3:
        return []
    stmt = select(RequestModel).where(RequestModel.name.like(f"%{letters}%"))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()


resolveUpdateForm = createUpdateResolver(FormModel, safe=True)

## section resolvers
resolveSectionById = createEntityByIdGetter(SectionModel)
resolveSectionAll = createEntityGetter(SectionModel)
resolvePartsForSection = create1NGetter(PartModel, foreignKeyName="section_id")

resolverUpdateSection = createUpdateResolver(SectionModel, safe=True)
resolveInsertSection = createInsertResolver(SectionModel)

## part resolvers
resolvePartById = createEntityByIdGetter(PartModel)
resolvePartAll = createEntityGetter(PartModel)
resolveItemsForPart = create1NGetter(ItemModel, foreignKeyName="part_id")

resolverUpdatePart = createUpdateResolver(PartModel, safe=True)
resolveInsertPart = createInsertResolver(PartModel)

## item resolvers
resolveItemById = createEntityByIdGetter(ItemModel)
resolveItemAll = createEntityGetter(ItemModel)

resolverUpdateItem = createUpdateResolver(ItemModel, safe=True)
resolveInsertItem = createInsertResolver(ItemModel)

async def createNewRequest(session, formtypeid):
    request = RequestModel()
    
    session.add(request)
    form = FormModel()
    form.type_id = formtypeid

    session.add(form)
    history = HistoryModel()
    session.add(history)
    history.form_id = form.id
    history.request_id = request.id
    await session.commit()
    print("new request", request.id, form.id, flush=True)
    return request
    
