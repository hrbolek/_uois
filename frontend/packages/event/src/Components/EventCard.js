import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { Calendar, PencilSquare } from "react-bootstrap-icons"
import { Link } from "@uoisfrontend/shared"
import { EventGroups } from "./EventGroups"
import { EventInvitations } from "./EventInvitations"
import { EventPresences } from "./EventPresences"

export const EventCard = ({event}) => {
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <Calendar /> {event.name}
                    </Col>
                    <Col>
                        {event?.startdate} - {event?.enddate}
                    </Col>
                    <Col>
                        
                    </Col>
                    <Col>
                        <div className="d-flex justify-content-end">
                            <Link id={event.id} tag="eventedit"><PencilSquare /> </Link>
                        </div>
                    </Col>
                </Row>

            </Card.Header>
            <Card.Body>
                <Row>
                    <Col><EventGroups event={event} /></Col>
                    <Col><EventInvitations event={event} /></Col>
                    <Col><EventPresences event={event} /></Col>
                </Row>
                
                
                {JSON.stringify(event)}
            </Card.Body>
        </Card>
    )
}