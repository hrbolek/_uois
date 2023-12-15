import Table from "react-bootstrap/Table";

export const UserGroupsTableRow = ({index, membership, actions}) => {
    return (
        <tr>
            <td>{index}</td>
            <td>{membership?.group?.name}</td>
            <td>{membership?.startdate}</td>
            <td>{membership?.enddate}</td>
        </tr>
    )
}

export const UserGroupsTableBody = ({user, actions, valid}) => {
    let membership = user?.membership || []
    membership = membership.filter(m => m?.valid === valid)
    return (
        <tbody>
            {membership.map(
                (m, index) => <UserGroupsTableRow key={m.id} index={index+1} membership={m} actions={actions} />
            )}
        </tbody>
    )
}

export const UserGroupsTableHeader = ({user, actions}) => {
    return (
        <thead>
            <tr>
                <th>#</th>
                <th>N</th>
                <th>Počátek</th>
                <th>Konec</th>
            </tr>
        </thead>
    )
}

export const UserGroupsTable = ({user, actions}) => {
    return (
        <Table>
            <UserGroupsTableHeader user={user} actions={actions}/>
            <UserGroupsTableBody user={user} actions={actions} valid={true}/>
        </Table>
    )
}