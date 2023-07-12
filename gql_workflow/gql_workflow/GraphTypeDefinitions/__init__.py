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

# @strawberryA.federation.type(keys=["id"], description="""Entity graph of dataflow""")
# class WorkflowGQLModel:
#     @classmethod
#     async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
#         loader = getLoaders(info).workflows
#         result = await loader.load(id)
#         if result is not None:
#             result._type_definition = cls._type_definition  # little hack :)
#         return result

#     @strawberryA.field(description="""primary key""")
#     def id(self) -> strawberryA.ID:
#         return self.id

#     @strawberryA.field(description="""Timestamp""")
#     def lastchange(self) -> strawberryA.ID:
#         return self.lastchange

#     @strawberryA.field(description="""name""")
#     def name(self) -> str:
#         return self.name
    
#     @strawberryA.field(description="""states in the workflow""")
#     async def states(self, info: strawberryA.types.Info) -> List["WorkflowStateGQLModel"]:
#         loader = getLoaders(info).workflowstates
#         result = await loader.filter_by(workflow_id=self.id)
#         return result

#     @strawberryA.field(description="""transitions in the workflow""")
#     async def transitions(self, info: strawberryA.types.Info) -> List["WorkflowTransitionGQLModel"]:
#         loader = getLoaders(info).workflowtransitions
#         result = await loader.filter_by(workflow_id=self.id)
#         return result


# @strawberryA.federation.type(keys=["id"], description="""Entity defining a state in dataflow (node in graph)""")
# class WorkflowStateGQLModel:
#     @classmethod
#     async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
#         loader = getLoaders(info).workflowstates
#         result = await loader.load(id)
#         if result is not None:
#             result._type_definition = cls._type_definition  # little hack :)
#         return result

#     @strawberryA.field(description="""primary key""")
#     def id(self) -> strawberryA.ID:
#         return self.id

#     @strawberryA.field(description="""Timestamp""")
#     def lastchange(self) -> strawberryA.ID:
#         return self.lastchange

#     @strawberryA.field(description="""name""")
#     def name(self) -> str:
#         return self.name
    
#     @strawberryA.field(description="""if teh state is enabled""")
#     def valid(self) -> str:
#         return self.valid
    
#     @strawberryA.field(description="""outcomming transitions""")
#     async def next_transitions(self, info: strawberryA.types.Info) -> List["WorkflowTransitionGQLModel"]:
#         loader = getLoaders(info).workflowtransitions
#         result = await loader.filter_by(sourcestate_id=self.id)
#         return result

#     @strawberryA.field(description="""incomming transitions""")
#     async def previous_transitions(self, info: strawberryA.types.Info) -> List["WorkflowTransitionGQLModel"]:
#         loader = getLoaders(info).workflowtransitions
#         result = await loader.filter_by(destinationstate_id=self.id)
#         return result
    
#     @strawberryA.field(description="""User rights""")
#     async def users(self, info: strawberryA.types.Info) -> List["WorkflowStateUserGQLModel"]:
#         loader = getLoaders(info).workflowstateusers
#         result = await loader.filter_by(workflowstate_id=self.id)
#         return result
    
#     @strawberryA.field(description="""User rights""")
#     async def roletypes(self, info: strawberryA.types.Info) -> List["WorkflowStateRoleTypeGQLModel"]:
#         loader = getLoaders(info).workflowstateroletypes
#         result = await loader.filter_by(workflowstate_id=self.id)
#         return result
    
#     @strawberryA.field(description="""The owing workflow""")
#     async def workflow(self, info: strawberryA.types.Info) -> Union["WorkflowGQLModel", None]:
#         result = await WorkflowGQLModel.resolve_reference(info, id=self.workflow_id)
#         return result
    

# @strawberryA.federation.type(keys=["id"], description="""Entity defining users with some rights for the state in dataflow (node in graph)""")
# class WorkflowStateUserGQLModel:
#     @classmethod
#     async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
#         loader = getLoaders(info).workflowstateusers
#         result = await loader.load(id)
#         if result is not None:
#             result._type_definition = cls._type_definition  # little hack :)
#         return result

#     @strawberryA.field(description="""primary key""")
#     def id(self) -> strawberryA.ID:
#         return self.id

