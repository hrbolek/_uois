import datetime
import strawberry
from typing import List, Optional, Union, Annotated

def getLoaders(info):
    return info.context["all"]

@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: strawberry.ID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID):
        return UserGQLModel(id=id)

@strawberry.federation.type(extend=True, keys=["id"])
class RoleTypeGQLModel:
    id: strawberry.ID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID):
        return RoleTypeGQLModel(id=id)

@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    id: strawberry.ID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID):
        return GroupGQLModel(id=id)
