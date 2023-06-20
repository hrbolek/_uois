import strawberry
from typing import Union

def getLoaders(info):
    return info.context["all"]

def getUser(info):
    return info.context["user"]

from .externalIdTypeGQLModel import ExternalIdTypeGQLModel

@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing an external type id (like SCOPUS identification / id)""",
)
class ExternalIdGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoaders(info=info).externalids
        print(loader, flush=True)
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Inner id""")
    def inner_id(self) -> strawberry.ID:
        return self.inner_id

    @strawberry.field(description="""Outer id""")
    def outer_id(self) -> str:
        return self.outer_id

    @strawberry.field(description="""Type of id""")
    async def id_type(self, info: strawberry.types.Info) -> "ExternalIdTypeGQLModel":
        result = await ExternalIdTypeGQLModel.resolve_reference(info=info, id=self.typeid_id)
        return result

    @strawberry.field(description="""Type name of id""")
    async def type_name(self, info: strawberry.types.Info) -> Union[str, None]:
        result = await ExternalIdTypeGQLModel.resolve_reference(info=info, id=self.typeid_id)
        if not result is None:
            result = result.name
        return result