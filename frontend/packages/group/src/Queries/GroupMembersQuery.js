import { authorizedFetch } from "@uoisfrontend/shared"

export const GroupMembersQueryJSON = (id) => ({
    query: `query($id: ID!) {
        result: groupById(id: $id) {
          __typename
          id
          lastchange
          name
          mastergroup {
            __typename
            id
            name
            grouptype {
              id
              name
            }
          }
          grouptype {
              id
              name
          }
          subgroups {
            __typename
            id
            name
            valid
            grouptype {
              id
              name
            }
          }
          roles {
            id
            lastchange
            valid
            startdate
            enddate
            
            roletype {
              id
              name
            }
            user {
              __typename
              id
              name
              surname
              email
            }
          }
          memberships {
            id
            lastchange
            valid
            startdate
            enddate
            user {
              __typename
              id
              name
              surname
              email
            }
          }                
        }
      }`,
    variables: {id: id}
})

export const GroupMembersQuery = (id) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(GroupMembersQueryJSON(id)),
    })