import datetime
import strawberry
from typing import List, Optional, Union, Annotated

import gql_workflow.GraphTypeDefinitions

def getLoaders(info):
    return info.context["all"]

WorkflowGQLModel = Annotated["WorkflowGQLModel", strawberry.lazy(".workflowGQLModel")]
WorkflowStateGQLModel = Annotated["WorkflowStateGQLModel", strawberry.lazy(".workflowStateGQLModel")]
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