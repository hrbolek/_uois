import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const SubjectQueryJSON = (id) => ({
    query: `query($id: ID!) {
        result: acsubjectById(id: $id) {
          __typename
          id lastchange
          name
          program {
            __typename
            id lastchange
            name
          }
          semesters {
            __typename
            id lastchange
            order
            classificationType { id name }
            credits
            topics {
              id lastchange
              name
              order
              lessons {
                id lastchange
                type { id name }
              }
            }
          }
        }
      }
      `,
    variables: {id: "ce250a68-b095-11ed-9bd8-0242ac110002"}
})

export const SubjectQuery = (id) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(SubjectQueryJSON(id)),
    })

export const SubjectFetchAsyncAction = (id) => (dispatch, getState) => {
    return (
        SubjectQuery(id)
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
