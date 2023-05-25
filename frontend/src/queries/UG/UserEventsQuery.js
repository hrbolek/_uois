import { authorizedFetch } from "../authorizedFetch"

export const UserEventsQueryJSON = (id, startdate, enddate) => ({
    "query":
        `query(
          $id: ID!
          $startdate: DateTime!
          $enddate: DateTime!
        ){
          result: userById(id: $id) {
            __typename
            id
            events(startdate: $startdate, enddate: $enddate) {
              id
              lastchange
              name
              startdate
              enddate
              eventType {
                id
                name
              }
            }
          }
        }`,
    "variables": {"id": id, startdate, enddate}
})

export const UserEventsQuery = (id, startdate, enddate) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(UserEventsQueryJSON(id, startdate, enddate)),
    })



