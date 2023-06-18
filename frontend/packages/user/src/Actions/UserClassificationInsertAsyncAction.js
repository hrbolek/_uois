import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers";

export const UserClassificationInsertQueryJSON = ({ user_id, semester_id, classification_level_id, order }) => ({
    query: `
    mutation(
        $user_id: ID!
        $semester_id: ID!
        $classification_level_id: ID!
        $order: Int!
      ) {
        result: classificationInsert(
          classification: {
            userId: $user_id
            semesterId: $semester_id
            classificationlevelId: $classification_level_id
            order: $order
          }) {
          id
          msg
          classification {
            user {
              __typename
              id
              classifications {
                id
                lastchange
                order
                semester { id }
                level { id name }
              }
            }
          }
        }
      }
    `,
    variables: {
        user_id,
        semester_id,
        classification_level_id,
        order
    }
})

export const UserClassificationInsertQuery = ({ user_id, semester_id, classification_level_id, order }) => 
    authorizedFetch("/gql", {
        body: JSON.stringify(UserClassificationInsertQueryJSON({ user_id, semester_id, classification_level_id, order }))
    })

export const UserClassificationInsertAsyncAction = ({user_id, semester_id, level_id, order}) => (dispatch, getState) => {
    return (
        UserClassificationInsertQuery({user_id, semester_id, level_id, order})
        .then(response => response.json())
        .then(
            json => {
                const result = json?.data?.result
                if (result) {
                    const user = result.classification.user
                    const action = All.ItemSliceActions.item_update(user)
                    dispatch(action)
                }
                return json
            }
        )
    )
}
