from typing import List, Union
import typing
import strawberry as strawberryA
import uuid

def AsyncSessionFromInfo(info):
    return info.context['session']

@strawberryA.federation.type(keys=["id"], description="""Entity graph of dataflow""")
class WorkflowGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveWorkflowById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

@strawberryA.federation.type(keys=["id"], description="""Entity representing an access to information""")
class AuthorizationGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveAuthorizationById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self, info: strawberryA.types.Info) -> strawberryA.ID:
        return self.id

from gql_workflow.GraphResolvers import resolveAuthorizationById, resolveWorkflowById

from gql_workflow.DBFeeder import randomWorkflowData

@strawberryA.type(description="""Type for query root""")
class Query:
   
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def workflow_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[WorkflowGQLModel, None]:
        result = await resolveWorkflowById(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Finds an authorization entity by its id""")
    async def authorization_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[AuthorizationGQLModel, None]:
        result = await resolveAuthorizationById(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def random_workflow_data(self, info: strawberryA.types.Info) -> Union[WorkflowGQLModel, None]:
        result = await randomWorkflowData(AsyncSessionFromInfo(info))
        return result