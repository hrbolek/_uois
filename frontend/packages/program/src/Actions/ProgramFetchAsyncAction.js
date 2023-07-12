import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const ProgramQueryJSON = (id) => ({
  query: `query($id: ID!) {
      result: programById(id: $id) {
        __typename
        id
        name
        lastchange
        type {
          id
          name
          level { id name }
          form { id name }
          language { id name }
          title { id name }
        }
        subjects {
          __typename
          id
          lastchange
          name
          semesters {
            id
            order
          }          
        }
      }
    }
    `,
  variables: {id: id}
})

export const ProgramQuery = (id) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(ProgramQueryJSON(id)),
    })

export const ProgramFetchAsyncAction = ({id}) => (dispatch, getState) => {
    return (
        ProgramQuery(id)
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
