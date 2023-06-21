import datetime
import strawberry
from typing import List, Optional, Union, Annotated

def getLoader(info):
    return info.context["all"]

RoleTypeGQLModel = Annotated["RoleTypeGQLModel", strawberry.lazy(".roleTypeGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a role type (like Dean)"""
)
class RoleCategoryGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoader(info).rolecategories
        result = await loader.load(id)
        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Primary key""")
    def lastchange(self) -> strawberry.ID:
        return self.lastchange

    @strawberry.field(description="""Role type name CZ""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Role type name EN""")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="""List of roles with this type""")
    async def role_types(self, info: strawberry.types.Info) -> List["RoleTypeGQLModel"]:
        # result = await resolveRoleForRoleType(session,  self.id)
        loader = getLoader(info).roletypes
        rows = await loader.filter_by(category_id=self.id)
        return rows
    
#####################################################################
#
# Special fields for query
#
#####################################################################
@strawberry.field(description="""Finds a role type by its id""")
async def role_category_by_id(
    self, info: strawberry.types.Info, id: strawberry.ID
) -> Union[RoleCategoryGQLModel, None]:
    result = await RoleCategoryGQLModel.resolve_reference(info,  id)
    return result

@strawberry.field(description="""gets role category page""")
async def role_category_page(
    self, info: strawberry.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 10
) -> Union[RoleCategoryGQLModel, None]:
    loader = getLoader(info).rolecategories
    result = await loader.page(skip, limit)
    return result

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input
class RoleCategoryUpdateGQLModel:
    id: strawberry.ID
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None

@strawberry.input
class RoleCategoryInsertGQLModel:
    id: Optional[strawberry.ID] = None
    name: Optional[str] = None
    name_en: Optional[str] = None

@strawberry.type
class RoleCategoryResultGQLModel:
    id: strawberry.ID = None
    msg: str = None

    @strawberry.field(description="""Result of role category operation""")
    async def role_category(self, info: strawberry.types.Info) -> Union[RoleCategoryGQLModel, None]:
        result = await RoleCategoryGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(description="""Updates a role category""")
async def role_category_update(self, 
    info: strawberry.types.Info, 
    role_category: RoleCategoryUpdateGQLModel

) -> RoleCategoryResultGQLModel:

    loader = getLoader(info).rolecategories
    row = await loader.update(role_category)

    result = RoleCategoryResultGQLModel()
    result.msg = "ok"
    result.id = role_category.id
    if row is None:
        result.msg = "fail"
    else:
        result.id = row.id

    
    return result

@strawberry.mutation(description="""Inserts a role category""")
async def role_category_insert(self, 
    info: strawberry.types.Info, 
    role_category: RoleCategoryInsertGQLModel

) -> RoleCategoryResultGQLModel:

    loader = getLoader(info).rolecategories
    row = await loader.insert(role_category)

    result = RoleCategoryResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    
    return result