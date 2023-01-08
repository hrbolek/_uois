import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { FacultySmall, UniversitySmall, TeacherSmall } from 'usersgroups/components/links'

export const GroupMembers = (props) => {
    const validMemberships = props.memberships.filter( m => m.valid)
    const validMemmbers = validMemberships.map( m => m.user )
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Členové {props.name}
                </Card.Title>
            </Card.Header>
            <Card.Body>
                {validMemmbers.map(
                    (user) => <><TeacherSmall key={user.id} {...user} /> <br/></>
                )}
            </Card.Body>
        </Card>
    )
}