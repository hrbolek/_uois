
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

from gql_publication.DBDefinitions import BaseModel, PublicationModel, AuthorModel, PublicationTypeModel, UserModel, SubjectModel



# User resolvers

resolveAuthorsByUser = create1NGetter()

# Publication resolvers 

resolvePublicationById = createEntityByIdGetter(PublicationModel)
resolvePublicationAll = createEntityGetter(PublicationModel)

resolveUpdatePublication = createUpdateResolver(PublicationModel)
resolveInsertPublication = createInsertResolver(PublicationModel)


# Author resolvers

resolveAuthorById = createEntityByIdGetter(AuthorModel)
resolveUpdateAuthor = createUpdateResolver(AuthorModel)
resolveInsertAuthor = createInsertResolver(AuthorModel)
resolveAuthorByUser = create1NGetter(AuthorModel, foreignKeyName='user_id')
resolveAuthorsForPublication = create1NGetter(AuthorModel, foreignKeyName='publication_id', options=joinedload(AuthorModel.user))

resolvePublicationForUser = create1NGetter(AuthorModel, foreignKeyName='publication_id', options=joinedload(AuthorModel.publication))
# Subject resolvers

resolvePublicationsForSubject = create1NGetter(SubjectModel, foreignKeyName='subject_id', options=joinedload(SubjectModel.publication))

resolveSubjectsFroPublication = create1NGetter(SubjectModel, foreignKeyName='publication_id', options=joinedload(SubjectModel.subject))



async def resolveUpdateAuthorOrder(session, id, author_id, order):
    result = list(await resolveAuthorsForPublication(session),id)
    sortedAuthors = sorted(result, key=lambda i: i['order'])
    
    modifiedAuthor = {}    
    index = next((index for (index, d) in enumerate(sortedAuthors) if d["id"] == author_id), None)
    modifiedAuthor =sortedAuthors.pop(index)

    limitValue = modifiedAuthor["order"]
    modifiedAuthor["order"] = order

    for author in sortedAuthors:
        if((author["order"] <= order) and (author["order"] >= limitValue)):
            author["order"] -= 1
        elif(author["order"] >= order) and (author["order"] <= limitValue):
            author["order"] += 1

    sortedAuthors.append(modifiedAuthor)

    await session.commit()
    return sortedAuthors

## PublicationType resolvers
resolvePublicationTypeById = createEntityByIdGetter(PublicationTypeModel)
resolvePublicationTypeAll = createEntityGetter(PublicationTypeModel)
resolvePublicationForPublicationType = create1NGetter(PublicationModel, foreignKeyName='publication_type_id')

