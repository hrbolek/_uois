//import { authorizedFetch } from "../authorizedFetch"
import { authorizedFetch } from "@uoisfrontend/shared/src/Queries/authorizedFetch";

export const UserEventsQueryJSON = (id, startdate, enddate) => ({
    "query":
        `query($id: ID!, $startdate: DateTime!, $enddate: DateTime! ) {
            result: userById(id: $id) {
              __typename
              id lastchange name surname email
              events(startdate: $startdate, enddate: $enddate) {
                __typename
                id
                lastchange
                name
                startdate
                enddate
              }
            }
          }`,
    "variables": {"id": id, startdate, enddate}
})

export const UserEventsQuery = (id, startdate, enddate) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(UserEventsQueryJSON(id, startdate, enddate)),
    })