#     @strawberryA.field(description="""Timestamp""")
#     def lastchange(self) -> strawberryA.ID:
#         return self.lastchange
   
#     @strawberryA.field(description="""User""")
#     async def user(self, info: strawberryA.types.Info) -> Union["UserGQLModel", None]:
#         result = await UserGQLModel.resolve_reference(id=self.user_id)
#         return result

#     @strawberryA.field(description="""Group for which the user has some right""")
#     async def group(self, info: strawberryA.types.Info) -> Union["GroupGQLModel", None]:
#         result = await GroupGQLModel.resolve_reference(id=self.group_id)
#         return result

#     @strawberryA.field(description="""State""")
#     async def state(self, info: strawberryA.types.Info) -> Union["WorkflowStateGQLModel", None]:
#         result = await WorkflowStateGQLModel.resolve_reference(info, self.workflowstate_id)
#         return result

# @strawberryA.federation.type(keys=["id"], description="""Entity defining role types with some rights for the state in dataflow (node in graph)""")
# class WorkflowStateRoleTypeGQLModel:
#     @classmethod
#     async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
#         loader = getLoaders(info).workflowstateusers
#         result = await loader.load(id)
#         if result is not None:
#             result._type_definition = cls._type_definition  # little hack :)
#         return result

#     @strawberryA.field(description="""primary key""")
#     def id(self) -> strawberryA.ID:
#         return self.id

#     @strawberryA.field(description="""Timestamp""")
#     def lastchange(self) -> strawberryA.ID:
#         return self.lastchange
   
#     @strawberryA.field(description="""State""")
#     async def state(self, info: strawberryA.types.Info) -> Union["WorkflowStateGQLModel", None]:
#         result = await WorkflowStateGQLModel.resolve_reference(info, self.workflowstate_id)
#         return result

#     @strawberryA.field(description="""Role type with some rights""")
#     async def role_type(self, info: strawberryA.types.Info) -> Union["RoleTypeGQLModel", None]:
#         result = await RoleTypeGQLModel.resolve_reference(id=self.roletype_id)
#         return result


# @strawberryA.federation.type(keys=["id"], description="""Entity defining a possible state change""")
# class WorkflowTransitionGQLModel:
#     @classmethod
#     async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
#         loader = getLoaders(info).workflowtransitions
#         result = await loader.load(id)
#         if result is not None:
#             result._type_definition = cls._type_definition  # little hack :)
#         return result

#     @strawberryA.field(description="""primary key""")
#     def id(self) -> strawberryA.ID:
#         return self.id

#     @strawberryA.field(description="""Timestamp""")
#     def lastchange(self) -> strawberryA.ID:
#         return self.lastchange

#     @strawberryA.field(description="""name""")
#     def name(self) -> str:
#         return self.name

#     @strawberryA.field(description="""if the transition is enabled""")
#     def valid(self) -> str:
#         return self.valid
    
#     @strawberryA.field(description="""name""")
#     async def source(self, info: strawberryA.types.Info) -> Union["WorkflowStateGQLModel", None]:
#         result = await WorkflowStateGQLModel.resolve_reference(info, self.sourcestate_id)
#         return result
    
#     @strawberryA.field(description="""name""")
#     async def destination(self, info: strawberryA.types.Info) -> Union["WorkflowStateGQLModel", None]:
#         result = await WorkflowStateGQLModel.resolve_reference(info, self.destinationstate_id)
#         return result

#     @strawberryA.field(description="""The owing workflow""")
#     async def workflow(self, info: strawberryA.types.Info) -> Union["WorkflowGQLModel", None]:
#         result = await WorkflowGQLModel.resolve_reference(info, id=self.workflow_id)
#         return result
    


# @strawberryA.federation.type(
#     keys=["id"], description="""Entity representing an access to information"""
# )
# class AuthorizationGQLModel:
#     @classmethod
#     async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
#         loader = getLoaders(info).authorizations
#         result = await loader.load(id)
#         if result is not None:
#             result._type_definition = cls._type_definition  # little hack :)
#         return result

