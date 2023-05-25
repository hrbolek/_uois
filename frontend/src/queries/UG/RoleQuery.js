import { authorizedFetch } from "../authorizedFetch"


export const RoleInsertQueryJSON = (role) => ({
    "query":
        `mutation($user_id: ID! $group_id: ID! $roletype_id: ID!) {
          result: roleInsert(role: {
            userId: $user_id
            groupId: $group_id
            roletypeId: $roletype_id
          }) {
            id
            msg
            role {
              id
              lastchange
            }
          }
        }`,
    "variables": {...role}
})

export const RoleInsertQuery = (role) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(RoleInsertQueryJSON(role)),
    })



