import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";


import { FacultySmall } from 'usersgroups/components/links';
import { RoleRow } from 'usersgroups/components/rolerow';

export const FacultyMedium = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <FacultySmall {...props} />
                </Card.Title>
            </Card.Header>
            <Card.Body>
                {props.roles.map(role => <RoleRow {...role}/>)}
            </Card.Body>
        </Card>
    )
}

export const GroupMedium = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <FacultySmall {...props} />
                </Card.Title>
            </Card.Header>
            <Card.Body>
                {props.roles.map(role => <RoleRow {...role}/>)}
            </Card.Body>
        </Card>
    )
}