#     @strawberryA.field(description="""Entity primary key""")
#     def id(self, info: strawberryA.types.Info) -> strawberryA.ID:
#         return self.id

#     @strawberryA.field(description="""Proxy users attached to this authorization""")
#     async def users(self, info: strawberryA.types.Info) -> List["AuthorizationUserGQLModel"]:
#         loader = getLoaders(info).authorizationusers
#         result = await loader.filter_by(authorization_id=self.id)
#         return result

#     @strawberryA.field(description="""Proxy groups attached to this authorization""")
#     async def groups(self, info: strawberryA.types.Info) -> List["AuthorizationGroupGQLModel"]:
#         loader = getLoaders(info).authorizationgroups
#         result = await loader.filter_by(authorization_id=self.id)
#         return result

#     @strawberryA.field(description="""Proxy role types attached to this authorization""")
#     async def role_types(self, info: strawberryA.types.Info) -> List["AuthorizationRoleTypeGQLModel"]:
#         loader = getLoaders(info).authorizationroletypes
#         result = await loader.filter_by(authorization_id=self.id)
#         return result


# @strawberryA.federation.type(extend=True, keys=["id"])
# class UserGQLModel:
#     id: strawberryA.ID = strawberryA.federation.field(external=True)

#     @classmethod
#     async def resolve_reference(cls, id: strawberryA.ID):
#         return UserGQLModel(id=id)


# @strawberryA.federation.type(
#     keys=["id"], description="""Entity representing an access to information"""
# )
# class AuthorizationUserGQLModel:
#     @classmethod
#     async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
#         loader = getLoaders(info).authorizationusers
#         result = await loader.load(id)
#         if result is not None:
#             result._type_definition = cls._type_definition  # little hack :)
#         return result

#     @strawberryA.field(description="""Entity primary key""")
#     def id(self, info: strawberryA.types.Info) -> strawberryA.ID:
#         return self.id
    
#     @strawberryA.field(description=""""Read, write, or other?""")
#     def accesslevel(self, info: strawberryA.types.Info) -> int:
#         return self.accesslevel
    
#     @strawberryA.field(description="""To which authorization this access definition belongs""")
#     async def authorization(self, info: strawberryA.types.Info) -> AuthorizationGQLModel:
#         result = await AuthorizationGQLModel.resolve_reference(info, self.authorization_id)
#         return result
    
#     @strawberryA.field(description="""User which has this access""")
#     async def user(self, info: strawberryA.types.Info) -> UserGQLModel:
#         result = UserGQLModel(id=self.user_id)
#         return result
    

# @strawberryA.federation.type(extend=True, keys=["id"])
# class RoleTypeGQLModel:
#     id: strawberryA.ID = strawberryA.federation.field(external=True)

#     @classmethod
#     async def resolve_reference(cls, id: strawberryA.ID):
#         return RoleTypeGQLModel(id=id)

# @strawberryA.federation.type(extend=True, keys=["id"])
# class GroupGQLModel:
#     id: strawberryA.ID = strawberryA.federation.field(external=True)

#     @classmethod
#     async def resolve_reference(cls, id: strawberryA.ID):
#         return GroupGQLModel(id=id)

# @strawberryA.federation.type(
#     keys=["id"], description="""Entity representing an access to information"""
# )
# class AuthorizationRoleTypeGQLModel:
#     @classmethod
#     async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
#         loader = getLoaders(info).authorizationusers
#         result = await loader.load(id)
#         if result is not None:
#             result._type_definition = cls._type_definition  # little hack :)
#         return result

#     @strawberryA.field(description="""Entity primary key""")
#     def id(self, info: strawberryA.types.Info) -> strawberryA.ID:
#         return self.id
    
#     @strawberryA.field(description="""Read, write, or other?""")
#     def accesslevel(self, info: strawberryA.types.Info) -> int:
#         return self.accesslevel
   
#     @strawberryA.field(description="""To which authorization this access definition belongs""")
#     async def authorization(self, info: strawberryA.types.Info) -> AuthorizationGQLModel:
#         result = await AuthorizationGQLModel.resolve_reference(info, self.authorization_id)
#         return result
    
