
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

from gql_publication.DBDefinitions import BaseModel, PublicationModel, AuthorModel, PublicationTypeModel, UserModel, SubjectModel

import copy

# User resolvers

# resolveAuthorsByUser = create1NGetter()

# Publication resolvers 

resolvePublicationById = createEntityByIdGetter(PublicationModel)

resolvePublicationAll = createEntityGetter(PublicationModel)

resolveUpdatePublication = createUpdateResolver(PublicationModel, safe=True)
resolveInsertPublication = createInsertResolver(PublicationModel)


# Author resolvers

resolveAuthorById = createEntityByIdGetter(AuthorModel)
resolveUpdateAuthor = createUpdateResolver(AuthorModel)
resolveInsertAuthor = createInsertResolver(AuthorModel)
resolveAuthorByUser = create1NGetter(AuthorModel, foreignKeyName='user_id')
resolveAuthorsForPublication = create1NGetter(AuthorModel, foreignKeyName='publication_id', options=joinedload(AuthorModel.user))

# resolvePublicationForUser = create1NGetter(AuthorModel, foreignKeyName='publication_id', options=joinedload(AuthorModel.publication))
# Subject resolvers

resolvePublicationsForSubject = create1NGetter(SubjectModel, foreignKeyName='subject_id', options=joinedload(SubjectModel.publication))

resolveSubjectsForPublication = create1NGetter(SubjectModel, foreignKeyName='publication_id', options=joinedload(SubjectModel.subject))


# async def  resolveUpdateAuthor = createUpdateResolver(AuthorModel)

async def resolveRemoveAuthor(session, publication_id, user_id):
    stmt = delete(AuthorModel).where((AuthorModel.user_id==user_id) & (AuthorModel.publication_id == publication_id))
    resultMsg= ""
    try:
        response = await session.execute(stmt)
        await session.commit()
        if(response.rowcount == 1):
            resultMsg = "ok"
        else:
            resultMsg = "fail"
        
    except:
        resultMsg="error"
  
    return resultMsg


async def resolvePublicationsByUser(session, id):
    stmt = select(PublicationModel).join(AuthorModel)
    stmt = stmt.filter(AuthorModel.user_id == id)
    response = await session.execute(stmt)
    result = response.scalars()
    return result 

async def resolvePublicationsForAuthor(session, id):
    stmt = select(PublicationModel).join(AuthorModel)
    stmt = stmt.filter(AuthorModel.id == id)
    response = await session.execute(stmt)
    result = response.scalars()
    return result 


async def resolveUpdateAuthorOrder(session, id, author_id, order):
    result = list(await resolveAuthorsForPublication(session,id))
    result.sort(key=lambda i: i.order)
    sortedAuthors = result
    modifiedAuthor =  copy.deepcopy(next(filter(lambda author: author['id'] == author_id, sortedAuthors)))

    limitValue = modifiedAuthor["order"]
    modifiedAuthor["order"] = order

    for author in sortedAuthors:
        if((author["order"] <= order) and (author["order"] >= limitValue)):
            author["order"] -= 1
        elif(author["order"] >= order) and (author["order"] <= limitValue):
            author["order"] += 1

    sortedAuthors[limitValue-1] = modifiedAuthor

    await session.commit()
    return sortedAuthors
    # return result 
## PublicationType resolvers
resolvePublicationTypeById = createEntityByIdGetter(PublicationTypeModel)
resolvePublicationTypeAll = createEntityGetter(PublicationTypeModel)
resolvePublicationForPublicationType = create1NGetter(PublicationModel, foreignKeyName='publication_type_id')

