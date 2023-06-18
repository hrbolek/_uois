import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const EventQueryJSON = (id) => ({
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
            lastchange
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
    variables: {id: id}
})

export const EventQuery = (id) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(EventQueryJSON(id)),
    })

export const EventFetchAsyncAction = (id) => (dispatch, getState) => {
    return (
        EventQuery(id)
        .then(response => response.json())
        .then(
            json => {
                const result = json?.data?.result
                if (result) {
                    const action = All.ItemSliceActions.item_update(result)
                    dispatch(action)
                }
                return json
            }
        )
    )
}
