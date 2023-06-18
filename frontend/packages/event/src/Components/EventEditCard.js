import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { Calendar, EyeFill, PencilSquare } from "react-bootstrap-icons"
import { Link } from "@uoisfrontend/shared"
import { EventGroups } from "./EventGroups"
import { EventInvitations } from "./EventInvitations"
import { EventPresenceEditableTable, EventPresences } from "./EventPresences"
import { EventStartPicker } from "./EventStartPicker"
import { EventEndPicker } from "./EventEndPicker"
import { EventInviteUser } from "./EventInviteUser"

/**
 * 
 * @param {Object} props.event 
 * @returns JSX.Element 
 */
export const EventEditCard = ({event}) => {
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <Calendar /> {event.name}
                    </Col>
                    <Col>
                        <div className="float-end"><EventStartPicker event={event} /> </div>
                        
                    </Col>
                    <Col>
                        <EventEndPicker event={event} />
                    </Col>
                    <Col>
                        <div className="d-flex justify-content-end">
                            <Link id={event.id} tag="event"><EyeFill /> </Link>
                        </div>
                    </Col>
                </Row>

            </Card.Header>
            <Card.Body>
                <Row>
                    <Col><EventGroups event={event} /></Col>
                    <hr />
                        {/* <br /> */}
                </Row>
                <Row>
                    <Col>
                        <EventPresenceEditableTable event={event} />
                        
                    </Col>
                </Row>
                Pozvat:
                <EventInviteUser event={event}/>
                {/* {JSON.stringify(event)} */}
            </Card.Body>
        </Card>
    )
}