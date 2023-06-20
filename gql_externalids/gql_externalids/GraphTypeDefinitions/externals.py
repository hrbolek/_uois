import strawberry
from typing import List

from .externalIdTypeGQLModel import ExternalIdGQLModel

def getLoaders(info):
    return info.context["all"]

def getUser(info):
    return info.context["user"]


@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: strawberry.ID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID):
        return UserGQLModel(id=id)

    @strawberry.field(description="""All external ids related to the user""")
    async def external_ids(
        self, info: strawberry.types.Info
    ) -> List["ExternalIdGQLModel"]:

        loader = getLoaders(info=info).externalids_inner_id
        result = await loader.load(self.id)    
        return result


@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:

    id: strawberry.ID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID):
        return GroupGQLModel(id=id)

    @strawberry.field(description="""All external ids related to a group""")
    async def external_ids(
        self, info: strawberry.types.Info
    ) -> List["ExternalIdGQLModel"]:
        loader = getLoaders(info=info).externalids_inner_id
        result = await loader.load(self.id)    
        return result