#     @strawberryA.field(description="""Role type which user must play in the group to have this access""")
#     async def role_type(self, info: strawberryA.types.Info) -> "RoleTypeGQLModel":
#         result = RoleTypeGQLModel(id=self.roletype_id)
#         return result
    
#     @strawberryA.field(description="""Group where the user having appropriate role has this access""")
#     async def group(self, info: strawberryA.types.Info) -> "GroupGQLModel":
#         result = GroupGQLModel(id=self.group_id)
#         return result
    

# @strawberryA.federation.type(
#     keys=["id"], description="""Entity representing an access to information"""
# )
# class AuthorizationGroupGQLModel:
#     @classmethod
#     async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
#         loader = getLoaders(info).authorizationusers
#         result = await loader.load(id)
#         if result is not None:
#             result._type_definition = cls._type_definition  # little hack :)
#         return result

#     @strawberryA.field(description="""Entity primary key""")
#     def id(self, info: strawberryA.types.Info) -> strawberryA.ID:
#         return self.id
    
#     @strawberryA.field(description="""Read, write, or other?""")
#     def accesslevel(self, info: strawberryA.types.Info) -> int:
#         return self.accesslevel
   
#     @strawberryA.field(description="""To which authorization this access definition belongs""")
#     async def authorization(self, info: strawberryA.types.Info) -> AuthorizationGQLModel:
#         result = await AuthorizationGQLModel.resolve_reference(info, self.authorization_id)
#         return result
    
#     @strawberryA.field(description="""Group which has this access""")
#     async def group(self, info: strawberryA.types.Info) -> "GroupGQLModel":
#         result = GroupGQLModel(id=self.group_id)
#         return result

# from gql_workflow.GraphResolvers import resolveAuthorizationById, resolveWorkflowById

# from gql_workflow.DBFeeder import randomWorkflowData


# @strawberryA.type(description="""Type for query root""")
# class Query:
#     @strawberryA.field(description="""Finds an workflow by their id""")
#     async def workflow_by_id(
#         self, info: strawberryA.types.Info, id: strawberryA.ID
#     ) -> Union[WorkflowGQLModel, None]:
#         result = await WorkflowGQLModel.resolve_reference(info, id)
#         return result

#     @strawberryA.field(description="""Finds an workflow page""")
#     async def workflow_page(
#         self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
#     ) -> List[WorkflowGQLModel]:
#         loader = getLoaders(info).workflows
#         result = await loader.page(skip=skip, limit=limit)
#         #result = await WorkflowGQLModel.resolve_reference(info, id)
#         return result

#     @strawberryA.field(description="""Finds an authorization entity by its id""")
#     async def authorization_by_id(
#         self, info: strawberryA.types.Info, id: strawberryA.ID
#     ) -> Union[AuthorizationGQLModel, None]:
#         result = await AuthorizationGQLModel.resolve_reference(info, id)
#         return result

#     @strawberryA.field(description="""Gets a page of authorizations""")
#     async def authorization_page(
#         self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
#     ) -> List[AuthorizationGQLModel]:
#         loader = getLoaders(info).authorizations
#         result = await loader.page(skip=skip, limit=limit)
#         return result

#     @strawberryA.field(description="""Finds an workflow by their id""")
#     async def random_workflow_data(
#         self, info: strawberryA.types.Info
#     ) -> Union[WorkflowGQLModel, None]:
#         result = await randomWorkflowData(AsyncSessionFromInfo(info))
#         return result


###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

from typing import Optional
import datetime

# @strawberryA.input
# class WorkflowInsertGQLModel:
#     name: str
#     name_en: Optional[str] = ""

#     type_id: Optional[strawberryA.ID] = None
#     id: Optional[strawberryA.ID] = None

# @strawberryA.input
# class WorkflowUpdateGQLModel:
#     lastchange: datetime.datetime
#     id: strawberryA.ID
#     name: Optional[str] = None
#     name_en: Optional[str] = None
#     type_id: Optional[strawberryA.ID] = None
    
# @strawberryA.type
# class WorkflowResultGQLModel:
#     id: strawberryA.ID = None
#     msg: str = None

#     @strawberryA.field(description="""Result of workflow operation""")
#     async def workflow(self, info: strawberryA.types.Info) -> Union[WorkflowGQLModel, None]:
#         result = await WorkflowGQLModel.resolve_reference(info, self.id)
#         return result

