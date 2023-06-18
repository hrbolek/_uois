import { authorizedFetch } from "../authorizedFetch"


export const RoleTypesQueryJSON = () => ({
    "query":
        `query {
          result: roleTypePage(skip:0, limit:100) {
            id
            name
          }
        }`,
    "variables": {}
})

export const RoleTypesQueryQuery = () =>
    authorizedFetch('/gql', {
        body: JSON.stringify(RoleTypesQueryJSON()),
    })



