import datetime
import strawberry
from typing import List, Optional, Union, Annotated

import gql_workflow.GraphTypeDefinitions

def getLoaders(info):
    return info.context["all"]

WorkflowGQLModel = Annotated["WorkflowGQLModel", strawberry.lazy(".workflowGQLModel")]
WorkflowStateGQLModel = Annotated["WorkflowStateGQLModel", strawberry.lazy(".workflowStateGQLModel")]
WorkflowStateResultGQLModel = Annotated["WorkflowStateResultGQLModel", strawberry.lazy(".workflowStateGQLModel")]
RoleTypeGQLModel = Annotated["RoleTypeGQLModel", strawberry.lazy(".externals")]

@strawberry.federation.type(keys=["id"], description="""Entity defining role types with some rights for the state in dataflow (node in graph)""")
class WorkflowStateRoleTypeGQLModel:
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
   
    @strawberry.field(description="""State""")
    async def state(self, info: strawberry.types.Info) -> Union["WorkflowStateGQLModel", None]:
        result = await gql_workflow.GraphTypeDefinitions.WorkflowStateGQLModel.resolve_reference(info, self.workflowstate_id)
        return result

    @strawberry.field(description="""Role type with some rights""")
    async def role_type(self, info: strawberry.types.Info) -> Union["RoleTypeGQLModel", None]:
        result = await gql_workflow.GraphTypeDefinitions.RoleTypeGQLModel.resolve_reference(id=self.roletype_id)
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
class WorkflowStateAddRoleGQLModel:
    workflowstate_id: strawberry.ID = strawberry.field(default=None, description="Identification of workflow state")
    roletype_id: strawberry.ID = strawberry.field(default=None, description="Identification of role type")
    accesslevel: int

@strawberry.input(description="""""")
class WorkflowStateRemoveRoleGQLModel:
    workflowstate_id: strawberry.ID = strawberry.field(default=None, description="Identification of workflow state")
    roletype_id: strawberry.ID = strawberry.field(default=None, description="Identification of role type")

@strawberry.mutation(description="""Adds or updates role at the workflow state""")
async def workflow_state_add_role(self, info: strawberry.types.Info, payload: WorkflowStateAddRoleGQLModel) -> Optional["WorkflowStateResultGQLModel"]:
    loader = getLoaders(info).workflowstateroletypes
    existing = await loader.filter_by(workflowstate_id=payload.workflowstate_id, roletype_id=payload.roletype_id)
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

@strawberry.mutation(description="""Remove the role from the workflow state""")
async def workflow_state_remove_role(self, info: strawberry.types.Info, payload: WorkflowStateRemoveRoleGQLModel) -> Optional["WorkflowStateResultGQLModel"]:
    loader = getLoaders(info).workflowstateroletypes
    existing = await loader.filter_by(workflowstate_id=payload.workflowstate_id, roletype_id=payload.roletype_id)
    existing = next(existing, None)
    result = gql_workflow.GraphTypeDefinitions.WorkflowStateResultGQLModel()
    result.id = payload.workflowstate_id
    if existing is None:
        result.msg = "fail"
    else:
        await loader.delete(existing.id)
        result.msg = "ok"
    return result
