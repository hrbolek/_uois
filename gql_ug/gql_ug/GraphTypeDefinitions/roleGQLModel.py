import datetime
import strawberry
from typing import List, Optional, Union, Annotated
import gql_ug.GraphTypeDefinitions

def getLoader(info):
    return info.context["all"]

GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".groupGQLModel")]
UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".userGQLModel")]
RoleTypeGQLModel = Annotated["RoleTypeGQLModel", strawberry.lazy(".roleTypeGQLModel")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing a role of a user in a group (like user A in group B is Dean)""",
)
class RoleGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        # result = await resolverRoleById(session,  id)
        loader = getLoader(info).roles
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
            result.__strawberry_definition__ = cls._type_definition # some version of strawberry changed :(
        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Time stamp""")
    def lastchange(self) -> strawberry.ID:
        return self.lastchange

    @strawberry.field(description="""If an user has still this role""")
    def valid(self) -> bool:
        return self.valid

    @strawberry.field(description="""When an user has got this role""")
    def startdate(self) -> Union[str, None]:
        return self.startdate

    @strawberry.field(description="""When an user has been removed from this role""")
    def enddate(self) -> Union[str, None]:
        return self.enddate

    @strawberry.field(description="""Role type (like Dean)""")
    async def roletype(self, info: strawberry.types.Info) -> RoleTypeGQLModel:
        # result = await resolveRoleTypeById(session,  self.roletype_id)
        result = await gql_ug.GraphTypeDefinitions.RoleTypeGQLModel.resolve_reference(info, self.roletype_id)
        return result

    @strawberry.field(
        description="""User having this role. Must be member of group?"""
    )
    async def user(self, info: strawberry.types.Info) -> UserGQLModel:
        # result = await resolveUserById(session,  self.user_id)
        result = await gql_ug.GraphTypeDefinitions.UserGQLModel.resolve_reference(info, self.user_id)
        return result

    @strawberry.field(description="""Group where user has a role name""")
    async def group(self, info: strawberry.types.Info) -> GroupGQLModel:
        # result = await resolveGroupById(session,  self.group_id)
        result = await gql_ug.GraphTypeDefinitions.GroupGQLModel.resolve_reference(info, self.group_id)
        return result
    
#####################################################################
#
# Special fields for query
#
#####################################################################

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input
class RoleUpdateGQLModel:
    id: strawberry.ID
    lastchange: datetime.datetime
    valid: Optional[bool] = None
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None

@strawberry.input
class RoleInsertGQLModel:
    user_id: strawberry.ID
    group_id: strawberry.ID
    roletype_id: strawberry.ID
    id: Optional[strawberry.ID] = None
    valid: Optional[bool] = True
    startdate: Optional[datetime.datetime] = datetime.datetime.now()
    enddate: Optional[datetime.datetime] = None

@strawberry.type
class RoleResultGQLModel:
    id: strawberry.ID = None
    msg: str = None

    @strawberry.field(description="""Result of user operation""")
    async def role(self, info: strawberry.types.Info) -> Union[RoleGQLModel, None]:
        result = await RoleGQLModel.resolve_reference(info, self.id)
        return result
    

@strawberry.mutation(description="""Updates a role""")
async def role_update(self, 
    info: strawberry.types.Info, 
    role: RoleUpdateGQLModel
) -> RoleResultGQLModel:

    loader = getLoader(info).roles
    updatedrow = await loader.update(role)

    result = RoleResultGQLModel()
    result.msg = "ok"
    result.id = role.id
    
    if updatedrow is None:
        result.msg = "fail"        
    
    return result

@strawberry.mutation(description="""Inserts a role""")
async def role_insert(self, 
    info: strawberry.types.Info, 
    role: RoleInsertGQLModel
) -> RoleResultGQLModel:

    loader = getLoader(info).roles

    result = RoleResultGQLModel()
    result.msg = "ok"
    
    updatedrow = await loader.insert(role)
    result.id = updatedrow.id
    
    return result    