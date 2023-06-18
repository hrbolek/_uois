import { GroupMembersQuery } from "../Queries/GroupMembersQuery"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const GroupMembersFetchAsyncAction = ({id}) => (dispatch, getState) => {
    return (
        GroupMembersQuery(id)
        .then(response => response.json())
        .then(
            json => {
                const result = json?.data?.result
                if (result) {
                    const action = All.ItemSliceActions.item_update(result)
                    dispatch(action)
                }
                return json
            }
        )
    )
}
