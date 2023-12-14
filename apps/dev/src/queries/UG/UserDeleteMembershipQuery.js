import { authorizedFetch } from "queries/authorizedFetch"

export const UserAddMembershipQueryJSON = ({user, group}) => ({
    "query": 
        `mutation($user_id: ID!, $group_id: ID!)
        {
          result: membershipInsert(membership: {userId: $user_id, groupId:$ group_id}) {
            id
            msg
             membership{
              id
              lastchange
              valid
            }
          }
        }
        `,
    "variables": {user_id: user.id, group_id: group.id}
})

export const UserAddMembershipQuery = ({user, group}) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(UserAddMembershipQueryJSON({user, group})),
    })