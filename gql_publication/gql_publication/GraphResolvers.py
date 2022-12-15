
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

from gql_publication.DBDefinitions import BaseModel, PublicationModel, AuthorModel, PublicationTypeModel, UserModel, SubjectModel

 ## Publication resolvers 

resolvePublicationById = createEntityByIdGetter(PublicationModel)
resolvePublicationAll = createEntityGetter(PublicationModel)

resolveUpdatePublication = createUpdateResolver(PublicationModel)
resolveInsertPublication = createInsertResolver(PublicationModel)


# Author resolvers

resolveAuthorById = createEntityByIdGetter(AuthorModel)
resolveUpdateAuthor = createUpdateResolver(AuthorModel)
resolveInsertAuthor = createInsertResolver(AuthorModel)
resolveUserForAuthor = create1NGetter(AuthorModel, foreignKeyName='user_id')
resolveAuthorsForPublication = create1NGetter(AuthorModel, foreignKeyName='publication_id', options=joinedload(AuthorModel.user))

# Subject resolvers

resolvePublicationsForSubject = create1NGetter(SubjectModel, foreignKeyName='subject_id', options=joinedload(SubjectModel.publication))


async def setCascadeAuthorsOrder(session, publication_id, author_id, order):
    result = list(await resolveAuthorsForPublication(session))
    for row in dbRecords:
        row['order']

    
    await session.commit()
    return result

## PublicationType resolvers
resolvePublicationTypeById = createEntityByIdGetter(PublicationTypeModel)
resolvePublicationTypeAll = createEntityGetter(PublicationTypeModel)
resolvePublicationForPublicationType = create1NGetter(PublicationModel, foreignKeyName='publication_type_id')

