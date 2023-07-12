import All from "@uoisfrontend/shared/src/keyedreducers"
import { DeleteButton, authorizedFetch } from "@uoisfrontend/shared"
import { CheckSquare, PlusLg, TrashFill } from "react-bootstrap-icons"
import { useDispatch } from "react-redux"
import { UserSearch } from "@uoisfrontend/user"


export const GroupMembershipUpdateQueryJSON = (membership) => ({
    query: `mutation(
            $id: ID!
            $lastchange: DateTime!
            $startdate: DateTime
            $enddate: DateTime
            $valid: Boolean
        ) {
        result: membershipUpdate(membership: {
          id: $id
          lastchange: $lastchange
          startdate: $startdate
          enddate: $enddate
          valid: $valid
        }){
          id
          msg
          membership {
            id
            group {
              id
              memberships {
                id
                valid
                lastchange
                startdate
                enddate
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
    variables: {...membership}
})

export const GroupMembershipInsertQueryJSON = (user, group) => ({
    query: `mutation(
        $startdate: DateTime
        $valid: Boolean
        $user_id: ID!
        $group_id: ID!
    ) {
        result: membershipInsert(membership: {
          startdate: $startdate
          valid: $valid
          userId: $user_id
          groupId: $group_id
          
        }){
          id
          msg
          membership {
            id
            group {
              id
              memberships {
                id
                valid
                startdate
                enddate
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
    variables: {
        startdate: new Date().toISOString().replace('Z', ''),
        valid: true,
        user_id: user.id,
        group_id: group.id
    }
})

export const GroupMembershipUpdateQuery = (membership) => 
    authorizedFetch('/gql', {
        body: JSON.stringify(GroupMembershipUpdateQueryJSON(membership))
    })

export const GroupMembershipInsertQuery = (user, group) => 
    authorizedFetch('/gql', {
        body: JSON.stringify(GroupMembershipInsertQueryJSON(user, group))
    })

export const GroupMembershipUpdateAsyncAction = ({group, membership}) => (dispatch, getState) => {
    // console.log("GroupMembershipUpdateAsyncAction", membership)
    return (
        GroupMembershipUpdateQuery(membership)
        .then(response => response.json())
        .then(json=> {
            const result = json?.data?.result
            if (result) {
                const group = result.membership.group
                // console.log("GroupMembershipUpdateAsyncAction.query", group)
                const action = All.ItemSliceActions.item_update(group)
                dispatch(action)
            }
            return json
        })
    )
}

export const GroupMembershipInsertAsyncAction = ({group, user}) => (dispatch, getState) => {
    return (
        GroupMembershipInsertQuery(user, group)
        .then(response => response.json())
        .then(json=> {
            const result = json?.data?.result
            if (result) {
                const group = result?.membership?.group
                if (group) {
                    const action = All.ItemSliceActions.item_update(group)
                    dispatch(action)
                } else {

                }
                
            }
            return json
        })
    )
}

export const GroupMemberRemoveButton = ({group, user}) => {
    const dispatch = useDispatch()
    const membership = group.membership.find(
        m => (m.user.id === user.id) & (m.valid)
    )
    const onRemove = () => {
        const newMembership = {
            ...membership,
            valid: false,
            enddate: new Date().toISOString().replace('Z', '')
        }
        dispatch(GroupMembershipUpdateAsyncAction({group, membership: newMembership}))
        .then(
            json => json
        )
    }
    if (membership) {
        return (
            <DeleteButton onClick={onRemove}><TrashFill /></DeleteButton>
        )    
    } else {
        return (null)
    }
}

export const GroupMemberAddButton = ({group, user}) => {
    const dispatch = useDispatch()
    const membership = group.membership.find(
        m => (m.user.id === user.id) & (m.valid)
    )
    const onAdd = () => {
        dispatch(GroupMembershipInsertAsyncAction({group, user}))
        .then(
            json => json
        )
    }
    if (membership) {
        return (null)    
    } else {
        return (
            <DeleteButton onClick={onAdd}><PlusLg /></DeleteButton>
        )
    }
}

export const GroupMemberAddWithSearch = ({group}) => {
    const dispatch = useDispatch()
    const onSelect = (user) => {
        dispatch(GroupMembershipInsertAsyncAction({group, user}))
        .then(
            json => json
        )

    }
    return (
        <UserSearch label="Přidat člena" onSelect={onSelect} />
    )
}


export const GroupMemberAddRemoveButton = ({group, user}) => {
    return(
        <>
            <GroupMemberAddButton group={group} user={user} />
            <GroupMemberRemoveButton group={group} user={user} />
        </>
    )
}