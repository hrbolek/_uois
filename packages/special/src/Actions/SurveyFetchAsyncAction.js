import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const SurveyQueryJSON = (id) => ({
    query: `query($id: ID!) {
        result: surveyById(id: $id) {
            __typename
          id
          name
          lastchange
          questions {
            id
            name
            order
            answers {
              id
              value
              aswered
              expired
              user {
                id
                email
              }
            }
          }
        }
      }
      `,
    variables: {id: id}
})

export const SurveyQuery = (id) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(SurveyQueryJSON(id)),
    })

export const SurveyFetchAsyncAction = (id) => (dispatch, getState) => {
    return (
        SurveyQuery(id)
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
