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

from .externalIdTypeGQLModel import ExternalIdTypeGQLModel
from .externalIdGQLModel import ExternalIdGQLModel

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

from .externals import UserGQLModel, GroupGQLModel

schema = strawberryA.federation.Schema(
    Query, types=(UserGQLModel, GroupGQLModel, UserEditorGQLModel, GroupEditorGQLModel)
)