# @strawberryA.input
# class WorkflowStateInsertGQLModel:
#     workflow_id: strawberryA.ID
#     name: str
#     name_en: Optional[str] = ""   
#     valid: Optional[bool] = True
#     id: Optional[strawberryA.ID] = None

# @strawberryA.input
# class WorkflowStateUpdateGQLModel:
#     lastchange: datetime.datetime
#     id: strawberryA.ID
#     valid: Optional[bool] = None
#     name: Optional[str] = None
#     name_en: Optional[str] = None
    
# @strawberryA.type
# class WorkflowStateResultGQLModel:
#     id: strawberryA.ID = None
#     msg: str = None

#     @strawberryA.field(description="""Result of workflow state operation""")
#     async def state(self, info: strawberryA.types.Info) -> Union[WorkflowStateGQLModel, None]:
#         result = await WorkflowStateGQLModel.resolve_reference(info, self.id)
#         return result

# @strawberryA.input
# class WorkflowTransitionInsertGQLModel:
#     workflow_id: strawberryA.ID
#     sourcestate_id: strawberryA.ID
#     destinationstate_id: strawberryA.ID
#     name: str
#     name_en: Optional[str] = ""   
#     valid: Optional[bool] = True
#     id: Optional[strawberryA.ID] = None

# @strawberryA.input
# class WorkflowTransitionUpdateGQLModel:
#     lastchange: datetime.datetime
#     id: strawberryA.ID
#     sourcestate_id: Optional[strawberryA.ID]
#     destinationstate_id: Optional[strawberryA.ID]
#     valid: Optional[bool] = None
#     name: Optional[str] = None
#     name_en: Optional[str] = None
    
# @strawberryA.type
# class WorkflowTransitionResultGQLModel:
#     id: strawberryA.ID = None
#     msg: str = None

#     @strawberryA.field(description="""Result of workflow transition operation""")
#     async def transition(self, info: strawberryA.types.Info) -> Union[WorkflowTransitionGQLModel, None]:
#         result = await WorkflowTransitionGQLModel.resolve_reference(info, self.id)
#         return result


# @strawberryA.input
# class AuthorizationInsertGQLModel:
#     id: Optional[strawberryA.ID] = None

# @strawberryA.input
# class AuthorizationAddUserGQLModel:
#     authorization_id: strawberryA.ID
#     user_id: strawberryA.ID
#     accesslevel: int

# @strawberryA.input
# class AuthorizationAddGroupGQLModel:
#     authorization_id: strawberryA.ID
#     group_id: strawberryA.ID
#     accesslevel: int

# @strawberryA.input
# class AuthorizationAddRoleGQLModel:
#     authorization_id: strawberryA.ID
#     roletype_id: strawberryA.ID
#     group_id: strawberryA.ID
#     accesslevel: int

# @strawberryA.input
# class AuthorizationRemoveUserGQLModel:
#     authorization_id: strawberryA.ID
#     user_id: strawberryA.ID

# @strawberryA.input
# class AuthorizationRemoveGroupGQLModel:
#     authorization_id: strawberryA.ID
#     group_id: strawberryA.ID

# @strawberryA.input
# class AuthorizationRemoveRoleGQLModel:
#     authorization_id: strawberryA.ID
#     role_type_id: strawberryA.ID
#     group_id: strawberryA.ID

    
# @strawberryA.type
# class AuthorizationResultGQLModel:
#     id: strawberryA.ID = None
#     msg: str = None

#     @strawberryA.field(description="""Result of authorization operation""")
#     async def authorization(self, info: strawberryA.types.Info) -> Union[AuthorizationGQLModel, None]:
#         result = await AuthorizationGQLModel.resolve_reference(info, self.id)
#         return result



# @strawberryA.type
# class Mutation:
#     @strawberryA.mutation(description="""Creates a new authorization""")
#     async def authorization_insert(self, info: strawberryA.types.Info, authorization: AuthorizationInsertGQLModel) -> AuthorizationResultGQLModel:
#         loader = getLoaders(info).authorizations
#         row = await loader.insert(authorization)
#         result = AuthorizationResultGQLModel()
#         result.msg = "ok"
#         result.id = row.id
#         return result

