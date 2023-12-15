import { authorizedFetch } from "queries/authorizedFetch"

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