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
    
    @strawberryA.field(description="""states in the workflow""")
    async def states(self, info: strawberryA.types.Info) -> List["WorkflowStateGQLModel"]:
        loader = getLoaders(info).workflowstates
        result = await loader.filter_by(workflow_id=self.id)
        return result

    @strawberryA.field(description="""transitions in the workflow""")
    async def transitions(self, info: strawberryA.types.Info) -> List["WorkflowTransitionGQLModel"]:
        loader = getLoaders(info).workflowtransitions
        result = await loader.filter_by(workflow_id=self.id)
        return result


@strawberryA.federation.type(keys=["id"], description="""Entity defining a state in dataflow (node in graph)""")
class WorkflowStateGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).workflowstates
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
    
    @strawberryA.field(description="""forward transitions""")
    async def next_transitions(self, info: strawberryA.types.Info) -> List["WorkflowTransitionGQLModel"]:
        loader = getLoaders(info).workflowtransitions
        result = await loader.filter_by(sourcestate_id=self.id)
        return result

    @strawberryA.field(description="""forward transitions""")
    async def previous_transitions(self, info: strawberryA.types.Info) -> List["WorkflowTransitionGQLModel"]:
        loader = getLoaders(info).workflowtransitions
        result = await loader.filter_by(destinationstate_id=self.id)
        return result
    
@strawberryA.federation.type(keys=["id"], description="""Entity defining a possible state change""")
class WorkflowTransitionGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).workflowtransitions
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

    @strawberryA.field(description="""name""")
    async def source(self, info: strawberryA.types.Info) -> Union["WorkflowStateGQLModel", None]:
        result = await WorkflowStateGQLModel.resolve_reference(info, self.sourcestate_id)
        return result
    
    @strawberryA.field(description="""name""")
    async def destination(self, info: strawberryA.types.Info) -> Union["WorkflowStateGQLModel", None]:
        result = await WorkflowStateGQLModel.resolve_reference(info, self.destinationstate_id)
        return result


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

    @strawberryA.field(description="""Proxy users attached to this authorization""")
    async def users(self, info: strawberryA.types.Info) -> List["AuthorizationUserGQLModel"]:
        loader = getLoaders(info).authorizationusers
        result = await loader.filter_by(authorization_id=self.id)
        return result

    @strawberryA.field(description="""Proxy groups attached to this authorization""")
    async def groups(self, info: strawberryA.types.Info) -> List["AuthorizationGroupGQLModel"]:
        loader = getLoaders(info).authorizationgroups
        result = await loader.filter_by(authorization_id=self.id)
        return result

    @strawberryA.field(description="""Proxy role types attached to this authorization""")
    async def role_types(self, info: strawberryA.types.Info) -> List["AuthorizationRoleTypeGQLModel"]:
        loader = getLoaders(info).authorizationroletypes
        result = await loader.filter_by(authorization_id=self.id)
        return result


@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing an access to information"""
)
class AuthorizationUserGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).authorizationusers
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self, info: strawberryA.types.Info) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description=""""Read, write, or other?""")
    def accesslevel(self, info: strawberryA.types.Info) -> int:
        return self.accesslevel
    
    @strawberryA.field(description="""To which authorization this access definition belongs""")
    async def authorization(self, info: strawberryA.types.Info) -> AuthorizationGQLModel:
        result = await AuthorizationGQLModel.resolve_reference(info, self.authorization_id)
        return result
    
    @strawberryA.field(description="""User which has this access""")
    async def user(self, info: strawberryA.types.Info) -> UserGQLModel:
        result = UserGQLModel(id=self.user_id)
        return result
    

@strawberryA.federation.type(extend=True, keys=["id"])
class RoleTypeGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return RoleTypeGQLModel(id=id)

@strawberryA.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return GroupGQLModel(id=id)

