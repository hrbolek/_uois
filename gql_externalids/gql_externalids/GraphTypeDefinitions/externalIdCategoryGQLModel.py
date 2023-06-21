import strawberry
import datetime
from typing import Optional, List, Union, Annotated
import gql_externalids.GraphTypeDefinitions

def getLoaders(info):
    return info.context["all"]

def getUser(info):
    return info.context["user"]


UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing an external category id ()""",
)
class ExternalIdCategoryGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        if id is None: return None
        loader = getLoaders(info=info).externalcategoryids
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
            result.__strawberry_definition__ = cls._type_definition # some version of strawberry changed :(

        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Category name""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Category name (En)""")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="""Timestamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Initial timestamp""")
    def created(self) -> datetime.datetime:
        return self.created

    @strawberry.field(description="""Who created it""")
    def created_by(self) -> Optional["UserGQLModel"]:
        #sync method which returns Awaitable :)
        return gql_externalids.GraphTypeDefinitions.UserGQLModel.resolve_reference(id=self.createdby)

    @strawberry.field(description="""Who updated it""")
    def changed_by(self) -> Optional["UserGQLModel"]:
        #sync method which returns Awaitable :)
        return gql_externalids.GraphTypeDefinitions.UserGQLModel.resolve_reference(id=self.changedby)

#####################################################################
#
# Special fields for query
#
#####################################################################

@strawberry.field(description="""Rows of externalcategoryids""")
async def externalidcategory_page(self, info: strawberry.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 100) -> List[ExternalIdCategoryGQLModel]:
    loader = getLoaders(info).externalcategoryids
    rows = await loader.page(skip=skip, limit=limit)
    return rows


#####################################################################
#
# Mutation section
#
#####################################################################

import datetime

@strawberry.input()
class ExternalIdCategoryInsertGQLModel:
    name: str = strawberry.field(default=None, description="Name of type")
    name_en: Optional[str] = strawberry.field(default=None, description="En name of type")
    id: Optional[strawberry.ID] = strawberry.field(default=None, description="Could be uuid primary key")
    createdby: strawberry.Private[strawberry.ID]

@strawberry.input()
class ExternalIdCategoryUpdateGQLModel:
    id: strawberry.ID = strawberry.field(default=None, description="Primary key")
    lastchange: datetime.datetime = strawberry.field(default=None, description="Timestamp")
    name: Optional[str] = strawberry.field(default=None, description="Name of category")
    name_en: Optional[str] = strawberry.field(default=None, description="En name of category")
    changedby: strawberry.Private[strawberry.ID]
    
@strawberry.type()
class ExternalIdCategoryResultGQLModel:
    id: Optional[strawberry.ID] = strawberry.field(default=None, description="Primary key of table row")
    msg: str = strawberry.field(default=None, description="""result of operation, should be "ok" or "fail" """)

    @strawberry.field(description="""Result of insert operation""")
    async def externalidcategory(self, info: strawberry.types.Info) -> Union[ExternalIdCategoryGQLModel, None]:
        result = await ExternalIdCategoryGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(description="defines a new external id category for an entity")
async def externalidcategory_insert(self, info: strawberry.types.Info, externalidcategory: ExternalIdCategoryInsertGQLModel) -> ExternalIdCategoryResultGQLModel:
    actingUser = getUser(info)
    loader = getLoaders(info).externalcategoryids
    externalidcategory.createdby = actingUser["id"]
    
    result = ExternalIdCategoryResultGQLModel()
    row = await loader.insert(externalidcategory)
    result.id = row.id
    result.msg = "ok"

    return result

@strawberry.mutation(description="Update existing external id category for an entity")
async def externalidcategory_update(self, info: strawberry.types.Info, externaltypeid: ExternalIdCategoryUpdateGQLModel) -> ExternalIdCategoryResultGQLModel:
    actingUser = getUser(info)
    loader = getLoaders(info).externalcategoryids
    externaltypeid.changedby = actingUser["id"]
    
    result = ExternalIdCategoryResultGQLModel()
    row = await loader.update(externaltypeid)
    if row is None:
        result.id = None
        result.msg = "fail"
    else:
        result.id = row.id
        result.msg = "ok"

    return result

