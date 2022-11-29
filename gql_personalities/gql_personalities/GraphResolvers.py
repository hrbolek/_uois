
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

from gql_personalities.DBDefinitions import BaseModel, UserModel, Personalities_Rank, Personalities_Study, Personalities_Certificate, Personalities_Medal, Personalities_WorkHistory, Personalities_RelatedDoc
from gql_personalities.DBDefinitions import Personalities_CertificateType, Personalities_MedalType
from gql_personalities.DBDefinitions import Personalities_MedalTypeGroup

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

