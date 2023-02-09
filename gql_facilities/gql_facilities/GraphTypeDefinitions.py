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
#
# priklad rozsireni UserGQLModel
#

from gql_facilities.GraphResolvers import resolveFacilitiesByGroup


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
        async with withInfo(info) as session:
            result = resolveFacilitiesByGroup(session, self.id)
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
        async with withInfo(info) as session:
            result = await resolveFacilityById(session, id)
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

    @strawberryA.field(description="""Facility full name""")
    def label(self) -> str:
        return self.label

    # address
    @strawberryA.field(description="""Facility address""")
    def address(self) -> str:
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
    def capacity(self) -> int:
        return self.capacity

    # manager_id

    # address
    @strawberryA.field(description="""Facility geometry (SVG)""")
    def geometry(self) -> str:
        return self.geometry

    @strawberryA.field(description="""Facility geo address""")
    def geolocation(self) -> str:
        return self.geolocation

    @strawberryA.field(description="""Facility timestamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Facility address""")
    async def type(self, info: strawberryA.types.Info) -> "FacilityTypeGQLModel":
        async with withInfo(info) as session:
            result = await resolveFacityTypeById(session, self.facilitytype_id)
            return result

    @strawberryA.field(description="""Facility address""")
    async def state(self, info: strawberryA.types.Info) -> "FacilityStateTypeGQLModel":
        async with withInfo(info) as session:
            result = await resolveFacityTypeById(session, self.facilitytype_id)
            return result

    @strawberryA.field(description="""Facility above this""")
    async def master_facility(self, info: strawberryA.types.Info) -> "FacilityGQLModel":
        async with withInfo(info) as session:
            result = await resolveFacilityById(session, self.facilitytype_id)
            return result

    @strawberryA.field(description="""Facilities inside facility""")
    async def sub_facilities(
        self, info: strawberryA.types.Info
    ) -> List["FacilityGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveFacilitiesByFacility(session, self.facilitytype_id)
            return result

    @strawberryA.field(description="""Facility address""")
    async def group(self, info: strawberryA.types.Info) -> Union["GroupGQLModel", None]:
        return GroupGQLModel(id=self.group_id)


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a facility type"""
)
class FacilityTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveFacilityById(session, id)
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

@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a facility type"""
)
class FacilityStateTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveFacilityStateTypeById(session, id)
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
from gql_facilities.GraphResolvers import resolveFacilityById


@strawberryA.type(description="""Type for query root""")
class Query:
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[str, None]:
        result = f"Hello {id}"
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def facility_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> FacilityGQLModel:
        async with withInfo(info) as session:
            result = await resolveFacilityById(session, id)
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
