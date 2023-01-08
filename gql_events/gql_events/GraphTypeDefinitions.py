from typing import List, Union
import typing
from warnings import filters
import strawberry as strawberryA
import uuid

def AsyncSessionFromInfo(info):
    return info.context['session']

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
    async def events(self, info: strawberryA.types.Info, startdate: datetime.datetime = None, enddate: datetime.datetime = None) -> List['EventGQLModel']:
        result = await resolveEventsForUser(AsyncSessionFromInfo(info), self.id, startdate, enddate)
        return result


from gql_events.GraphResolvers import resolveEventsForGroup
@strawberryA.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return GroupGQLModel(id=id)

    @strawberryA.field(description="""Events""")
    async def events(self, info: strawberryA.types.Info, startdate: datetime.datetime = None, enddate: datetime.datetime = None) -> List['EventGQLModel']:
        result = await resolveEventsForGroup(AsyncSessionFromInfo(info), self.id, startdate, enddate)
        return result

import datetime
from gql_events.GraphResolvers import resolveEventById, resolveUsersForEvent, resolveGroupsForEvent
@strawberryA.federation.type(keys=["id"], description="""Entity representing events""")
class EventGQLModel:
    
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveEventById(AsyncSessionFromInfo(info), id)
        #result._type_definition = UserGQLModel()._type_definition # little hack :)
        result._type_definition = cls._type_definition # little hack :)
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
    async def organizers(self, info: strawberryA.types.Info) -> List['UserGQLModel']:
        links = await resolveUsersForEvent(AsyncSessionFromInfo(info), self.id)
        result = list(map(lambda item: item.user, links))
        print('event.orgs', result)
        return result

    @strawberryA.field(description="""Groups of users linked to the event""")
    async def groups(self, info: strawberryA.types.Info) -> List['GroupGQLModel']:
        links = await resolveGroupsForEvent(AsyncSessionFromInfo(info), self.id)
        result = list(map(lambda item: item.group, links))
        print('event.group', result)
        return result


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

from typing import Optional
import datetime
from gql_events.GraphResolvers import resolveEventPage
@strawberryA.type(description="""Type for query root""")
class Query:
   
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello_events(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[str, None]:
        result = f'Hello {id}'
        return result

    @strawberryA.field(description="""Finds all events paged""")
    async def event_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[EventGQLModel]:
        result = await resolveEventPage(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Finds a particulat event""")
    async def event_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[EventGQLModel, None]:
        result = await resolveEventById(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Finds all events for an organizer""")
    async def event_by_organizer(self, info: strawberryA.types.Info, id: uuid.UUID, startdate: Optional[datetime.datetime] = None, enddate: Optional[datetime.datetime] = None) -> List[EventGQLModel]:
        result = await resolveEventsForUser(AsyncSessionFromInfo(info), id, startdate, enddate)
        return result

    @strawberryA.field(description="""Finds all events for a group""")
    async def event_by_group(self, info: strawberryA.types.Info, id: uuid.UUID, startdate: Optional[datetime.datetime] = None, enddate: Optional[datetime.datetime] = None) -> List[EventGQLModel]:
        result = await resolveEventsForGroup(AsyncSessionFromInfo(info), id, startdate, enddate)
        return result

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, ))