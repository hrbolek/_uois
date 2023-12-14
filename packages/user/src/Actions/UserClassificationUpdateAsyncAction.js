import { ItemActions } from "@uoisfrontend/shared"
import { authorizedFetch2 } from "@uoisfrontend/shared/src/Queries/authorizedFetch"

const UserClassificationQueryJSON = (id) => ({
    query: `
    query ($id: ID!) {
        result: userById(id: $id) {
            id
            classifications {
                id
                lastchange
                semester { id}
                level{id name}
                order
                date
            }
        }
      }
    `,
    variables: {id}
})

const UserClassificationMutationQueryJSON = ({id, lastchange, level_id}) => ({
    query: `
    mutation($id: ID! $lastchange: DateTime! $level_id: ID!) {
        result: classificationUpdate(classification: {
          id: $id,
          lastchange: $lastchange,
          classificationlevelId: $level_id
        }) {
          id
          msg
          classification {
            user {
              id
              name
              surname
              email
              classifications {
                id
                lastchange
                order
                semester { id }
                level { id name }
                date
              }
            }
          }
        }
      }
    `,
    variables: {id, level_id, lastchange}
})

const UserClassificationQuery = (id) => 
    authorizedFetch2('/gql', {
        body: JSON.stringify(UserClassificationQueryJSON(id))
    })

const UserClassificationMutationQuery = ({id, lastchange, level_id}) => 
    authorizedFetch2('/gql', {
        body: JSON.stringify(UserClassificationMutationQueryJSON({id, lastchange, level_id}))
    })

// export const UserClassificationFetchAsyncAction = (id) => (dispatch, getState) => {
//     UserClassificationQuery(id)
//     .then(json => {
//         const result = json?.data?.result
//         if (result) {
//             const action = ItemActions.item_update(result)
//             dispatch(action)
//         }
//     })
// }

export const UserClassificationUpdateAsyncAction = ({id, lastchange, level_id}) => (dispatch, getState) => {
    UserClassificationMutationQuery({id, lastchange, level_id})
    .then(json => {
        const result = json?.data?.result
        if (result) {
            const user = result.classification.user
            const action = ItemActions.item_update(user)
            dispatch(action)
        }
    })

}