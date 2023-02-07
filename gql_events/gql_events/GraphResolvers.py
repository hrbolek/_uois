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
    EventOrganizerModel,
)
from gql_events.DBDefinitions import UserModel, GroupModel, EventParticipantModel

###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

resolveEventById = createEntityByIdGetter(EventModel)
resolveEventPage = createEntityGetter(EventModel)
resolveUsersForEvent = create1NGetter(
    EventOrganizerModel,
    foreignKeyName="event_id",
    options=joinedload(EventOrganizerModel.user),
)
resolveGroupsForEvent = create1NGetter(
    EventGroupModel,
    foreignKeyName="event_id",
    options=joinedload(EventGroupModel.group),
)

resolveParticipantsForEvent = create1NGetter(
    EventParticipantModel,
    foreignKeyName="event_id",
    options=joinedload(EventOrganizerModel.user),
)

resolveEventsForUser_ = create1NGetter(
    EventOrganizerModel,
    foreignKeyName="user_id",
    options=joinedload(EventOrganizerModel.event),
)
resolveEventsForGroup_ = create1NGetter(
    EventGroupModel,
    foreignKeyName="group_id",
    options=joinedload(EventGroupModel.event),
)

from sqlalchemy.future import select


async def resolveEventsForGroup(session, id, startdate=None, enddate=None):
    statement = select(EventModel).join(EventGroupModel)
    if startdate is not None:
        statement = statement.filter(EventModel.start >= startdate)
    if enddate is not None:
        statement = statement.filter(EventModel.end <= enddate)
    statement = statement.filter(EventGroupModel.group_id == id)

    response = await session.execute(statement)
    result = response.scalars()
    return result


async def resolveEventsForParticipant(session, id, startdate=None, enddate=None):
    statement = select(EventModel).join(EventParticipantModel)
    if startdate is not None:
        statement = statement.filter(EventModel.start >= startdate)
    if enddate is not None:
        statement = statement.filter(EventModel.end <= enddate)
    statement = statement.filter(EventParticipantModel.user_id == id)

    response = await session.execute(statement)
    result = response.scalars()
    return result


async def resolveEventsForUser(session, id, startdate=None, enddate=None):
    statement = select(EventModel).join(EventOrganizerModel)
    if startdate is not None:
        statement = statement.filter(EventModel.start >= startdate)
    if enddate is not None:
        statement = statement.filter(EventModel.end <= enddate)
    statement = statement.filter(EventOrganizerModel.user_id == id)

    response = await session.execute(statement)
    result = response.scalars()
    return result
