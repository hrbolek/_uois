import { UserAddMembershipQuery } from "queries/UG/UserAddMembershipQuery"
import { UserQuery } from "../queries/UG/UserQuery"
import { ItemActions } from "./keyedreducers"
import { UserUpdateQuery } from "queries/UG/UserUpdateQuery"
import { MembershipUpdateQuery } from "queries/UG/MembershipUpdateQuery"

export const UserRoleAddAsyncAction = (user, membership) => (dispatch, getState) => {
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