#     @strawberryA.mutation(description="""Adds or updates a user at the authorization""")
#     async def authorization_add_user(self, info: strawberryA.types.Info, authorization: AuthorizationAddUserGQLModel) -> AuthorizationResultGQLModel:
#         loader = getLoaders(info).authorizationusers
#         existing = await loader.filter_by(authorization_id=authorization.authorization_id, user_id=authorization.user_id)
#         result = AuthorizationResultGQLModel()
#         result.msg = "ok"
#         row = next(existing, None)
#         if  row is None:
#             row = await loader.insert(authorization)
#             result.id = authorization.authorization_id
#         else:
#             row = await loader.update(row, {"accesslevel": authorization.accesslevel})
#             if row is None:
#                 result.id = None
#                 result.msg = "fail"
#             result.id = authorization.authorization_id
#         return result

#     @strawberryA.mutation(description="""Remove the user from the authorization""")
#     async def authorization_remove_user(self, info: strawberryA.types.Info, authorization: AuthorizationAddUserGQLModel) -> AuthorizationResultGQLModel:
#         loader = getLoaders(info).authorizationusers
#         existing = await loader.filter_by(authorization_id=authorization.authorization_id, user_id=authorization.user_id)
#         existing = next(existing, None)
#         result = AuthorizationResultGQLModel()
#         result.id = authorization.authorization_id
#         if existing is None:
#             result.msg = "fail"
#         else:
#             await loader.delete(existing.id)
#             result.msg = "ok"
#         return result

#     @strawberryA.mutation(description="""Adds or updates a group at the authorization""")
#     async def authorization_add_group(self, info: strawberryA.types.Info, authorization: AuthorizationAddGroupGQLModel) -> AuthorizationResultGQLModel:
#         loader = getLoaders(info).authorizationgroups
#         existing = await loader.filter_by(authorization_id=authorization.authorization_id, group_id=authorization.group_id)
#         result = AuthorizationResultGQLModel()
#         result.msg = "ok"
#         row = next(existing, None)
#         if  row is None:
#             row = await loader.insert(authorization)
#             result.id = authorization.authorization_id
#         else:
#             row = await loader.update(row, {"accesslevel": authorization.accesslevel})
#             if row is None:
#                 result.id = None
#                 result.msg = "fail"
#             result.id = authorization.authorization_id
#         return result

#     @strawberryA.mutation(description="""Remove the group from the authorization""")
#     async def authorization_remove_group(self, info: strawberryA.types.Info, authorization: AuthorizationAddGroupGQLModel) -> AuthorizationResultGQLModel:
#         loader = getLoaders(info).authorizationgroups
#         existing = await loader.filter_by(authorization_id=authorization.authorization_id, group_id=authorization.group_id)
#         existing = next(existing, None)
#         result = AuthorizationResultGQLModel()
#         result.id = authorization.authorization_id
#         if existing is None:
#             result.msg = "fail"
#         else:
#             await loader.delete(existing.id)
#             result.msg = "ok"
#         return result

#     @strawberryA.mutation(description="""Adds or updates a roletype at group at the authorization""")
#     async def authorization_add_role(self, info: strawberryA.types.Info, authorization: AuthorizationAddRoleGQLModel) -> AuthorizationResultGQLModel:
#         loader = getLoaders(info).authorizationroles
#         existing = await loader.filter_by(authorization_id=authorization.authorization_id, group_id=authorization.group_id, roletype_id=authorization.roletype_id)
#         result = AuthorizationResultGQLModel()
#         result.msg = "ok"
#         row = next(existing, None)
#         if  row is None:
#             row = await loader.insert(authorization)
#             result.id = authorization.authorization_id
#         else:
#             row = await loader.update(row, {"accesslevel": authorization.accesslevel})
#             if row is None:
#                 result.id = None
#                 result.msg = "fail"
#             result.id = authorization.authorization_id
#         return result

