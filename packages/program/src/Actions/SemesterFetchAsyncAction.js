import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const SemesterQueryJSON = (id) => ({
  query: `query($id: ID!) {
      result: acsemesterById(id: $id) {
          id
          order
          credits
          lastchange
          subject {
              id
              name
          }
          classificationType {
              id
              name
              lastchange
          }
          topics {
              id
              name
              lastchange
              order
          }
          plans {
            id
          }
       }
      }
    `,
  variables: {id: id}
})

export const SemesterQuery = (id) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(SemesterQueryJSON(id)),
    })

export const SemesterFetchAsyncAction = ({id}) => (dispatch, getState) => {
    return (
        SemesterQuery(id)
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