@strawberryA.federation.type(
    keys=["id"], description="""Entity representing an access to information"""
)
class AuthorizationRoleTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).authorizationusers
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self, info: strawberryA.types.Info) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description="""Read, write, or other?""")
    def accesslevel(self, info: strawberryA.types.Info) -> int:
        return self.accesslevel
   
    @strawberryA.field(description="""To which authorization this access definition belongs""")
    async def authorization(self, info: strawberryA.types.Info) -> AuthorizationGQLModel:
        result = await AuthorizationGQLModel.resolve_reference(info, self.authorization_id)
        return result
    
    @strawberryA.field(description="""Role type which user must play in the group to have this access""")
    async def role_type(self, info: strawberryA.types.Info) -> "RoleTypeGQLModel":
        result = RoleTypeGQLModel(id=self.roletype_id)
        return result
    
    @strawberryA.field(description="""Group where the user having appropriate role has this access""")
    async def group(self, info: strawberryA.types.Info) -> "GroupGQLModel":
        result = GroupGQLModel(id=self.group_id)
        return result
    

@strawberryA.federation.type(
    keys=["id"], description="""Entity representing an access to information"""
)
class AuthorizationGroupGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).authorizationusers
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self, info: strawberryA.types.Info) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description="""Read, write, or other?""")
    def accesslevel(self, info: strawberryA.types.Info) -> int:
        return self.accesslevel
   
    @strawberryA.field(description="""To which authorization this access definition belongs""")
    async def authorization(self, info: strawberryA.types.Info) -> AuthorizationGQLModel:
        result = await AuthorizationGQLModel.resolve_reference(info, self.authorization_id)
        return result
    
    @strawberryA.field(description="""Group which has this access""")
    async def group(self, info: strawberryA.types.Info) -> "GroupGQLModel":
        result = GroupGQLModel(id=self.group_id)
        return result

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

    @strawberryA.field(description="""Finds an workflow page""")
    async def workflow_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
    ) -> List[WorkflowGQLModel]:
        loader = getLoaders(info).workflows
        result = await loader.page(skip=skip, limit=limit)
        #result = await WorkflowGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds an authorization entity by its id""")
    async def authorization_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[AuthorizationGQLModel, None]:
        result = await AuthorizationGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Gets a page of authorizations""")
    async def authorization_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
    ) -> List[AuthorizationGQLModel]:
        loader = getLoaders(info).authorizations
        result = await loader.page(skip=skip, limit=limit)
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

    @strawberryA.field(description="""Result of workflow operation""")
    async def workflow(self, info: strawberryA.types.Info) -> Union[WorkflowGQLModel, None]:
        result = await WorkflowGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.input
class WorkflowStateInsertGQLModel:
    workflow_id: strawberryA.ID
    name: str
    name_en: Optional[str] = ""   
    id: Optional[strawberryA.ID] = None

@strawberryA.input
class WorkflowStateUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID
    name: Optional[str] = None
    name_en: Optional[str] = None
    
@strawberryA.type
class WorkflowStateResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of workflow state operation""")
    async def workflow(self, info: strawberryA.types.Info) -> Union[WorkflowStateGQLModel, None]:
        result = await WorkflowStateGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberryA.type
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

    @strawberryA.mutation
    async def workflow_state_insert(self, info: strawberryA.types.Info, state: WorkflowStateInsertGQLModel) -> WorkflowStateResultGQLModel:
        loader = getLoaders(info).workflowstates
        row = await loader.insert(state)
        result = WorkflowStateResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation
    async def workflow_state_update(self, info: strawberryA.types.Info, state: WorkflowStateUpdateGQLModel) -> WorkflowStateResultGQLModel:
        loader = getLoaders(info).workflowstates
        row = await loader.update(state)
        result = WorkflowStateResultGQLModel()
        result.msg = "ok"
        result.id = state.id
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

schema = strawberryA.federation.Schema(query=Query, types=(UserGQLModel,), mutation=Mutation)
#schema = strawberryA.federation.Schema(query=Query, mutation=Mutation)
