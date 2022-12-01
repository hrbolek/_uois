
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

from gql_personalities.DBDefinitions import BaseModel, UserModel, Rank, Study, Certificate, Medal, WorkHistory, RelatedDoc
from gql_personalities.DBDefinitions import RankType, CertificateType, MedalType
from gql_personalities.DBDefinitions import CertificateTypeGroup, MedalTypeGroup

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################


#user resolvers
resolveUserById = createEntityByIdGetter(UserModel)

#rank resolvers
resolveRankById = createEntityByIdGetter(Rank)

#rankType resolvers
resolveRankTypeById = createEntityByIdGetter(RankType)

#study resolvers
resolveStudyById = createEntityByIdGetter(Study)

#certificate resolvers
resolveCertificateById = createEntityByIdGetter(Certificate)

#certificateType resolvers
resolveCertificateTypeById = createEntityByIdGetter(CertificateType)

#certificateTypeGroup resolvers
resolveCertificateTypeGroupById = createEntityByIdGetter(CertificateTypeGroup)

#medal resolvers
resolveMedalById = createEntityByIdGetter(Medal)

#medalType resolvers
resolveMedalTypeById = createEntityByIdGetter(MedalType)

#medalTypeGroup resolvers
resolveMedalTypeGroupById = createEntityByIdGetter(MedalTypeGroup)

#workHistory resolvers
resolveMedalTypeGroupById = createEntityByIdGetter(MedalTypeGroup)

#relatedDoc resolvers
resolveRelatedDocById = createEntityByIdGetter(RelatedDoc)

###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

