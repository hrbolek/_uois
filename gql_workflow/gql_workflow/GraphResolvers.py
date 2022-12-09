
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

from gql_workflow.DBDefinitions import BaseModel

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

from gql_workflow.DBDefinitions import WorkflowModel, AuthorizationModel

## workflow resolvers
resolveWorkflowsPaged = createEntityGetter(WorkflowModel)
resolveWorkflowById = createEntityByIdGetter(WorkflowModel)
resolveInsertWorkflow = createInsertResolver(WorkflowModel)

## authorization resolvers
resolveAuthorizationsPaged = createEntityGetter(AuthorizationModel)
resolveAuthorizationById = createEntityByIdGetter(AuthorizationModel)
resolveInsertAuthorization = createInsertResolver(AuthorizationModel)