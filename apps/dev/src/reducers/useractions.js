import { UserAddMembershipQuery } from "queries/UG/UserAddMembershipQuery"
import { UserQuery } from "../queries/UG/UserQuery"
import { ItemActions } from "./keyedreducers"
import { UserUpdateQuery } from "queries/UG/UserUpdateQuery"
import { MembershipUpdateQuery } from "queries/UG/MembershipUpdateQuery"
import { RoleInsertQuery } from "queries/UG/RoleQuery"
import { UserEventsQuery } from "queries/UG/UserEventsQuery"

export const UserFetchAsyncAction = (id) => (dispatch, getState) => {
    return (
        UserQuery(id)
        .then(response => response.json())
        .then(json => {
            const user = json?.data?.result
            if (user) {
                dispatch(ItemActions.item_update(user))
            }
            return json
        })
    )
}

export const UserAddMembershipAsyncAction = (user, group) => (dispatch, getState) => {
    return (
        UserAddMembershipQuery({user, group})
        .then(response => response.json())
        .then(json => {
            const msg = json?.data?.result.msg
            if (msg === "ok") {
                dispatch(UserFetchAsyncAction(user.id))
            }
            return json
        })
    )
}

export const UserUpdateAsyncAction = (user) => (dispatch, getState) => {
    return (
        UserUpdateQuery(user)
        .then(response => response.json())
        .then(json => {
            const msg = json?.data?.result.msg
            if (msg === "ok") {
                dispatch(UserFetchAsyncAction(user.id))
            }
            return json
        })
    )
}

export const UserMembershipUpdateAsyncAction = (user, membership) => (dispatch, getState) => {
    return (
        MembershipUpdateQuery(membership)
        .then(response => response.json())
        .then(json => {
            const msg = json?.data?.result.msg
            if (msg === "ok") {
                dispatch(UserFetchAsyncAction(user.id))
            }
            return json
        })
    )
}

export const UserRoleAddAsyncAction = (user, group, roletype) => (dispatch, getState) => {
    // const insertRecord = {user_id: user.id, group_id: group.id, roletype_id: roletype.id}
    // console.log("UserRoleAddAsyncAction", insertRecord)
    return (
        RoleInsertQuery({user_id: user.id, group_id: group.id, roletype_id: roletype.id})
        .then(response => response.json())
        .then(json => {
            const msg = json?.data?.result.msg
            if (msg === "ok") {
                dispatch(UserFetchAsyncAction(user.id))
            }
            return json
        })
    )
}

export const UserEventsFetchAsync = (id, startdate, enddate) => (dispatch, getState) => {
    console.log("UserEventsFetchAsync", id, startdate, enddate)
    let _startdate = startdate
    if (!_startdate) {
        _startdate = new Date()
    } 
    let _enddate = enddate
    if (!_enddate) {
        //
    }
    return (
        UserEventsQuery(id, startdate, enddate)
        .then(response => response.json())
        .then(json => {
            const events = json?.data?.result.events
            console.log("UserEventsFetchAsync", json)
            if (events) {
                dispatch(ItemActions.item_update_events({id: id, events: events}))
            }
            return json
        })
    )
}