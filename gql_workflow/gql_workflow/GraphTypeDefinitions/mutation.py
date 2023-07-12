import strawberry

@strawberry.type
class Mutation:
    from .authorizationGQLModel import authorization_insert
    authorization_insert = authorization_insert

    from .authorizationGroupGQLModel import authorization_add_group
    authorization_add_group = authorization_add_group

    from .authorizationGroupGQLModel import authorization_remove_group
    authorization_remove_group = authorization_remove_group

    from .authorizationRoleTypeGQLModel import authorization_add_role
    authorization_add_role = authorization_add_role

    from .authorizationRoleTypeGQLModel import authorization_remove_role
    authorization_remove_role = authorization_remove_role

    from .authorizationUserGQLModel import authorization_add_user
    authorization_add_user = authorization_add_user

    from .authorizationUserGQLModel import authorization_remove_user
    authorization_remove_user = authorization_remove_user

    from .workflowGQLModel import workflow_insert
    workflow_insert = workflow_insert

    from .workflowGQLModel import workflow_update
    workflow_update = workflow_update

    from .workflowStateGQLModel import workflow_state_insert
    workflow_state_insert = workflow_state_insert

    from .workflowStateGQLModel import workflow_state_update
    workflow_state_update = workflow_state_update

    # from .WorkflowStateRoleTypeGQLModel import *

    from .workflowTransitionGQLModel import workflow_transition_insert
    workflow_transition_insert = workflow_transition_insert

    from .workflowTransitionGQLModel import workflow_transition_update
    workflow_transition_update = workflow_transition_update

    # from .WorkflowStateUserGQLModel import *
    from .workflowStateUserGQLModel import workflow_state_add_user
    workflow_state_add_user = workflow_state_add_user

    from .workflowStateUserGQLModel import workflow_state_remove_user
    workflow_state_remove_user = workflow_state_remove_user

    from .workflowStateRoleTypeGQLModel import workflow_state_add_role    
    workflow_state_add_role = workflow_state_add_role

    from .workflowStateRoleTypeGQLModel import workflow_state_remove_role
    workflow_state_remove_role = workflow_state_remove_role