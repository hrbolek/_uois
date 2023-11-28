import { ItemActions } from "@uoisfrontend/shared/src/Store"


import { authorizedFetch } from "@uoisfrontend/shared"
import { authorizedFetch2 } from "@uoisfrontend/shared/src/Queries/authorizedFetch"

const GroupMembersQueryJSON = (id) => ({
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
          memberships {
            id
            lastchange
            valid
            startdate
            enddate
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

const GroupMembersQuery = (id) =>
    authorizedFetch2('/gql', {
        body: JSON.stringify(GroupMembersQueryJSON(id)),
    })

export const GroupMembersFetchAsyncAction = ({id}) => (dispatch, getState) => {
    return (
        GroupMembersQuery(id)
        .then(
            json => {
                const result = json?.data?.result
                if (result) {
                    const action = ItemActions.item_update(result)
                    dispatch(action)
                    return result
                }
                return json
            }
        )
    )
}
