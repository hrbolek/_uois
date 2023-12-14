import { authorizedFetch } from "./authorizedFetch"

export const GroupQueryJSON = (id) => ({
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
        }
      }`,
    variables: {id: id}
})

export const GroupQuery = (id, signal) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(GroupQueryJSON(id)),
        signal
    })