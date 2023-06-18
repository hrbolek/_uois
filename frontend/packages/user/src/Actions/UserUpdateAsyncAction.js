import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

// import { authorizedFetch } from "queries/authorizedFetch"

export const UserUpdateQueryJSON = (user) => ({
    "query": 
        `mutation($id: ID!, $lastchange: DateTime!,
            $name: String!, $surname: String!, $email: String!
          ) {
            result: userUpdate(user: {id: $id lastchange: $lastchange 
              name: $name surname: $surname email: $email}) {
              id
              msg
              user {
                id
                lastchange
                name
                surname
                valid
                email
              }
            }
          }
        `,
    "variables": {...user}
})

export const UserUpdateQuery = (user) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(UserUpdateQueryJSON(user)),
    })

export const UserUpdateAsyncAction = (user) => (dispatch, getState) => {
    console.log("UserUpdateAsyncAction")
    return (
        UserUpdateQuery(user)
        .then(response => response.json())
        .then(json => {
            const msg = json?.data?.result.msg
            if (msg === "ok") {
                const newUser = json?.data?.result.user
                dispatch(All.ItemSliceActions.item_update(newUser))
            }
            return json
        })
    )
}