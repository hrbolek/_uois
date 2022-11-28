
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

from gql_publication.DBDefinitions import BaseModel, PublicationModel, AuthorModel, PublicationTypeModel, UserModel

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery


 ## Publication resolvers 

resolvePublicationById = createEntityByIdGetter(PublicationModel)
resolvePublicaitonAll = createEntityGetter(PublicationModel)

resolveUpdatePublication = createUpdateResolver(PublicationModel)
resolveInsertPublication = createInsertResolver(PublicationModel)

#### Probrat na konzultaci

# resolvePublicationByName = createEntityByNameGetter(PublicationModel)
# resolvePublicationByYear = createEntityByYearGetter(PublicationModel)

# async def resolvePublicationByPublicationTypeAndUser(session, userId, publicationTypeId):
#     stmt = select(PublicationModel).join(PublicationTypeModel).where(PublicationModel.publication_type_id == publicationTypeId).join(AuthorModel).where(AuthorModel.publication_id == PublicationModel.publication_type_id).where(AuthorModel.user_id == UserModel.id)
#     dbSet = await session.execute(stmt)
#     result = dbSet.scalars()
#     return result


## Author resolvers

resolveAuthorById = createEntityByIdGetter(AuthorModel)
resolverUpdateAuthor = createUpdateResolver(AuthorModel)
resolveInsertAuthor = createInsertResolver(AuthorModel)
resolveUserForAuthor = create1NGetter(AuthorModel, foreignKeyName='user_id', options=joinedload(AuthorModel.user))
resolveAuthorForPublication = create1NGetter(AuthorModel, foreignKeyName='publication_id', options=joinedload(AuthorModel.publication))



## PublicationType resolvers
resolvePublicationTypeById = createEntityByIdGetter(PublicationTypeModel)
resolvePublicationTypeAll = createEntityGetter(PublicationTypeModel)
resolvePublicationForPublicationType = create1NGetter(PublicationModel, foreignKeyName='publication_type_id')


from gql_publication.DBDefinitions import PublicationModel, AuthorModel, PublicationTypeModel