#     @strawberryA.mutation(description="""Remove the group from the authorization""")
#     async def authorization_remove_role(self, info: strawberryA.types.Info, authorization: AuthorizationAddRoleGQLModel) -> AuthorizationResultGQLModel:
#         loader = getLoaders(info).authorizationroles
#         existing = await loader.filter_by(authorization_id=authorization.authorization_id, group_id=authorization.group_id, roletype_id=authorization.roletype_id)
#         result = AuthorizationResultGQLModel()
#         if existing is None:
#             result.msg = "fail"
#         else:
#             await loader.delete(existing.id)
#             result.msg = "ok"
#         return result

#     @strawberryA.mutation(description="""Creates a new workflow""")
#     async def workflow_insert(self, info: strawberryA.types.Info, workflow: WorkflowInsertGQLModel) -> WorkflowResultGQLModel:
#         loader = getLoaders(info).workflows
#         row = await loader.insert(workflow)
#         result = WorkflowResultGQLModel()
#         result.msg = "ok"
#         result.id = row.id
#         return result

#     @strawberryA.mutation
#     async def workflow_update(self, info: strawberryA.types.Info, workflow: WorkflowUpdateGQLModel) -> WorkflowResultGQLModel:
#         loader = getLoaders(info).workflows
#         row = await loader.update(workflow)
#         result = WorkflowResultGQLModel()
#         result.msg = "ok"
#         result.id = workflow.id
#         if row is None:
#             result.msg = "fail"
            
#         return result

#     @strawberryA.mutation
#     async def workflow_state_insert(self, info: strawberryA.types.Info, state: WorkflowStateInsertGQLModel) -> WorkflowStateResultGQLModel:
#         loader = getLoaders(info).workflowstates
#         row = await loader.insert(state)
#         result = WorkflowStateResultGQLModel()
#         result.msg = "ok"
#         result.id = row.id
#         return result

#     @strawberryA.mutation
#     async def workflow_state_update(self, info: strawberryA.types.Info, state: WorkflowStateUpdateGQLModel) -> WorkflowStateResultGQLModel:
#         loader = getLoaders(info).workflowstates
#         row = await loader.update(state)
#         result = WorkflowStateResultGQLModel()
#         result.msg = "ok"
#         result.id = state.id
#         if row is None:
#             result.msg = "fail"
            
#         return result

#     @strawberryA.mutation
#     async def workflow_transition_insert(self, info: strawberryA.types.Info, state: WorkflowTransitionInsertGQLModel) -> WorkflowTransitionResultGQLModel:
#         loader = getLoaders(info).workflowtransitions
#         row = await loader.insert(state)
#         result = WorkflowTransitionResultGQLModel()
#         result.msg = "ok"
#         result.id = row.id
#         return result

#     @strawberryA.mutation
#     async def workflow_transition_update(self, info: strawberryA.types.Info, state: WorkflowTransitionUpdateGQLModel) -> WorkflowTransitionResultGQLModel:
#         loader = getLoaders(info).workflowtransitions
#         row = await loader.update(state)
#         result = WorkflowTransitionResultGQLModel()
#         result.msg = "ok"
#         result.id = state.id
#         if row is None:
#             result.msg = "fail"
            
#         return result

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

from .query import Query
from .mutation import Mutation
from .externals import UserGQLModel, GroupGQLModel, RoleTypeGQLModel

from .authorizationGQLModel import AuthorizationGQLModel, AuthorizationResultGQLModel
from .authorizationGroupGQLModel import AuthorizationGroupGQLModel
from .authorizationRoleTypeGQLModel import AuthorizationRoleTypeGQLModel
from .authorizationUserGQLModel import AuthorizationUserGQLModel

from .workflowGQLModel import WorkflowGQLModel
from .workflowStateGQLModel import WorkflowStateGQLModel
from .workflowStateGQLModel import WorkflowStateResultGQLModel
from .workflowStateUserGQLModel import WorkflowStateUserGQLModel
from .workflowTransitionGQLModel import WorkflowTransitionGQLModel
from .workflowStateRoleTypeGQLModel import WorkflowStateRoleTypeGQLModel

schema = strawberryA.federation.Schema(query=Query, types=(UserGQLModel,), mutation=Mutation)
#schema = strawberryA.federation.Schema(query=Query, mutation=Mutation)
