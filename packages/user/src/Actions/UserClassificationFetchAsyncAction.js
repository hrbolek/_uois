import { authorizedFetch } from "@uoisfrontend/shared"
import { ItemActions } from "@uoisfrontend/shared/src/Store"

export const UserClassificationQueryJSON = (id) => ({
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

export const UserClassificationQuery = (id) => 
    authorizedFetch('/gql', {
        body: JSON.stringify(UserClassificationQueryJSON(id))
    })

export const UserClassificationFetchAsyncAction = ({id}) => (dispatch, getState) => {
    UserClassificationQuery(id)
    .then(response => response.json())
    .then(json => {
        const result = json?.data?.result
        if (result) {
            const action = ItemActions.item_update(result)
            dispatch(action)
        }
    })

}