import datetime
import strawberry
from typing import List, Optional, Union, Annotated
import gql_ug.GraphTypeDefinitions

def getLoader(info):
    return info.context["all"]

RoleGQLModel = Annotated["RoleGQLModel", strawberry.lazy(".roleGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a role type (like Dean)"""
)
class RoleTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        # result = await resolveRoleTypeById(session,  id)
        loader = getLoader(info).roletypes
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
            result.__strawberry_definition__ = cls._type_definition # some version of strawberry changed :(
        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Datetime stamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Role type name CZ""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Role type name EN""")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="""List of roles with this type""")
    async def roles(self, info: strawberry.types.Info) -> List["RoleGQLModel"]:
        # result = await resolveRoleForRoleType(session,  self.id)
        loader = getLoader(info).roles
        result = await loader.filter_by(roletype_id=self.id)
        return result

#####################################################################
#
# Special fields for query
#
#####################################################################
@strawberry.field(description="""Finds a role type by its id""")
async def role_type_by_id(
    self, info: strawberry.types.Info, id: strawberry.ID
) -> Union[RoleTypeGQLModel, None]:
    result = await RoleTypeGQLModel.resolve_reference(info, id)
    return result

@strawberry.field(description="""Finds all roles types paged""")
async def role_type_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10
) -> List[RoleTypeGQLModel]:
    # result = await resolveRoleTypeAll(session,  skip, limit)
    loader = getLoader(info).roletypes
    result = await loader.page(skip, limit)
    return result
    
#####################################################################
#
# Mutation section
#
#####################################################################
import datetime
@strawberry.input
class RoleTypeUpdateGQLModel:
    id: strawberry.ID
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None

@strawberry.input
class RoleTypeInsertGQLModel:
    id: Optional[strawberry.ID] = None
    name: Optional[str] = None
    name_en: Optional[str] = None

@strawberry.type
class RoleTypeResultGQLModel:
    id: strawberry.ID = None
    msg: str = None

    @strawberry.field(description="""Result of role type operation""")
    async def role_type(self, info: strawberry.types.Info) -> Union[RoleTypeGQLModel, None]:
        result = await RoleTypeGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(description="""Updates existing roleType record""")
async def role_type_update(self, 
    info: strawberry.types.Info, 
    role_type: RoleTypeUpdateGQLModel

) -> RoleTypeResultGQLModel:
    print("role_type_update", role_type, flush=True)
    loader = getLoader(info).roletypes
    row = await loader.update(role_type)
    if row is not None:
        print("role_type_update", row, row.name, row.id, flush=True)
    result = RoleTypeResultGQLModel()
    result.msg = "ok"
    result.id = role_type.id
    if row is None:
        result.msg = "fail"
    
    return result

@strawberry.mutation(description="""Inserts a new roleType record""")
async def role_type_insert(self, 
    info: strawberry.types.Info, 
    role_type: RoleTypeInsertGQLModel

) -> RoleTypeResultGQLModel:
    #print("role_type_update", role_type, flush=True)
    loader = getLoader(info).roletypes
    row = await loader.insert(role_type)
    if row is not None:
        print("role_type_update", row, row.name, row.id, flush=True)
    result = RoleTypeResultGQLModel()
    result.msg = "ok"
    result.id = row.id       
    return result    