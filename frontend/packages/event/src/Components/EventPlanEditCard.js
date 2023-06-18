import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { Calendar, PencilSquare } from "react-bootstrap-icons"
import { Link } from "@uoisfrontend/shared"

import { EventSubEventsEditableTable } from "./EventSubEventsEditableTable"
import { AddSchoolYearButton } from "./AddSchoolYearButton"
import { AddSemesterButton } from "./AddSemesterButton"

// EventFetchYearsAsyncAction

export const EventYear = ({event}) => {
    return (
        <>
            {event.name} <br/>
            <EventSubEventsEditableTable event={event}>
                <AddSemesterButton />
            </EventSubEventsEditableTable> 
            
        </>
    )
}

export const EventPlanEditCard = ({plan}) => {
    const years = plan?.events || []
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <Calendar /> "Plán"
                    </Col>
                    <Col>
                        {/* {event?.startdate} - {event?.enddate} */}
                    </Col>
                    <Col>
                        
                    </Col>
                    <Col>
                        {/* <div className="d-flex justify-content-end">
                            <Link id={event.id} tag="eventedit"><PencilSquare /> </Link>
                        </div> */}
                    </Col>
                </Row>

            </Card.Header>
            <Card.Body>
                {years.map(y => <EventYear key={y.id} event={y} />

                )}
                <hr />
                <AddSchoolYearButton />
            </Card.Body>
            <Card.Body>               
                
                {JSON.stringify(plan)}
            </Card.Body>
        </Card>
    )
}