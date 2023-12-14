import { authorizedFetch } from "./authorizedFetch"
import { CreateFetchQuery } from "./creators"

export const EventQueryJSON = (event) => ({
    query: `query($id: ID!) {
        result: eventById(id: $id) {
          __typename
          id
          lastchange
          name
          startdate
          enddate
          eventType{
            id
            name
          }
          masterEvent {
            __typename
            id
            name
            startdate
            enddate
            eventType {
              id
              name
            }
          }
          presences {
            id
            presenceType {
              id
              name
            }
            invitationType {
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
          groups {
            __typename
            id
            name
          }
        }
      }`,
    variables: event
})

export const EventQuery = CreateFetchQuery(EventQueryJSON)
export const EventQuery_ = (id) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(EventQueryJSON(id)),
    })