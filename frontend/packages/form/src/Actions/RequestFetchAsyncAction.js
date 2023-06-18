// import { EventQuery } from "@uoisfrontend/shared/src/Queries/EventQuery"
import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const RequestQueryJSON = (id) => ({
    query: `query($id: ID!) {
        result: requestById(id: $id) {
                __typename
                id
                name
                lastchange
                histories {
                id
                name
                form {
                    id
                    
                }
                              
              }
            }
          }
      `,

    "variables": {id: id}
})

export const RequestQuery = (id) => 
    authorizedFetch('/gql', {
        body: JSON.stringify(RequestQueryJSON(id)),
    })

export const RequestFetchAsyncAction = ({id}) => (dispatch, getState) => {
    return (
        RequestQuery(id)
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
