import { TrashFill } from "react-bootstrap-icons"
import { DeleteButton, Link } from "@uoisfrontend/shared"
import { GroupRole } from "./GroupRoles"
import Table from "react-bootstrap/Table"
import { GroupRoleValidButton } from "./GroupRoleValidButton"
import { GroupRoleStartPicker } from "./GroupRoleStartPicker"
import { GroupRoleEndPicker } from "./GroupRoleEndPicker"

export const GroupEditRoles_ = ({group}) => {
    const roles = group?.roles || []
    return (
        <>
            {roles.map(
                (role, index) => <GroupRole key={role.id} role={role} group={group}><DeleteButton><TrashFill /></DeleteButton> </GroupRole>
            )}
        </>
    )
}

const UserLink = ({user}) => {
    return (
        <Link id={user.id} tag="user">{user.name} {user.surname}</Link>
    )
}

const GroupEditRolesTableBody = ({group, roles}) => {
    return (
        <tbody>
            {roles.map(
                (role, index) => 
                    <tr key={role.id}>
                        <td>{index+1}</td>
                        <td>{role?.roletype?.name}</td>
                        <td><UserLink user={role.user} /></td>
                        <td>
                            <GroupRoleStartPicker group={group} role={role} />
                        </td>
                        <td>
                            <GroupRoleEndPicker  group={group} role={role} />
                        </td>
                        <td>
                            <GroupRoleValidButton group={group} role={role}/> 
                        </td>
                    </tr>
            )}
        </tbody>
    )
}

/**
 * 
 * Allows to edit already existing roles, validated / invalidate them and set start and end datetime
 * 
 * @function
 * 
 * @param {Object} props.group
 * Group to be edited
 * 
 * @returns JSX.Element
 */
export const GroupRolesEdit = ({group, onlyValid=true, onlyInvalid=false}) => {
    let roles = group?.roles || []
    let tableHeader = null
    console.log("GroupRolesEdit", onlyValid, onlyInvalid)
    if (onlyInvalid === true) {       
        roles = roles.filter(
            (m) => m.valid === false
        )
        // console.log("GroupEditRoles.invalid", roles)

        tableHeader = "Neaktivní role"
    } else {
        roles = roles.filter(
            (m) => m.valid === onlyValid
        )
        // console.log("GroupEditRoles.valid", roles)
        tableHeader = "Aktivní role"
    }

    return (
        <Table>
            <thead>
                <tr>
                    <th className="table-success" colSpan={6}>{tableHeader}</th>
                </tr>
                <tr>
                    <th>#</th>
                    <th>Role</th>
                    <th>User</th>
                    <th>Start</th>
                    <th>End</th>
                    <th></th>
                </tr>
            </thead>
            <GroupEditRolesTableBody group={group} roles={roles} />
        </Table>
    )
}