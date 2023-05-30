import typing
import strawberry

@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: strawberry.ID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID):
        return cls(id=id)

@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:

    id: strawberry.ID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID):
        return cls(id=id)

@strawberry.federation.type(extend=True, keys=["id"])
class EventGQLModel:

    id: strawberry.ID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID):
        return cls(id=id)
    
@strawberry.federation.type(extend=True, keys=["id"])
class FacilityGQLModel:

    id: strawberry.ID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID):
        return cls(id=id)