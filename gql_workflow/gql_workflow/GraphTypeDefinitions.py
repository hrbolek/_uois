from typing import List, Union
import typing
import strawberry as strawberryA
import uuid


def AsyncSessionFromInfo(info):
    print(
        "obsolete function used AsyncSessionFromInfo, use withInfo context manager instead"
    )
    return info.context["session"]

def getLoaders(info):
    return info.context['all']

@strawberryA.federation.type(keys=["id"], description="""Entity graph of dataflow""")
class WorkflowGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).workflows
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Timestamp""")
    def lastchange(self) -> strawberryA.ID:
        return self.lastchange

    @strawberryA.field(description="""name""")
    def name(self) -> str:
        return self.name


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing an access to information"""
)
class AuthorizationGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).authorizations
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self, info: strawberryA.types.Info) -> strawberryA.ID:
        return self.id


from gql_workflow.GraphResolvers import resolveAuthorizationById, resolveWorkflowById

from gql_workflow.DBFeeder import randomWorkflowData


@strawberryA.type(description="""Type for query root""")
class Query:
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def workflow_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[WorkflowGQLModel, None]:
        result = await WorkflowGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds an authorization entity by its id""")
    async def authorization_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[AuthorizationGQLModel, None]:
        result = await AuthorizationGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def random_workflow_data(
        self, info: strawberryA.types.Info
    ) -> Union[WorkflowGQLModel, None]:
        result = await randomWorkflowData(AsyncSessionFromInfo(info))
        return result


###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

from typing import Optional
import datetime

@strawberryA.input
class WorkflowInsertGQLModel:
    name: str
    name_en: Optional[str] = ""

    type_id: Optional[strawberryA.ID] = None
    id: Optional[strawberryA.ID] = None

@strawberryA.input
class WorkflowUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID
    name: Optional[str] = None
    name_en: Optional[str] = None
    type_id: Optional[strawberryA.ID] = None
    
    
@strawberryA.type
class WorkflowResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of user operation""")
    async def workflow(self, info: strawberryA.types.Info) -> Union[WorkflowGQLModel, None]:
        result = await WorkflowGQLModel.resolve_reference(info, self.id)
        return result


    
@strawberryA.federation.type(extend=True)
class Mutation:
    @strawberryA.mutation
    async def workflow_insert(self, info: strawberryA.types.Info, workflow: WorkflowInsertGQLModel) -> WorkflowResultGQLModel:
        loader = getLoaders(info).workflows
        row = await loader.insert(workflow)
        result = WorkflowResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation
    async def workflow_update(self, info: strawberryA.types.Info, workflow: WorkflowUpdateGQLModel) -> WorkflowResultGQLModel:
        loader = getLoaders(info).workflows
        row = await loader.update(workflow)
        result = WorkflowResultGQLModel()
        result.msg = "ok"
        result.id = workflow.id
        if row is None:
            result.msg = "fail"
            
        return result

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

#schema = strawberryA.federation.Schema(query=Query, types=(UserGQLModel,), mutation=Mutation)
schema = strawberryA.federation.Schema(query=Query, mutation=Mutation)
