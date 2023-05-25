import { configureStore } from "@reduxjs/toolkit"
import { ItemActions, ItemReducer } from "./keyedreducers"
import { UserAddMembershipAsyncAction, UserEventsFetchAsync, UserFetchAsyncAction, UserMembershipUpdateAsyncAction, UserRoleAddAsyncAction, UserUpdateAsyncAction } from "./useractions"
import { MsgActions, MsgAddAsyncAction, MsgFlashAsyncAction, MsgReducer } from "./msgsreducers"
import { MembershipUpdateQuery } from "queries/UG/MembershipUpdateQuery"


/**
 * Toto je hlavni store pro celou aplikaci. Zde zacleneno pro demonstraci. 
 */
export const store = configureStore(
    { 
        reducer: {
            items: ItemReducer,
            msgs: MsgReducer
        }, 
        preloadedState: {
            items: {}
        }
})
console.log("store configured")
console.log(JSON.stringify(store.getState()))
const dispatch = store.dispatch

export const bindGroupActions = (dispatch) => ({
    onDispatch: dispatch,

    onMsgRemove: (msg) => dispatch(MsgActions.msg_delete(msg)),
    onMsgFlashAsync: (msg) => dispatch(MsgFlashAsyncAction(msg)),
    onMsgAddAsync: (msg) => dispatch(MsgAddAsyncAction(msg)),

    onUserUpdate: (user) => dispatch(ItemActions.item_update(user)),
    onUserUpdateAsync: (user) => dispatch(UserUpdateAsyncAction(user)),
    onUserFetchAsync: (id) => dispatch(UserFetchAsyncAction(id)),
    onUserMembershipAdd: (user, group) => dispatch(UserAddMembershipAsyncAction(user, group)),
    onUserRoleAddAsync: (user, group, role) => dispatch(UserRoleAddAsyncAction(user, group, role)),
    onUserEventsFetchAsync: (user, startdate, enddate) => dispatch(UserEventsFetchAsync(user, startdate, enddate)),

    onUserMembershipUpdateAsyncAction: (user, membership) => dispatch(UserMembershipUpdateAsyncAction(user, membership))
    // onUserMembershipUpdateAsyncAction: (membership) => dispatch(UserMembershipUpdateAsyncAction(membership))
})



/**
 * Vsechny akce / callbacky pro celou aplikaci
 * Lze je kdekoliv importovat a vyuzit. 
 * Je ovsem zadouci, aby se tyto dostaly ke "spodnim" komponentam pres props.
 * Tim se zabezpeci jejich "purity" (nejsou zavisle na globalnich parametrech)
 */
export const actions = {
    ...bindGroupActions(dispatch)
}