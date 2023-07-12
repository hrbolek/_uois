import datetime
import strawberry
from typing import List, Optional, Union, Annotated

import gql_workflow.GraphTypeDefinitions

def getLoaders(info):
    return info.context["all"]

UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]

WorkflowGQLModel = Annotated["WorkflowGQLModel", strawberry.lazy(".workflowGQLModel")]
WorkflowStateGQLModel = Annotated["WorkflowStateGQLModel", strawberry.lazy(".workflowStateGQLModel")]
WorkflowStateResultGQLModel = Annotated["WorkflowStateResultGQLModel", strawberry.lazy(".workflowStateGQLModel")]

@strawberry.federation.type(keys=["id"], description="""Entity defining users with some rights for the state in dataflow (node in graph)""")
class WorkflowStateUserGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoaders(info).workflowstateusers
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
            result.__strawberry_definition__ = cls._type_definition # some version of strawberry changed :(
        return result


    @strawberry.field(description="""primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Timestamp""")
    def lastchange(self) -> strawberry.ID:
        return self.lastchange
   
    @strawberry.field(description="""User""")
    async def user(self, info: strawberry.types.Info) -> Union["UserGQLModel", None]:
        result = await gql_workflow.GraphTypeDefinitions.UserGQLModel.resolve_reference(id=self.user_id)
        return result

    @strawberry.field(description="""Group for which the user has some right""")
    async def group(self, info: strawberry.types.Info) -> Union["GroupGQLModel", None]:
        result = await gql_workflow.GraphTypeDefinitions.GroupGQLModel.resolve_reference(id=self.group_id)
        return result

    @strawberry.field(description="""State""")
    async def state(self, info: strawberry.types.Info) -> Union["WorkflowStateGQLModel", None]:
        result = await gql_workflow.GraphTypeDefinitions.WorkflowStateGQLModel.resolve_reference(info, self.workflowstate_id)
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

@strawberry.input(description="""""")
class WorkflowStateAddUserGQLModel:
    workflowstate_id: strawberry.ID = strawberry.field(default=None, description="Identification of workflow state")
    user_id: strawberry.ID = strawberry.field(default=None, description="Identification of user")
    group_id: strawberry.ID = strawberry.field(default=None, description="Identification of group for which the user has appropriate access level")
    accesslevel: int

@strawberry.input(description="""""")
class WorkflowStateRemoveUserGQLModel:
    workflowstate_id: strawberry.ID = strawberry.field(default=None, description="Identification of workflow state")
    user_id: strawberry.ID = strawberry.field(default=None, description="Identification of user")
    group_id: strawberry.ID = strawberry.field(default=None, description="Identification of group for which the user has appropriate access level")

@strawberry.mutation(description="""Adds or updates a user & group at the workflow state""")
async def workflow_state_add_user(self, info: strawberry.types.Info, payload: WorkflowStateAddUserGQLModel) -> Optional["WorkflowStateResultGQLModel"]:
    loader = getLoaders(info).workflowstateusers
    existing = await loader.filter_by(workflowstate_id=payload.workflowstate_id, user_id=payload.user_id, group_id=payload.group_id)
    result = gql_workflow.GraphTypeDefinitions.WorkflowStateResultGQLModel()
    result.msg = "ok"
    row = next(existing, None)
    if  row is None:
        row = await loader.insert(payload)
        result.id = payload.workflowstate_id
    else:
        row = await loader.update(row, {"accesslevel": payload.accesslevel})
        if row is None:
            result.id = None
            result.msg = "fail"
        result.id = payload.workflowstate_id
    return result

@strawberry.mutation(description="""Remove the user & group from the workflow state""")
async def workflow_state_remove_user(self, info: strawberry.types.Info, payload: WorkflowStateRemoveUserGQLModel) -> Optional["WorkflowStateResultGQLModel"]:
    loader = getLoaders(info).workflowstateusers
    existing = await loader.filter_by(workflowstate_id=payload.workflowstate_id, user_id=payload.user_id, group_id=payload.group_id)
    existing = next(existing, None)
    result = gql_workflow.GraphTypeDefinitions.WorkflowStateResultGQLModel()
    result.id = payload.workflowstate_id
    if existing is None:
        result.msg = "fail"
    else:
        await loader.delete(existing.id)
        result.msg = "ok"
    return result
