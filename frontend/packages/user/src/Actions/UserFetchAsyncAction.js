import { authorizedFetch2 } from "@uoisfrontend/shared/src/Queries/authorizedFetch"
import { ItemActions } from "@uoisfrontend/shared/src/Store"

const UserQueryJSON = (id) => ({
    "query":
        `query($id: UUID!) {
            result: userById(id: $id) {
              __typename
              id lastchange name surname email
              membership {
                id lastchange valid startdate enddate
                group {
                  id name
                }
              }
              roles {
                id lastchange valid startdate enddate
                roletype {
                  id name nameEn
                }
                group {
                  id name
                }
              }
            }
          }`,
    "variables": {"id": id}
})

const UserQuery = (id) =>
    authorizedFetch2('/gql', {
        body: JSON.stringify(UserQueryJSON(id)),
    })

export const UserFetchAsyncAction = ({id}) => (dispatch, getState) => {
    return UserQuery(id)
    .then(
        json => {
            const result = json?.data?.result
            console.log("UserFetchAsyncAction.result", JSON.stringify(json))
            if (result) {
                console.log("UserFetchAsyncAction.result", JSON.stringify(result))
                const action = ItemActions.item_update(result)
                dispatch(action)
            }
            return json
        }
    )
}