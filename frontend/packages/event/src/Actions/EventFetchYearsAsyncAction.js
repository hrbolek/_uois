import { authorizedFetch } from "@uoisfrontend/shared"
import { ItemActions } from "@uoisfrontend/shared/src/Store"

export const EventFetchYearsQueryJSON = (id) => ({
    query: `query($id: ID!){
      result: eventTypeById(id: $id) {
        __typename
        id
        name
        events {
          __typename
          id
          name
          startdate
          enddate
          eventType {
            id
            name
          }
          subEvents(startdate: "2000-01-01", enddate: "2040-12-31") {
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
    variables: {id}
})

export const EventFetchYearsQuery = (id) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(EventFetchYearsQueryJSON(id)),
    })

export const EventFetchYearsAsyncAction = (id) => (dispatch, getState) => {
    return (
        EventFetchYearsQuery(id)
        .then(response => response.json())
        .then(
            json => {
                const result = json?.data?.result
                if (result) {
                    const action = ItemActions.item_update(result)
                    dispatch(action)
                    for(let se of result.events) {
                        const action = ItemActions.item_update(se)
                        dispatch(action)
                    }
                }
                return json
            }
        )
    )
}
