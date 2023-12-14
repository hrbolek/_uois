import Form from "components/Form";
import { Plus, TrashFill } from "react-bootstrap-icons";
import Table from "react-bootstrap/Table";
import { RoleTypeSelectFetch } from "./RoleTypeSelect";
import { UGSearchSmall } from "./UGSearch";
import { useMemo, useState } from "react";
import { Col, Row } from "react-bootstrap";

export const UserRolesTableRow = ({index, role, actions}) => {
    return (
        <tr>
            <td>{index}</td>
            <td>{role?.roletype?.name}</td>
            <td>{role?.group?.name}</td>
            <td>{role?.startdate}</td>
            <td>{role?.enddate}</td>
            <td><Form.DeleteButton><TrashFill /></Form.DeleteButton></td>
        </tr>
    )
}

export const UserRolesTableToolsRow = ({user, actions}) => {
    const [currentGroup, setCurrentGroup] = useState({})
    const [roleType, setRoleType] = useState({})
    const selectGroup = (group) => {
        setCurrentGroup(group)
    }
    const onAddRole = () => {
        console.log("onAddRole", currentGroup)
        console.log("onAddRole", roleType)
        if ((currentGroup.id) && (roleType.id)){
            actions.onUserRoleAddAsync(user, currentGroup, roleType)
            .then(
                json => {
                    const msg = json?.data?.result?.msg
                    if (msg === "ok") {
                        actions.onMsgFlashAsync({title: "Role ok", variant: "success"})
                    } else {
                        actions.onMsgAddAsync({title: "Chyba: " + JSON.stringify(json), variant: "danger"})
                    }
                }
            )
        }
    }

    const GroupHintComponent = useMemo( 
        () =>({group}) => {
            return (
                <> <span className="btn btn-sm btn-outline-primary" onClick={()=>selectGroup(group)}>{group.name}</span></>
            )
    })

    return (
        <tr>
            <th colSpan={2}>Přidat roli</th>
            <td>
                <UGSearchSmall groups={true} GroupComponent={GroupHintComponent}/>
            </td>
            <td colSpan={3}>
                <Row>
                    <Col>
                        <div className="input-group mb-3">
                            <span className="btn btn-outline-primary">{currentGroup?.name}</span>
                            <RoleTypeSelectFetch onSelect={setRoleType}/>
                            <span className="btn btn-outline-primary" onClick={onAddRole}><Plus /></span>
                        </div>
                    </Col>
                </Row>              
            
            </td>
        </tr>
    )
}

export const UserRolesTableBody = ({user, actions}) => {
    return (
        <tbody>
            {user?.roles?.map(
                (role, index) => <UserRolesTableRow key={role.id} index={index+1} role={role} actions={actions} />
            )}
            <UserRolesTableToolsRow user={user} actions={actions} />
        </tbody>
    )
}

export const UserRolesTableHeader = ({user, actions}) => {
    return (
        <thead>
            <tr>
                <th className="">#</th>
                <th className="w-25">N</th>
                <th className="w-25">G</th>
                <th className="w-25">počátek</th>
                <th className="w-25">konec</th>
                <th className=""></th>
            </tr>
        </thead>
    )
}

export const UserRolesEditTable = ({user, actions}) => {
    return (
        <Table>
            <UserRolesTableHeader user={user} actions={actions}/>
            <UserRolesTableBody user={user} actions={actions}/>
        </Table>
    )
}