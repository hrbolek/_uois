from typing import List, Union
import typing
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager

@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass


def AsyncSessionFromInfo(info):
    print(
        "obsolte function used AsyncSessionFromInfo, use withInfo context manager instead"
    )
    return info.context["session"]


###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
import datetime
from gql_events.GraphResolvers import resolveEventsForUser


@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)

    @strawberryA.field(description="""Events""")
    async def events(
        self,
        info: strawberryA.types.Info,
        startdate: datetime.datetime = None,
        enddate: datetime.datetime = None,
    ) -> List["EventGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveEventsForUser(session, self.id, startdate, enddate)
            return result


@strawberryA.federation.type(keys=["id"])
class EventUserGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveEventById(session, id)
            # result._type_definition = UserGQLModel()._type_definition # little hack :)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Present, Vacation etc.""")
    async def presence_type(self) -> 'PresenceTypeGQLModel':
        result = await resolvePresenceTypeById(self.presencetype_id)
        return result

    @strawberryA.field(description="""Present, Vacation etc.""")
    async def invitation_type(self) -> 'InvitationTypeGQLModel':
        result = await resolveInvitationTypeById(self.invitation_id)
        return result

    @strawberryA.field(description="""Present, Vacation etc.""")
    def user(self) -> 'UserGQLModel':
        result = UserGQLModel(id=self.user_id)
        return result

    @strawberryA.field(description="""Present, Vacation etc.""")
    async def event(self, info: strawberryA.types.Info) -> 'EventGQLModel':
        result = await EventGQLModel.resolve_reference(info, id=self.event_id)
        return result

@strawberryA.federation.type(keys=["id"])
class PresenceTypeGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveEventById(session, id)
            # result._type_definition = UserGQLModel()._type_definition # little hack :)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name of type (cze)""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Name of type (en)""")
    def name_en(self) -> str:
        return self.name_en

@strawberryA.federation.type(keys=["id"])
class InvitationTypeGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveEventById(session, id)
            # result._type_definition = UserGQLModel()._type_definition # little hack :)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name of type (cze)""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Name of type (en)""")
    def name_en(self) -> str:
        return self.name_en

from gql_events.GraphResolvers import resolveEventsForGroup

@strawberryA.federation.type(extend=True, keys=["id"])
class GroupGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return GroupGQLModel(id=id)

    @strawberryA.field(description="""Events""")
    async def events(
        self,
        info: strawberryA.types.Info,
        startdate: datetime.datetime = None,
        enddate: datetime.datetime = None,
    ) -> List["EventGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveEventsForGroup(session, self.id, startdate, enddate)
            return result

import datetime
from gql_events.GraphResolvers import (
    resolveEventById,
    resolveGroupsForEvent,
)


@strawberryA.federation.type(keys=["id"], description="""Entity representing events""")
class EventGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveEventById(session, id)
            # result._type_definition = UserGQLModel()._type_definition # little hack :)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Primary key""")
    def name(self) -> Union[str, None]:
        return self.name

    @strawberryA.field(description="""Primary key""")
    def startdate(self) -> Union[datetime.datetime, None]:
        return self.start

    @strawberryA.field(description="""Primary key""")
    def enddate(self) -> Union[datetime.datetime, None]:
        return self.end

    @strawberryA.field(description="""Organizers of the event""")
    async def organizers(self, info: strawberryA.types.Info) -> List["UserGQLModel"]:
        async with withInfo(info) as session:
            links = await resolveUsersForEvent(session, self.id)
            result = list(map(lambda item: item.user, links))
            # print('event.orgs', result)
            return result

    @strawberryA.field(description="""Groups of users linked to the event""")
    async def groups(self, info: strawberryA.types.Info) -> List["GroupGQLModel"]:
        async with withInfo(info) as session:
            links = await resolveGroupsForEvent(session, self.id)
            result = list(map(lambda item: item.group, links))
            # print('event.group', result)
            return result

    @strawberryA.field(description="""Participants of the event""")
    async def participants(self, info: strawberryA.types.Info) -> List["UserGQLModel"]:
        async with withInfo(info) as session:
            links = await resolveParticipantsForEvent(session, self.id)
            result = list(map(lambda item: item.user, links))
            # print('event.group', result)
            return result


@strawberryA.federation.type(keys=["id"], description="""Entity representing events""")
class EventEditorGQLModel:
    ##
    ## Mutace, obejiti problemu s federativnim API
    ##

    # vysledky opearace update
    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveEventById(session, id)
            # result._type_definition = UserGQLModel()._type_definition # little hack :)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result of update operation""")
    def result(self) -> str:
        return self.result

    @strawberryA.field(description="""Result of update operation""")
    async def event(self, info: strawberryA.types.Info) -> UserGQLModel:
        async with withInfo(info) as session:
            result = await resolveEventById(session, self.id)
            return result


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

from typing import Optional
import datetime
from gql_events.GraphResolvers import resolveEventPage, resolveEventsForParticipant


@strawberryA.type(description="""Type for query root""")
class Query:
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello_events(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[str, None]:
        result = f"Hello {id}"
        return result

    @strawberryA.field(description="""Finds all events paged""")
    async def event_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[EventGQLModel]:
        async with withInfo(info) as session:
            result = await resolveEventPage(session, skip, limit)
            return result

    @strawberryA.field(description="""Finds a particulat event""")
    async def event_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[EventGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolveEventById(session, id)
            return result

    @strawberryA.field(description="""Finds all events for an organizer""")
    async def event_by_organizer(
        self,
        info: strawberryA.types.Info,
        id: uuid.UUID,
        startdate: Optional[datetime.datetime] = None,
        enddate: Optional[datetime.datetime] = None,
    ) -> List[EventGQLModel]:
        async with withInfo(info) as session:
            result = await resolveEventsForUser(session, id, startdate, enddate)
            return result

    @strawberryA.field(description="""Finds all events for a group""")
    async def event_by_group(
        self,
        info: strawberryA.types.Info,
        id: uuid.UUID,
        startdate: Optional[datetime.datetime] = None,
        enddate: Optional[datetime.datetime] = None,
    ) -> List[EventGQLModel]:
        async with withInfo(info) as session:
            result = await resolveEventsForGroup(session, id, startdate, enddate)
            return result

    @strawberryA.field(description="""Finds all events for a participant""")
    async def event_by_participant(
        self,
        info: strawberryA.types.Info,
        id: uuid.UUID,
        startdate: Optional[datetime.datetime] = None,
        enddate: Optional[datetime.datetime] = None,
    ) -> List[EventGQLModel]:
        async with withInfo(info) as session:
            result = await resolveEventsForParticipant(session, id, startdate, enddate)
            return result


###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel,))
