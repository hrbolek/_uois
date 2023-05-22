
from uoishelpers.dataloaders import createIdLoader, createFkeyLoader

from gql_workflow.DBDefinitions import (
    WorkflowModel,
    WorkflowStateModel,
    WorkflowStateRoleTypeModel,
    WorkflowStateUserModel,
    WorkflowTransitionModel,
    AuthorizationGroupModel,
    AuthorizationModel,
    AuthorizationRoleTypeModel,
    AuthorizationUserModel
)

dbmodels = {
    "workflows": WorkflowModel,
    "workflowstates": WorkflowStateModel,
    "workflowstateroletypes": WorkflowStateRoleTypeModel,
    "workflowstateusers": WorkflowStateUserModel,
    "workflowtransitions": WorkflowTransitionModel,
    "authorizationgroups": AuthorizationGroupModel,
    "authorizations": AuthorizationModel,
    "authorizationroletypes": AuthorizationRoleTypeModel,
    "authorizationusers": AuthorizationUserModel
}

async def createLoaders(asyncSessionMaker, models=dbmodels):
    def createLambda(loaderName, DBModel):
        return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
    attrs = {}
    for key, DBModel in models.items():
        attrs[key] = property(cache(createLambda(key, DBModel)))
    
    Loaders = type('Loaders', (), attrs)   
    return Loaders()

from functools import cache