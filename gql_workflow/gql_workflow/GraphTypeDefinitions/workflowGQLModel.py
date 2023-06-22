import datetime
import strawberry
from typing import List, Optional, Union, Annotated

import gql_workflow.GraphTypeDefinitions

def getLoaders(info):
    return info.context["all"]

WorkflowTransitionGQLModel = Annotated["WorkflowTransitionGQLModel", strawberry.lazy(".workflowTransitionGQLModel")]
WorkflowStateUserGQLModel = Annotated["WorkflowStateUserGQLModel", strawberry.lazy(".workflowStateUserGQLModel")]
WorkflowStateGQLModel = Annotated["WorkflowStateGQLModel", strawberry.lazy(".workflowStateGQLModel")]


@strawberry.federation.type(keys=["id"], description="""Entity graph of dataflow""")
class WorkflowGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoaders(info).workflows
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
    
    @strawberry.field(description="""states in the workflow""")
    async def states(self, info: strawberry.types.Info) -> List["WorkflowStateGQLModel"]:
        loader = getLoaders(info).workflowstates
        result = await loader.filter_by(workflow_id=self.id)
        return result

    @strawberry.field(description="""transitions in the workflow""")
    async def transitions(self, info: strawberry.types.Info) -> List["WorkflowTransitionGQLModel"]:
        loader = getLoaders(info).workflowtransitions
        result = await loader.filter_by(workflow_id=self.id)
        return result

#####################################################################
#
# Special fields for query
#
#####################################################################
@strawberry.field(description="""Finds an workflow by their id""")
async def workflow_by_id(
    self, info: strawberry.types.Info, id: strawberry.ID
) -> Union["WorkflowGQLModel", None]:
    result = await WorkflowGQLModel.resolve_reference(info, id)
    return result

@strawberry.field(description="""Finds an workflow page""")
async def workflow_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 20
) -> List["WorkflowGQLModel"]:
    loader = getLoaders(info).workflows
    result = await loader.page(skip=skip, limit=limit)
    #result = await WorkflowGQLModel.resolve_reference(info, id)
    return result

    
#####################################################################
#
# Mutation section
#
#####################################################################


@strawberry.input
class WorkflowInsertGQLModel:
    name: str
    name_en: Optional[str] = ""

    type_id: Optional[strawberry.ID] = None
    id: Optional[strawberry.ID] = None

@strawberry.input
class WorkflowUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberry.ID
    name: Optional[str] = None
    name_en: Optional[str] = None
    type_id: Optional[strawberry.ID] = None
    
@strawberry.type
class WorkflowResultGQLModel:
    id: strawberry.ID = None
    msg: str = None

    @strawberry.field(description="""Result of workflow operation""")
    async def workflow(self, info: strawberry.types.Info) -> Union[WorkflowGQLModel, None]:
        result = await WorkflowGQLModel.resolve_reference(info, self.id)
        return result
    

@strawberry.mutation(description="""Creates a new workflow""")
async def workflow_insert(self, info: strawberry.types.Info, workflow: WorkflowInsertGQLModel) -> WorkflowResultGQLModel:
    loader = getLoaders(info).workflows
    row = await loader.insert(workflow)
    result = WorkflowResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberry.mutation
async def workflow_update(self, info: strawberry.types.Info, workflow: WorkflowUpdateGQLModel) -> WorkflowResultGQLModel:
    loader = getLoaders(info).workflows
    row = await loader.update(workflow)
    result = WorkflowResultGQLModel()
    result.msg = "ok"
    result.id = workflow.id
    if row is None:
        result.msg = "fail"
        
    return result