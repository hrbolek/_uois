import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const SurveyUserQueryJSON = (id) => ({
    query: `query($id: ID!) {
        result: userById(id: $id) {
          id
          name
          surname
          email
          answers {
            id
            lastchange
            value
            aswered
            expired
            question {
              id
              name
              type { id name }
              values {
                id
                name
                order
              }
              survey { id name }
            }
          }
        }
      }
      `,
    variables: {id: id}
})

export const SurveyUserQuery = (id) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(SurveyUserQueryJSON(id)),
    })

export const SurveyUserFetchAsyncAction = ({id}) => (dispatch, getState) => {
    return (
      SurveyUserQuery(id)
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
