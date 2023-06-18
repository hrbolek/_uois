// import { EventQuery } from "@uoisfrontend/shared/src/Queries/EventQuery"
import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const FacilityQueryJSON = (id) => ({
    query: `query($id: ID!) {
        result: facilityById(id: $id) {
            __typename
            id
            name
            lastchange
            geometry
            geolocation
            group {
                id
            }
            type {
              id
              name
            }
            masterFacility {
                __typename
              id
              name
            }
            subFacilities {
                __typename
              id
              name
            }
          }
      }
      `,

    "variables": {id: id}
})

export const FacilityQuery = (id) => 
    authorizedFetch('/gql', {
        body: JSON.stringify(FacilityQueryJSON(id)),
    })

export const FacilityFetchAsyncAction = (id) => (dispatch, getState) => {
    return (
        FacilityQuery(id)
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
