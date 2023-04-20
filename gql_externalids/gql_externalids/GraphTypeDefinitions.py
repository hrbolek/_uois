from typing import List, Union, Optional
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

def getLoaders(info):
    return info.context['all']
###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
# - venujte pozornost metode resolve reference, tato metoda je dulezita pro komunikaci mezi prvky federace,
#
###########################################################################################################################

from gql_externalids.GraphResolvers import (
    resolveExternalTypeById,
    resolveExternalIds,
    resolveExternalIdById,
)


@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing an external type id (like SCOPUS identification / id)""",
)
class ExternalIdTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info=info).externaltypeids
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Type name""")
    def name(self) -> str:
        return self.name


@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing an external type id (like SCOPUS identification / id)""",
)
class ExternalIdGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info=info).externalids
        print(loader, flush=True)
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Inner id""")
    def inner_id(self) -> strawberryA.ID:
        return self.inner_id

    @strawberryA.field(description="""Outer id""")
    def outer_id(self) -> str:
        return self.outer_id

    @strawberryA.field(description="""Type of id""")
    async def id_type(self, info: strawberryA.types.Info) -> "ExternalIdTypeGQLModel":
        result = await ExternalIdTypeGQLModel.resolve_reference(info=info, id=self.typeid_id)
        return result

    @strawberryA.field(description="""Type name of id""")
    async def type_name(self, info: strawberryA.types.Info) -> Union[str, None]:
        result = await ExternalIdTypeGQLModel.resolve_reference(info=info, id=self.typeid_id)
        if not result is None:
            result = result.name
        return result

###########################################################################################################################
#
# nasleduji rozsirene GQLModely (existuji nekde jinde a vy jim pridavate dalsi atributy)
# vsimnete si,
# - jak je definovan dekorator tridy (extend=True)
# - jaky dekorator je pouzit (federation.type)
#
# - venujte pozornost metode resolve reference, tato metoda je dulezita pro komunikaci mezi prvky federace,
# - ma odlisnou implementaci v porovnani s modelem, za ktery jste odpovedni
#
###########################################################################################################################


@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)

    @strawberryA.field(description="""All external ids related to the user""")
    async def external_ids(
        self, info: strawberryA.types.Info
    ) -> List["ExternalIdGQLModel"]:

        loader = getLoaders(info=info).externalids_inner_id
        result = await loader.load(self.id)    
        return result


@strawberryA.federation.type(extend=True, keys=["id"])
class GroupGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return GroupGQLModel(id=id)

    @strawberryA.field(description="""All external ids related to a group""")
    async def external_ids(
        self, info: strawberryA.types.Info
    ) -> List["ExternalIdGQLModel"]:
        loader = getLoaders(info=info).externalids_inner_id
        result = await loader.load(self.id)    
        return result

from gql_externalids.GraphResolvers import resolveAssignExternalId

@strawberryA.federation.type(extend=True, keys=["id"])
class GroupEditorGQLModel:  # GroupGQLEditorModel

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return GroupEditorGQLModel(id=id)

    @strawberryA.field(description="""Inner id""")
    async def assign_external_id(
        self, info: strawberryA.types.Info, external_id: str, typeid_id: strawberryA.ID
    ) -> "ExternalIdGQLModel":
        async with withInfo(info) as session:
            result = await resolveAssignExternalId(
                session, internalid=self.id, externalid=external_id, typeid=typeid_id
            )
            return result


@strawberryA.federation.type(extend=True, keys=["id"])
class UserEditorGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return UserEditorGQLModel(id=id)

    @strawberryA.field(description="""Inner id""")
    async def assign_external_id(
        self, info: strawberryA.types.Info, external_id: str, typeid_id: strawberryA.ID
    ) -> "ExternalIdGQLModel":
        async with withInfo(info) as session:
            result = await resolveAssignExternalId(
                session, internalid=self.id, externalid=external_id, typeid=typeid_id
            )
            return result


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

from gql_externalids.GraphResolvers import (
    resolveExternalTypePaged,
    resolveExternalIdIntoInnerId,
    resolveInnerIdIntoExternalIds,
)


@strawberryA.type(description="""Type for query root""")
class Query:
    # @strawberryA.field(description="""Returns all types for external ids""")
    # async def external_id_page(
    #     self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    # ) -> List[ExternalIdTypeGQLModel]:
    #     async with withInfo(info) as session:
    #         result = await resolveExternalTypePaged(session, skip, limit)
    #         return result

    @strawberryA.field(
        description="""Returns inner id based on external id type and external id value"""
    )
    async def internal_id(
        self,
        info: strawberryA.types.Info,
        external_type_id: strawberryA.ID,
        external_id: str,
    ) -> Union[strawberryA.ID, None]:
        async with withInfo(info) as session:
            result = await resolveExternalIdIntoInnerId(
                session, externalid=external_id, typeid=external_type_id
            )
            return result.inner_id

    @strawberryA.field(
        description="""Returns outer ids based on external id type and external id value"""
    )
    async def external_ids(
        self,
        info: strawberryA.types.Info,
        internal_id: strawberryA.ID,
        external_type_id: Optional[strawberryA.ID] = None,
    ) -> List[ExternalIdGQLModel]:
        async with withInfo(info) as session:
            result = await resolveInnerIdIntoExternalIds(
                session, internalid=internal_id, typeid=external_type_id
            )
            return result


###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(
    Query, types=(UserGQLModel, GroupGQLModel, UserEditorGQLModel, GroupEditorGQLModel)
)
