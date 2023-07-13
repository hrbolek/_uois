import datetime
import strawberry
from typing import List, Optional, Union, Annotated

import gql_workflow.GraphTypeDefinitions

def getLoaders(info):
    return info.context["all"]

UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]
WorkflowGQLModel = Annotated["WorkflowGQLModel", strawberry.lazy(".workflowGQLModel")]
WorkflowStateGQLModel = Annotated["WorkflowStateGQLModel", strawberry.lazy(".workflowStateGQLModel")]

@strawberry.federation.type(keys=["id"], description="""Entity defining a possible state change""")
class WorkflowTransitionGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoaders(info).workflowtransitions
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

    @strawberry.field(description="""if the transition is enabled""")
    def valid(self) -> Optional[bool]:
        return self.valid
    
    @strawberry.field(description="""name""")
    async def source(self, info: strawberry.types.Info) -> Union["WorkflowStateGQLModel", None]:
        result = await gql_workflow.GraphTypeDefinitions.WorkflowStateGQLModel.resolve_reference(info, self.sourcestate_id)
        return result
    
    @strawberry.field(description="""name""")
    async def destination(self, info: strawberry.types.Info) -> Union["WorkflowStateGQLModel", None]:
        result = await gql_workflow.GraphTypeDefinitions.WorkflowStateGQLModel.resolve_reference(info, self.destinationstate_id)
        return result

    @strawberry.field(description="""The owing workflow""")
    async def workflow(self, info: strawberry.types.Info) -> Union["WorkflowGQLModel", None]:
        result = await gql_workflow.GraphTypeDefinitions.WorkflowGQLModel.resolve_reference(info, id=self.workflow_id)
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
class WorkflowTransitionInsertGQLModel:
    workflow_id: strawberry.ID
    sourcestate_id: strawberry.ID
    destinationstate_id: strawberry.ID
    name: str
    name_en: Optional[str] = ""   
    valid: Optional[bool] = True
    id: Optional[strawberry.ID] = None

@strawberry.input(description="""""")
class WorkflowTransitionUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberry.ID
    sourcestate_id: Optional[strawberry.ID]
    destinationstate_id: Optional[strawberry.ID]
    valid: Optional[bool] = None
    name: Optional[str] = None
    name_en: Optional[str] = None
    
@strawberry.type(description="""""")
class WorkflowTransitionResultGQLModel:
    id: strawberry.ID = None
    msg: str = None

    @strawberry.field(description="""Result of workflow transition operation""")
    async def transition(self, info: strawberry.types.Info) -> Union[WorkflowTransitionGQLModel, None]:
        result = await gql_workflow.GraphTypeDefinitions.WorkflowTransitionGQLModel.resolve_reference(info, self.id)
        return result
    

@strawberry.mutation(description="""""")
async def workflow_transition_insert(self, info: strawberry.types.Info, state: WorkflowTransitionInsertGQLModel) -> WorkflowTransitionResultGQLModel:
    loader = getLoaders(info).workflowtransitions
    row = await loader.insert(state)
    result = WorkflowTransitionResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberry.mutation(description="""""")
async def workflow_transition_update(self, info: strawberry.types.Info, state: WorkflowTransitionUpdateGQLModel) -> WorkflowTransitionResultGQLModel:
    loader = getLoaders(info).workflowtransitions
    row = await loader.update(state)
    result = WorkflowTransitionResultGQLModel()
    result.msg = "ok"
    result.id = state.id
    if row is None:
        result.msg = "fail"
        
    return result    