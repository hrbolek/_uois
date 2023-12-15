import Form from "components/Form";
import { Plus, TrashFill } from "react-bootstrap-icons";
import Table from "react-bootstrap/Table";

export const UserRolesTableRow = ({index, role, actions}) => {
    return (
        <tr>
            <td>{index}</td>
            <td>{role?.roletype?.name}</td>
            <td>{role?.group?.name}</td>
            <td>{role?.startdate}</td>
            <td>{role?.enddate}</td>
        </tr>
    )
}

export const UserRolesTableBody = ({user, actions}) => {
    return (
        <tbody>
            {user?.roles?.map(
                (role, index) => <UserRolesTableRow key={role.id} index={index+1} role={role} actions={actions} />
            )}
            
        </tbody>
    )
}

export const UserRolesTableHeader = ({user, actions}) => {
    return (
        <thead>
            <tr>
                <th className="">#</th>
                <th className="w-25">Role</th>
                <th className="w-25">Skupina</th>
                <th className="w-25">Počátek</th>
                <th className="w-25">Konec</th>
                <th className="w-25"></th>
            </tr>
        </thead>
    )
}

export const UserRolesTable = ({user, actions}) => {
    return (
        <Table>
            <UserRolesTableHeader user={user} actions={actions}/>
            <UserRolesTableBody user={user} actions={actions}/>
        </Table>
    )
}