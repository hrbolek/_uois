import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { RoleRow } from 'usersgroups/components/RoleRow';

export const RolesCard = (props) => {
    const { user } = props
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Vedoucí pracovníci
                </Card.Title>
            </Card.Header>
            <Card.Body>
                {user.roles?.map(role => <RoleRow role={role}/>)}
            </Card.Body>
        </Card>
    )
}