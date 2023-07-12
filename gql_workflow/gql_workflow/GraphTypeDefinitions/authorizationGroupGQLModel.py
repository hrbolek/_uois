import datetime
import strawberry
from typing import List, Optional, Union, Annotated

import gql_workflow.GraphTypeDefinitions

def getLoaders(info):
    return info.context["all"]

GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]
AuthorizationGQLModel = Annotated["AuthorizationGQLModel", strawberry.lazy(".authorizationGQLModel")]
AuthorizationResultGQLModel = Annotated["AuthorizationResultGQLModel", strawberry.lazy(".authorizationGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Entity representing an access to information"""
)
class AuthorizationGroupGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoaders(info).authorizationusers
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
            result.__strawberry_definition__ = cls._type_definition # some version of strawberry changed :(
        return result


    @strawberry.field(description="""Entity primary key""")
    def id(self, info: strawberry.types.Info) -> strawberry.ID:
        return self.id
    
    @strawberry.field(description="""Read, write, or other?""")
    def accesslevel(self, info: strawberry.types.Info) -> int:
        return self.accesslevel
   
    @strawberry.field(description="""To which authorization this access definition belongs""")
    async def authorization(self, info: strawberry.types.Info) -> Optional[AuthorizationGQLModel]:
        result = await gql_workflow.GraphTypeDefinitions.AuthorizationGQLModel.resolve_reference(info, self.authorization_id)
        return result
    
    @strawberry.field(description="""Group which has this access""")
    async def group(self, info: strawberry.types.Info) -> Optional["GroupGQLModel"]:
        result = gql_workflow.GraphTypeDefinitions.GroupGQLModel(id=self.group_id)
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

@strawberry.input
class AuthorizationAddGroupGQLModel:
    authorization_id: strawberry.ID
    group_id: strawberry.ID
    accesslevel: int

@strawberry.input
class AuthorizationRemoveGroupGQLModel:
    authorization_id: strawberry.ID
    group_id: strawberry.ID


@strawberry.mutation(description="""Adds or updates a group at the authorization""")
async def authorization_add_group(self, info: strawberry.types.Info, authorization: AuthorizationAddGroupGQLModel) -> Optional["AuthorizationResultGQLModel"]:
    loader = getLoaders(info).authorizationgroups
    existing = await loader.filter_by(authorization_id=authorization.authorization_id, group_id=authorization.group_id)
    result = gql_workflow.GraphTypeDefinitions.AuthorizationResultGQLModel()
    result.msg = "ok"
    row = next(existing, None)
    if  row is None:
        row = await loader.insert(authorization)
        result.id = authorization.authorization_id
    else:
        row = await loader.update(row, {"accesslevel": authorization.accesslevel})
        if row is None:
            result.id = None
            result.msg = "fail"
        result.id = authorization.authorization_id
    return result

@strawberry.mutation(description="""Remove the group from the authorization""")
async def authorization_remove_group(self, info: strawberry.types.Info, authorization: AuthorizationRemoveGroupGQLModel) -> Optional["AuthorizationResultGQLModel"]:
    loader = getLoaders(info).authorizationgroups
    existing = await loader.filter_by(authorization_id=authorization.authorization_id, group_id=authorization.group_id)
    existing = next(existing, None)
    result = gql_workflow.GraphTypeDefinitions.AuthorizationResultGQLModel()
    result.id = authorization.authorization_id
    if existing is None:
        result.msg = "fail"
    else:
        await loader.delete(existing.id)
        result.msg = "ok"
    return result