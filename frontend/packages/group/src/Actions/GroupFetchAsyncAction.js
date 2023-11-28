import { authorizedFetch } from "@uoisfrontend/shared"
import { authorizedFetch2 } from "@uoisfrontend/shared/src/Queries/authorizedFetch"
import { ItemActions } from "@uoisfrontend/shared/src/Store"
import { useLoaderData } from "react-router-dom"

export const GroupQueryJSON = (id) => ({
    query: `query($id: UUID!) {
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
              nameEn
          }
          subgroups {
            __typename
            id
            name
            valid
            grouptype {
              id
              name
              nameEn
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
    authorizedFetch2('/gql', {
        body: JSON.stringify(GroupQueryJSON(id)),
        signal
    })


export const GroupFetchAsyncAction = ({id}, signal) => async (dispatch, getState) => {
    // console.log("GroupFetchAsyncAction: " + JSON.stringify(id))
    if (!id) {
        throw Error("check call, must be object {id}")
    }
    // const state = getState()
    // console.log("GroupFetchAsyncAction.state: " + JSON.stringify(state))
    const jsonData = await GroupQuery(id, signal)
    const result = jsonData?.data?.result
    // console.log("GroupFetchAsyncAction.result: " + JSON.stringify(result))
    if (result) {
        const action = ItemActions.item_update(result)
        // console.log("GroupFetchAsyncAction.action: " + JSON.stringify(action))
        dispatch(action)

        const mastergroup = result?.mastergroup
        if (mastergroup) {
            // console.log("GroupFetchAsyncAction.master in process: " + JSON.stringify(mastergroup))
            dispatch(GroupFetchAsyncAction(mastergroup))
        }
    } 
    return jsonData
}
