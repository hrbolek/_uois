import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const UserClassificationJSON = (id) => ({
  query: `query($id: ID!) {
      result: userById(id: $id) {
        id
        name
        surname
        email
        classifications {
          id
          lastchange
          level { id name }
          semester {
            id
            order
            subject {
              id
              name
              program {
                id
                name
              }
            }
          }
        }
      }
    }
    `,
  variables: {id}
})

export const UserClassification = (id) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(UserClassificationJSON(id)),
    })

export const UserClassificationFetchAsyncAction = ({id}) => (dispatch, getState) => {
    console.log("UserClassificationFetchAsyncAction", id)
    return (
        UserClassification(id)
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
