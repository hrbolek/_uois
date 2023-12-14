import { Calendar3Fill } from "react-bootstrap-icons"
import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"
import { UserAddEventButton, UserEvents } from "../Components"

export const UserEventsCard = ({user}) => {
    return (
        <Card>
            <Card.Header>
               <Calendar3Fill /> Kalendar {user.email}
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col>
                        {/* <UserEvents user={user} /> */}
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <UserAddEventButton user={user} />
                    </Col>
                </Row>
                
            </Card.Body>
        </Card>
    )
}