import { useDispatch } from "react-redux"
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import Card from "react-bootstrap/Card"

import { GroupMembershipInsertAsyncAction } from "./GroupMemberRemoveButton"
import { UserSearch } from "@uoisfrontend/user"
import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"
import { RoleTypeSelect } from "./RoleTypeSelect"
import { useState } from "react"


export const GroupRoleInsertQueryJSON = (role) => ({
    query: `mutation(
            $user_id: ID!
            $group_id: ID!
            $roletype_id: ID!
            $startdate: DateTime
            $valid: Boolean
        ) {
            result: roleInsert(role: {
                userId: $user_id
                groupId: $group_id
                roletypeId: $roletype_id
                valid: $valid
                startdate: $startdate
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
                roletype{ id name }
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
        ...role,
    }
})

export const GroupRoleInsertQuery = (role) => 
    authorizedFetch('/gql', {
        body: JSON.stringify(GroupRoleInsertQueryJSON(role))
    })

export const GroupRoleInsertAsyncAction = ({group, role}) => (dispatch, getState) => {
    // console.log("GroupRoleInsertAsyncAction", membership)
    return (
        GroupRoleInsertQuery(role)
        .then(response => response.json())
        .then(json=> {
            const result = json?.data?.result
            if (result) {
                const group = result.role.group
                // console.log("GroupRoleInsertAsyncAction.query", group)
                const action = All.ItemSliceActions.item_update(group)
                dispatch(action)
            }
            return json
        })
    )
}

export const GroupRoleAddWithSearch = ({group}) => {
    const dispatch = useDispatch()
    const onSelect = (user) => {
        const role = {user_id: user.id, group_id: group.id, roletype_id: roletype}
        dispatch(GroupRoleInsertAsyncAction({group, role}))
        .then(
            json => json
        )

    }
    const [roletype, setRoletype] = useState(null)

    const onRoleSelect = (role) => {
        setRoletype(role)
    }
    return (
        <Card>
            <Card.Body>
                <Row>
                    <Col>
                        {/* <b>Typ role</b> */}
                        <RoleTypeSelect label={"Typ role"} onSelect={onRoleSelect}/>
                    </Col>
                    
                    <Col>
                        {/* <b>Uživatel</b> */}
                        <UserSearch label={"Jméno uživatele"} onSelect={onSelect} />
                    </Col>           
                </Row>

            </Card.Body>
        </Card>
        
    )
}