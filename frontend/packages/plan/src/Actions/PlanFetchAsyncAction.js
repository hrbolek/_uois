import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const PlanQueryJSON = (id) => ({
    query: `query($id: ID!) {
        result: planById(id: $id) {
          __typename
          id
          lastchange
          semester {
              __typename
              id
              order
              subject {
                id
                name
              }
          }
          lessons {
            __typename
            id
            name
            lastchange
            length
            order
            type {
              id
              name
            }
            users {
              __typename
              id
              name
              surname
              email
            }
            groups {
              __typename
              id
              name
            }
            facilities {
              __typename
              id
              name
              label
            }
          }
        }
      }
      `,
    variables: {id: "a5085468-394f-4a8b-bf23-4e72a6a6d415"}
})

export const PlanQuery = (id) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(PlanQueryJSON(id)),
    })

export const PlanFetchAsyncAction = ({id}) => (dispatch, getState) => {
    return (
        PlanQuery(id)
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
