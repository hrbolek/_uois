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

from gql_events.DBDefinitions import BaseModel

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################

from gql_events.DBDefinitions import (
    EventModel,
    EventGroupModel,
    EventTypeModel,
    PresenceModel,
    PresenceTypeModel,
    InvitationTypeModel
)


###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

resolveEventTypeById = createEntityByIdGetter(EventTypeModel)
resolveEventTypePage = createEntityGetter(EventTypeModel)


resolveEventById = createEntityByIdGetter(EventModel)
resolveEventPage = createEntityGetter(EventModel)
resolveGroupsForEvent = create1NGetter(EventGroupModel, foreignKeyName="event_id")

resolveEventsForGroup_ = create1NGetter(
    EventGroupModel,
    foreignKeyName="group_id",
    options=joinedload(EventGroupModel.event),
)

from sqlalchemy.future import select


async def resolveEventsForGroup(session, id, startdate=None, enddate=None):
    statement = select(EventModel).join(EventGroupModel)
    if startdate is not None:
        statement = statement.filter(EventModel.startdate >= startdate)
    if enddate is not None:
        statement = statement.filter(EventModel.enddate <= enddate)
    statement = statement.filter(EventGroupModel.group_id == id)

    response = await session.execute(statement)
    result = response.scalars()
    return result


async def resolveEventsForUser(session, id, startdate=None, enddate=None):
    statement = select(EventModel).join(PresenceModel)
    if startdate is not None:
        statement = statement.filter(EventModel.startdate >= startdate)
    if enddate is not None:
        statement = statement.filter(EventModel.enddate <= enddate)
    statement = statement.filter(PresenceModel.user_id == id)

    response = await session.execute(statement)
    result = response.scalars()
    return result

async def resolvePresencesForEvent(session, id, invitationtypelist=[]):
    statement = select(PresenceModel)
    if len(invitationtypelist) > 0:
        statement = statement.filter(PresenceModel.invitation_id.in_(invitationtypelist))
    response = await session.execute(statement)
    result = response.scalars()
    return result

resolvePresenceTypeById = createEntityByIdGetter(PresenceTypeModel)
resolveInvitationTypeById = createEntityByIdGetter(InvitationTypeModel)

