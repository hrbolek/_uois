
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

from gql_publication.DBDefinitions import BaseModel

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery


 ## Publication resolvers 

resolvePublicationById = createEntityByIdGetter(PublicationModel)
resolvePublicaitonAll = createEntityGetter(PublicationModel)

resolverUpdatePublication = createUpdateResolver(PublicationModel)
resolveInsertPublication = createInsertResolver(PublicationModel)
# resolveAuthorForPublication = create1NGetter(AuthorModel, foreignKeyName='publication_id', options=joinedload(MembershipModel.group))


## Author resolvers

resolveAuthorById = createEntityByIdGetter(AuthorModel)

resolverUpdateAuthor = createUpdateResolver(PublicationModel)
resolveInsertAuthor = createInsertResolver(PublicationModel)


## PublicationType resolvers
resolveRoleTypeById = createEntityByIdGetter(PublicationTypeModel)
resolveRoleTypeAll = createEntityGetter(PublicationTypeModel)
resolveRoleForRoleType = create1NGetter(PublicationModel, foreignKeyName='publication_type_id')



from gql_publication.DBDefinitions import PublicationModel, AuthorModel, PublicationTypeModel
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


# ...