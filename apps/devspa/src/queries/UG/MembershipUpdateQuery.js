import { authorizedFetch } from "queries/authorizedFetch"

export const MembershipUpdateQueryJSON = (membership) => ({
    "query": 
        `mutation($id: ID!, $lastchange: DateTime!
          $valid: Boolean
          $startdate: DateTime
          $enddate: DateTime
        ){
          result: membershipUpdate(membership: {
            id: $id
            lastchange: $lastchange
            valid: $valid
            startdate: $startdate
            enddate: $enddate
          }) {
            id
            msg
            membership {
              id
              lastchange
            }
          }
        }
        `,
    "variables": {...membership}
})

export const MembershipUpdateQuery = (membership) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(MembershipUpdateQueryJSON(membership)),
    })