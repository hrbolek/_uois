import All from "@uoisfrontend/shared/src/keyedreducers"
import { DeleteButton, authorizedFetch } from "@uoisfrontend/shared"
import { CheckSquare, PlusLg, TrashFill } from "react-bootstrap-icons"
import { useDispatch } from "react-redux"

export const GroupRoleUpdateQueryJSON = (role) => ({
    query: `mutation(
            $id: ID!
            $lastchange: DateTime!
            $startdate: DateTime
            $enddate: DateTime
            $valid: Boolean
        ) {
        result: roleUpdate(role: {
          id: $id
          lastchange: $lastchange
          startdate: $startdate
          enddate: $enddate
          valid: $valid
        }){
          id
          msg
          role {
            id
            group {
              id
              roles {
                id
                valid
                lastchange
                startdate
                enddate
                roletype {id name }
                user {
                  id
                  name
                  surname
                  email
                }
              }
            }
          }
        }
      }`,
    variables: {...role}
})

export const GroupRoleUpdateQuery = (role) => 
    authorizedFetch('/gql', {
        body: JSON.stringify(GroupRoleUpdateQueryJSON(role))
    })

export const GroupRoleUpdateAsyncAction = ({group, role}) => (dispatch, getState) => {
    // console.log("GroupRoleUpdateAsyncAction", membership)
    return (
        GroupRoleUpdateQuery(role)
        .then(response => response.json())
        .then(json=> {
            const result = json?.data?.result
            if (result) {
                const group = result.role.group
                // console.log("GroupRoleUpdateAsyncAction.query", group)
                const action = All.ItemSliceActions.item_update(group)
                dispatch(action)
            }
            return json
        })
    )
}

export const GroupRoleValidButton = ({group, role}) => {
    const dispatch = useDispatch()
    const onChange = (value) => {
        const newRole = {
            ...role,
            valid: !role.valid
        }
        dispatch(GroupRoleUpdateAsyncAction({group, role: newRole}))
        .then(
            json => json
        )
    }
    if (role?.valid) {
        return (
            <DeleteButton onClick={onChange}><TrashFill /></DeleteButton>
        )    
    } else {
        return (
            <DeleteButton onClick={onChange}><PlusLg /></DeleteButton>
        )
    }
}

