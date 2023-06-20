import strawberry

def getLoaders(info):
    return info.context["all"]

def getUser(info):
    return info.context["user"]


@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing an external type id (like SCOPUS identification / id)""",
)
class ExternalIdTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoaders(info=info).externaltypeids
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Type name""")
    def name(self) -> str:
        return self.name

