import Card from "react-bootstrap/Card";

import { UserPersonal } from 'users/components/UserPersonal'
import { UserPersonalEdit } from 'users/components/UserPersonalEdit'
import { UserMembership } from 'users/components/UserMembership'
import { UserRoles } from 'users/components/UserRoles'
import { TeacherTimeTable } from 'users/components/TeacherTimeTable'
import { TeacherEventList } from 'events/components/TeacherEventList'

export const UserDebug = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    UserDebug
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <UserPersonalEdit user={props.user} actions={props.actions} /> <br/>
                <UserPersonal user={props.user} /> <br/>
                <TeacherEventList user={props.user} /> <br />
                <TeacherTimeTable user={props.user} /> <br/>
                <UserMembership user={props.user} /> <br />
                <UserRoles user={props.user} />  <br />

            </Card.Body>
            <Card.Footer>
                {JSON.stringify(props)}
            </Card.Footer>
        </Card>
    )
}