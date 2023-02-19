from typing import List, Union
import typing
from unittest import result
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

##TODO relations

def getLoaders(info):
    return info.context['all']
###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
#
# priklad rozsireni UserGQLModel
#

from gql_facilities.GraphResolvers import resolveFacilitiesByGroup

@strawberryA.federation.type(extend=True, keys=["id"])
class EventGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return EventGQLModel(id=id)  # jestlize rozsirujete, musi byt tento vyraz


@strawberryA.federation.type(extend=True, keys=["id"])
class GroupGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return GroupGQLModel(id=id)  # jestlize rozsirujete, musi byt tento vyraz

    #     zde je rozsireni o dalsi resolvery
    #     @strawberryA.field(description="""Inner id""")
    #     async def external_ids(self, info: strawberryA.types.Info) -> List['ExternalIdGQLModel']:
    #         result = await resolveExternalIds(session,  self.id)
    #         return result

    @strawberryA.field(description="""facilities managed by a group""")
    async def facilities(
        self, info: strawberryA.types.Info
    ) -> List["FacilityGQLModel"]:
        loader = getLoaders(info).facilities_by_group_id
        result = await loader.load(self.id)
        return result


import datetime

from gql_facilities.GraphResolvers import (
    resolveFacilityById,
    resolveFacityTypeById,
    resolveFacilitiesByFacility,
)


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a Facility"""
)
class FacilityGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).facility_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    # @classmethod
    # async def resolve_for_event(cls, info: strawberryA.types.Info, event_id: strawberryA.ID):
    #     pass

    # id
    @strawberryA.field(description="""primary key/facility id""")
    def id(self) -> strawberryA.ID:
        return self.id

    # name
    @strawberryA.field(description="""Facility name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Facility name""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""Facility full name""")
    def label(self) -> Union[str, None]:
        return self.label

    # address
    @strawberryA.field(description="""Facility address""")
    def address(self) -> Union[str, None]:
        return self.address

    # valid
    @strawberryA.field(description="""is the facility still valid""")
    def valid(self) -> bool:
        return self.valid

    # #startdate
    # @strawberryA.field(description="""is the membership still valid""")
    # def valid(self) -> datetime:
    #     return self.valid
    # #enddate
    # facilitytype_id

    # capacity
    @strawberryA.field(description="""Facility's name""")
    def capacity(self) -> Union[int, None]:
        return self.capacity

    # manager_id

    # address
    @strawberryA.field(description="""Facility geometry (SVG)""")
    def geometry(self) -> Union[str, None]:
        return self.geometry

    @strawberryA.field(description="""Facility geo address""")
    def geolocation(self) -> Union[str, None]:
        return self.geolocation

    @strawberryA.field(description="""Facility timestamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Facility address""")
    async def type(self, info: strawberryA.types.Info) -> "FacilityTypeGQLModel":
        result = await FacilityTypeGQLModel.resolve_reference(info=info, id=self.facilitytype_id)
        return result

    @strawberryA.field(description="""Intermediate entity linking to event and facility""")
    async def event_states(self, info: strawberryA.types.Info) -> List["FacilityEventGQLModel"]:
        loader = getLoaders(info).event_facility_by_facility_id
        result = await loader.load(self.id)
        return result

    @strawberryA.field(description="""Facility above this""")
    async def master_facility(self, info: strawberryA.types.Info) -> Union["FacilityGQLModel", None]:
        if self.master_facility_id is None:
            return None
        result = await FacilityGQLModel.resolve_reference(info=info, id=self.master_facility_id)
        return result

    @strawberryA.field(description="""Facilities inside facility""")
    async def sub_facilities(
        self, info: strawberryA.types.Info
    ) -> List["FacilityGQLModel"]:
        loader = getLoaders(info).facilities_by_master_id
        result = await loader.load(self.id)
        return result

    @strawberryA.field(description="""Facility address""")
    async def group(self, info: strawberryA.types.Info) -> Union["GroupGQLModel", None]:
        if self.group_id is None:
            return None
        return GroupGQLModel(id=self.group_id)

from gql_facilities.GraphResolvers import facilityTypePageStatement

@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a facility type"""
)
class FacilityTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).facilitytype_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result
    
    # id
    @strawberryA.field(description="""primary key/facility id""")
    def id(self) -> strawberryA.ID:
        return self.id

    # name
    @strawberryA.field(description="""Facility name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Facility name""")
    def name_en(self) -> str:
        return self.name_en


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing the link between facility and event"""
)
class FacilityEventGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).event_facility_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key/facility id""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""the event""")
    def event(self) -> "EventGQLModel":
        return EventGQLModel(id=self.event_id)

    @strawberryA.field(description="""the facility""")
    async def facility(self, info: strawberryA.types.Info) -> "FacilityGQLModel":
        #print()
        result = await FacilityGQLModel.resolve_reference(info=info, id=self.facility_id)
        return result

    @strawberryA.field(description="""the facility""")
    async def state(self, info: strawberryA.types.Info) -> "FacilityStateTypeGQLModel":
        result = await FacilityStateTypeGQLModel.resolve_reference(info=info, id=self.state_id)
        return result


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a facility type"""
)
class FacilityStateTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).event_facility_state_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    # id
    @strawberryA.field(description="""primary key/facility id""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Facility state type name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Facility state type name""")
    def name_en(self) -> str:
        return self.name_en

###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################
from gql_facilities.GraphResolvers import resolveFacilityById, facilityStateTypePageStatement, facilityPageStatement


@strawberryA.type(description="""Type for query root""")
class Query:
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello_facility(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[str, None]:
        result = f"Hello {id}"
        return result

    @strawberryA.field(description="""Finds an facility their id""")
    async def facility_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[FacilityGQLModel, None]:
        result = await FacilityGQLModel.resolve_reference(info=info, id=id)
        return result

    @strawberryA.field(description="""Finds an facility their id""")
    async def facility_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[FacilityGQLModel]:
        loader = getLoaders(info).facility_by_id
        stmt = facilityPageStatement.offset(skip).limit(limit)
        result = await loader.execute_select(stmt)
        #result = await FacilityGQLModel.resolve_reference(info=info, id=id)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def facility_type_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[FacilityTypeGQLModel, None]:
        result = await FacilityTypeGQLModel.resolve_reference(info=info, id=id)
        return result

    @strawberryA.field(description="""Returns all facility types""")
    async def facility_type_page(
        self, info: strawberryA.types.Info
    ) -> List[FacilityTypeGQLModel]:
        loader = getLoaders(info).facilitytype_by_id
        result = await loader.execute_select(facilityTypePageStatement)
        return result

    @strawberryA.field(description="""Returns all facility event states""")
    async def facility_event_state_type_page(
        self, info: strawberryA.types.Info
    ) -> List[FacilityStateTypeGQLModel]:
        loader = getLoaders(info).event_facility_state_by_id
        result = await loader.execute_select(facilityStateTypePageStatement)
        return result


###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(GroupGQLModel,))
