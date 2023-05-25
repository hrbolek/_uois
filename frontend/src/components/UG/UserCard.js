import Card from "react-bootstrap/Card"
import { UserGroupsTable } from "./UserGroupsTable"
import { UserRolesTable } from "./UserRolesTable"
import { PencilFill } from "react-bootstrap-icons"
import Form from "components/Form"
import { UserEvents } from "./UserEvents"


export const UserCard = ({user, actions}) => {
    return (
        <Card>
            <Card.Header>
                {user.name} {user.surname} ({user.email}) {user.id} <Form.Link tag={"useredit"} id={user.id}><PencilFill /></Form.Link>
            </Card.Header>
            <Card.Body>
                <h3>Kalendář</h3>
                <UserEvents user={user} actions={actions} />
                <h3>Členství</h3>
                <UserGroupsTable user={user} actions={actions} />
                <h3>Role</h3>
                <UserRolesTable user={user} actions={actions} />
            </Card.Body>
        </Card>
    )
}