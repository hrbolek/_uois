import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const EventUpdateQueryJSON = (event) => ({
    query: `mutation(
        $id: ID!
        $lastchange: DateTime!
        $name: String
        $startdate: DateTime
        $enddate: DateTime
        $eventtype_id: ID
      ) {
      result: eventUpdate(event: {
        id: $id
        name: $name
        startdate: $startdate
        enddate: $enddate
        lastchange: $lastchange
        eventtypeId: $eventtype_id
        
      }) {
          id
          msg
          event {
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
          }
        }
      }`,
    variables: {...event, masterevent_id: event.masterevent_id, eventtype_id: event.eventtype_id}
})

export const EventUpdateQuery = (event) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(EventUpdateQueryJSON(event)),
    })

export const EventUpdateAsyncAction = (event) => (dispatch, getState) => {
    return (
        EventUpdateQuery(event)
        .then(response => response.json())
        .then(
            json => {
                const msg = json?.data?.result?.msg
                if (msg === "ok") {
                    const event = json?.data?.result?.event
                    const action = All.ItemSliceActions.item_update(event)
                    dispatch(action)
                }
                return json
            }
        )
    )
}
