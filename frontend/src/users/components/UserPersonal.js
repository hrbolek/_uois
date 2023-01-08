import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { UserSmall } from 'users/components/links';

export const UserPersonal = (props) => {
    const { user } = props
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <UserSmall user={user} />
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col><b>Jméno</b></Col><Col>{user.name}</Col>
                </Row>
                <Row>
                    <Col><b>Příjmení</b></Col><Col>{user.surname}</Col>
                </Row>
                <Row>
                    <Col><b>Email</b></Col><Col>{user.email}</Col>
                </Row>
            </Card.Body>
        </Card>
    )
}