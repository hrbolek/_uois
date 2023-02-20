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

from gql_presences.DBDefinitions import (
    BaseModel,
    TaskModel,
    ContentModel,
)

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################

# user

#resolveUserModelPage = createEntityGetter(UserModel)
#resolveUserModelById = createEntityByIdGetter(UserModel)

# task on event

resolveTasksForUser = create1NGetter(TaskModel, foreignKeyName="user_id")

# tasks

resolveTaskModelByPage = createEntityGetter(TaskModel)
resolveTaskModelById = createEntityByIdGetter(TaskModel)
resolveTasksForEvent = create1NGetter(TaskModel, foreignKeyName="event_id")
# content

resolveContentModelByPage = createEntityGetter(ContentModel)
resolveContentModelById = createEntityByIdGetter(ContentModel)
resolveContentForEvent = create1NGetter(ContentModel, foreignKeyName="event_id")


###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

# resolveItemById = createEntityByIdGetter(EntityModel)
# resolveItemPage = createEntityGetter(EntityModel)

# ...
