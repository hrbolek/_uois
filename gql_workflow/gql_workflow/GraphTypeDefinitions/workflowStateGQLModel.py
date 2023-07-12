import datetime
import strawberry
from typing import List, Optional, Union, Annotated

import gql_workflow.GraphTypeDefinitions

def getLoaders(info):
    return info.context["all"]

UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]

WorkflowGQLModel = Annotated["WorkflowGQLModel", strawberry.lazy(".workflowGQLModel")]
WorkflowTransitionGQLModel = Annotated["WorkflowTransitionGQLModel", strawberry.lazy(".workflowTransitionGQLModel")]
WorkflowStateUserGQLModel = Annotated["WorkflowStateUserGQLModel", strawberry.lazy(".workflowStateUserGQLModel")]
WorkflowStateRoleTypeGQLModel = Annotated["WorkflowStateRoleTypeGQLModel", strawberry.lazy(".workflowStateRoleTypeGQLModel")]

@strawberry.federation.type(keys=["id"], description="""Entity defining a state in dataflow (node in graph)""")
class WorkflowStateGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoaders(info).workflowstates
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

    @strawberry.field(description="""name""")
    def name(self) -> str:
        return self.name
    
    @strawberry.field(description="""if the state is enabled""")
    def valid(self) -> Optional[bool]:
        return self.valid
    
    @strawberry.field(description="""outcomming transitions""")
    async def next_transitions(self, info: strawberry.types.Info) -> List["WorkflowTransitionGQLModel"]:
        loader = getLoaders(info).workflowtransitions
        result = await loader.filter_by(sourcestate_id=self.id)
        return result

    @strawberry.field(description="""incomming transitions""")
    async def previous_transitions(self, info: strawberry.types.Info) -> List["WorkflowTransitionGQLModel"]:
        loader = getLoaders(info).workflowtransitions
        result = await loader.filter_by(destinationstate_id=self.id)
        return result
    
    @strawberry.field(description="""User rights""")
    async def users(self, info: strawberry.types.Info) -> List["WorkflowStateUserGQLModel"]:
        loader = getLoaders(info).workflowstateusers
        result = await loader.filter_by(workflowstate_id=self.id)
        return result
    
    @strawberry.field(description="""User rights""")
    async def roletypes(self, info: strawberry.types.Info) -> List["WorkflowStateRoleTypeGQLModel"]:
        loader = getLoaders(info).workflowstateroletypes
        result = await loader.filter_by(workflowstate_id=self.id)
        return result
    
    @strawberry.field(description="""The owing workflow""")
    async def workflow(self, info: strawberry.types.Info) -> Union["WorkflowGQLModel", None]:
        result = await WorkflowGQLModel.resolve_reference(info, id=self.workflow_id)
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
class WorkflowStateInsertGQLModel:
    workflow_id: strawberry.ID
    name: str
    name_en: Optional[str] = ""   
    valid: Optional[bool] = True
    id: Optional[strawberry.ID] = None

@strawberry.input
class WorkflowStateUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberry.ID
    valid: Optional[bool] = None
    name: Optional[str] = None
    name_en: Optional[str] = None
    
@strawberry.type
class WorkflowStateResultGQLModel:
    id: strawberry.ID = None
    msg: str = None

    @strawberry.field(description="""Result of workflow state operation""")
    async def state(self, info: strawberry.types.Info) -> Union[WorkflowStateGQLModel, None]:
        result = await WorkflowStateGQLModel.resolve_reference(info, self.id)
        return result



@strawberry.mutation
async def workflow_state_insert(self, info: strawberry.types.Info, state: WorkflowStateInsertGQLModel) -> WorkflowStateResultGQLModel:
    loader = getLoaders(info).workflowstates
    row = await loader.insert(state)
    result = WorkflowStateResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberry.mutation
async def workflow_state_update(self, info: strawberry.types.Info, state: WorkflowStateUpdateGQLModel) -> WorkflowStateResultGQLModel:
    loader = getLoaders(info).workflowstates
    row = await loader.update(state)
    result = WorkflowStateResultGQLModel()
    result.msg = "ok"
    result.id = state.id
    if row is None:
        result.msg = "fail"
        
    return result