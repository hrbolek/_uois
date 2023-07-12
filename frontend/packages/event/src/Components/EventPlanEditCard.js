import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { Calendar, PencilSquare } from "react-bootstrap-icons"
import { Link } from "@uoisfrontend/shared"

import { EventSubEventsEditableTable } from "./EventSubEventsEditableTable"
import { AddSchoolYearButton } from "./AddSchoolYearButton"
import { AddSemesterButton } from "./AddSemesterButton"
import { Table } from "react-bootstrap"
import { useState } from "react"

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

export const EventPlanTableHeader = ({events}) => {
    return (
        <thead>
            <tr>
                <th colSpan={3}>#</th>
                <th colSpan={3}>ZS</th>
                <th colSpan={3}>LS</th>
            </tr>
        </thead>
    )
}

export const EventPlanTableRow = ({event}) => {
    const semesters = event?.subEvents || []
    const zs = semesters[0]
    const ls = semesters[0]
    return (
            <tr>
                <td>
                    <Link id={event.id} tag="event">{event.name}</Link>
                </td>
                <td>
                    {event.startdate}
                </td>
                <td>
                    {event.enddate}
                </td>
                
                {zs?<>
                    <td>
                        <Link id={zs.id} tag="event">{zs.name}</Link>
                    </td>
                    <td>{zs.startdate}</td>
                    <td>{zs.enddate}</td>
                    </>: 
                    <td colSpan={3}>
                        <AddSemesterButton />
                    </td>
                }
                {ls?
                    <>
                    <td>
                        <Link id={ls.id} tag="event">{ls.name}</Link>
                    </td>
                    <td>{ls.startdate}</td>
                    <td>{ls.enddate}</td>
                    </>: 
                    <td colSpan={3}>
                        <AddSemesterButton />
                    </td>
                }
                
            </tr>       
    )
}

export const EventPlanTable = ({events}) => {
    const events_ = [...events]
    events_.sort((a, b) => {
        if (a.name < b.name) return 1
        if (a.name > b.name) return -1
        return 0
    })
    return (
        <Table bordered striped>
            <EventPlanTableHeader />
            <tbody>
            {events_.map(
                event => <EventPlanTableRow key={event.id} event={event} />
            )}
            </tbody>
            <tfoot>
                <tr>
                    <th colSpan={3}><AddSchoolYearButton /></th>
                    <th colSpan={6}></th>
                </tr>
            </tfoot>
        </Table>
    )
}


export const DayCell = ({index, onMouseEnter, ...props}) => {
    const onMouseEnter_ = () => {
        if (onMouseEnter) {
            onMouseEnter(index)
        }
    }
    return (
        <td onMouseEnter={onMouseEnter_} {...props}>{" "}</td>
    )
}

export const Weeks = ({cols=15}) => {
    const [cols_] = useState(
        (() => { 
            return new Array(cols).fill(0)
        })()
    )
    return (
        <Table>
            <thead></thead>
            <tbody>
                <tr>
                    {cols_.map((item, index) =>
                        <td key={index}>{index}</td>
                    )}
                </tr>
            </tbody>
        </Table>
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
                <EventPlanTable events={plan.events} />
            </Card.Body>
            <Card.Body>               
                
                {JSON.stringify(plan)}
            </Card.Body>
        </Card>
    )
}