// import { EventQuery } from "@uoisfrontend/shared/src/Queries/EventQuery"
import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const FormQueryJSON = (id) => ({
    query: `query($id: ID!) {
        result: formById(id: $id) {
              __typename
              id
              lastchange
              name
              valid
              type {
                id 
                name
              }
              sections {
                id
                name
                lastchange
                order
                parts {
                  id
                  name
                  lastchange
                  order
                  items {
                    id
                    name
                    order
                    lastchange
                    value
                    type {
                      id 
                      name
                    }
                  }
                }
              }
            }
          }
      `,

    "variables": {id: id}
})

export const FormQuery = (id) => 
    authorizedFetch('/gql', {
        body: JSON.stringify(FormQueryJSON(id)),
    })

export const FormFetchAsyncAction = ({id}) => (dispatch, getState) => {
    return (
        FormQuery(id)
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
