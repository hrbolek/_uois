import All from "@uoisfrontend/shared/src/keyedreducers"
import { authorizedFetch } from "@uoisfrontend/shared"

export const GroupUpdateQueryJSON = ({group}) => ({
    query: `mutation(
        $id: ID!
        $lastchange: DateTime!
        $name: String
        $grouptypeId: ID
        $mastergroupId: ID
        $valid: Boolean
      ) {
        result: groupUpdate(group: {
          id: $id
          lastchange: $lastchange
          name: $name
          grouptypeId: $grouptypeId
          mastergroupId: $mastergroupId
          valid: $valid
        }) {
          id
          msg
          group {
            __typename
            id
            lastchange
            name
            mastergroup { id name }
            grouptype { id name }
          }
        }
      }`,
    variables: {...group, grouptypeId: group?.grouptypeId, mastergroupId: group?.mastergroupId}
})

export const GroupUpdateQuery = ({group}) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(GroupUpdateQueryJSON({group}))
    })

export const GroupUpdateAsyncAction = (group) => (dispatch, getState) => {
    // console.log("GroupUpdateAsyncAction", group)
    return (
        GroupUpdateQuery({group})
        .then(response => response.json())
        .then(
            json => {
                const result = json?.data?.result
                if (result) {
                    const group = result?.group
                    const action = All.ItemSliceActions.item_update(group)
                    dispatch(action)
                }
                return json
            }
        )
    )

}