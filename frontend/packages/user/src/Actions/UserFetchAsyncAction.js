import { UserQuery } from "@uoisfrontend/shared/src/Queries"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const UserFetchAsyncAction = ({id}) => (dispatch, getState) => {
    return UserQuery(id)
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
}