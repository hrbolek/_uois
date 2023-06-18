import { GroupQuery } from "@uoisfrontend/shared/src/Queries/GroupQuery"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const GroupFetchAsyncAction = ({id}, signal) => (dispatch, getState) => {
    if (!id) {
        throw Error("check call, must be object {id}")
    }
    
    return (
        GroupQuery(id, signal)
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
