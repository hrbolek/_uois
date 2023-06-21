import strawberry
import datetime
from typing import Union, Optional, List, Annotated
import gql_externalids.GraphTypeDefinitions

def getLoaders(info):
    return info.context["all"]

def getUser(info):
    return info.context["user"]

UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]

from .externalIdTypeGQLModel import ExternalIdTypeGQLModel

###########################################################################################################################
#
# zde definujte sve nove GQL modely, kde mate zodpovednost
#
# - venujte pozornost metode resolve reference, tato metoda je dulezita pro komunikaci mezi prvky federace,
#
###########################################################################################################################



@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing an external type id (like SCOPUS identification / id)""",
)
class ExternalIdGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        if id is None: return None
        loader = getLoaders(info=info).externalids
        print(loader, flush=True)
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
            result.__strawberry_definition__ = cls._type_definition # some version of strawberry changed :(

        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> strawberry.ID:
        return self.id

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
    
#####################################################################
#
# Special fields for query
#
#####################################################################
@strawberry.field(
    description="""Returns inner id based on external id type and external id value"""
    )
async def internal_id(
    self,
    info: strawberry.types.Info,
    typeid_id: strawberry.ID,
    outer_id: str,
) -> Union[strawberry.ID, None]:
    loader = getLoaders(info).externalids
    rows = await loader.filter_by(outer_id=outer_id, typeid_id=typeid_id)
    row = next(rows, None)
    if row is None:
        return None
    else:
        return row.inner_id

@strawberry.field(
    description="""Returns outer ids based on external id type and inner id value"""
    )
async def external_ids(
    self,
    info: strawberry.types.Info,
    inner_id: strawberry.ID,
    typeid_id: Optional[strawberry.ID] = None,
) -> List[ExternalIdGQLModel]:
    loader = getLoaders(info).externalids
    if typeid_id is None:
        rows = await loader.filter_by(inner_id=inner_id)
    else:
        rows = await loader.filter_by(inner_id=inner_id, typeid_id=typeid_id)
    return rows
    
#####################################################################
#
# Mutation section
#
#####################################################################

@strawberry.input()
class ExternalIdInsertGQLModel:
    inner_id: strawberry.ID = strawberry.field(default=None, description="Primary key of entity which new outeid is assigned")
    typeid_id: strawberry.ID = strawberry.field(default=None, description="Type of external id")
    outer_id: strawberry.ID = strawberry.field(default=None, description="Key used by other systems")
    changedby: strawberry.Private[strawberry.ID] = None
    createdby: strawberry.Private[strawberry.ID] = None

@strawberry.input()
class ExternalIdUpdateGQLModel:
    inner_id: strawberry.ID = strawberry.field(default=None, description="Primary key of entity which new outeid is assigned")
    typeid_id: strawberry.ID = strawberry.field(default=None, description="Type of external id")
    outer_id: strawberry.ID = strawberry.field(default=None, description="Key used by other systems")

@strawberry.type()
class ExternalIdResultGQLModel:
    id: Optional[strawberry.ID] = strawberry.field(default=None, description="Primary key of table row")
    msg: str = strawberry.field(default=None, description="""result of operation, should be "ok" or "fail" """)

    @strawberry.field(description="""Result of drone operation""")
    async def externalid(self, info: strawberry.types.Info) -> Union[ExternalIdGQLModel, None]:
        result = await ExternalIdGQLModel.resolve_reference(info, self.id)
        return result


@strawberry.mutation(description="defines a new external id for an entity")
async def externalid_insert(self, info: strawberry.types.Info, externalid: ExternalIdInsertGQLModel) -> ExternalIdResultGQLModel:
    actingUser = getUser(info)
    loader = getLoaders(info).externalids
    externalid.changedby = actingUser["id"]
    
    result = ExternalIdResultGQLModel()
    rows = await loader.filter_by(inner_id=externalid.inner_id, typeid_id=externalid.typeid_id, outer_id=externalid.outer_id)
    row = next(rows, None)
    if row is None:
        row = await loader.insert(externalid)
        result.id = row.id
        result.msg = "ok"
    else:
        result.id = row.id
        result.msg = "fail"
    return result

@strawberry.mutation(description="definies a new external id for an entity")
async def externalid_delete(self, info: strawberry.types.Info, externalid: ExternalIdUpdateGQLModel) -> ExternalIdResultGQLModel:
    loader = getLoaders(info).externalids
    result = ExternalIdResultGQLModel()
    rows = await loader.filter_by(inner_id=externalid.inner_id, typeid_id=externalid.typeid_id, outer_id=externalid.outer_id)
    row = next(rows, None)
    if row is not None:
        row = await loader.delete(row.id)
        result.msg = "ok"
    else:
        result.id = None
        result.msg = "fail"
    return result