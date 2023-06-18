import { Table } from "react-bootstrap"
import { EventStartPicker } from "./EventStartPicker"
import { AddSemesterButton } from "./AddSemesterButton"
import { Link } from "@uoisfrontend/shared"

function EventSubEventTableRow({event}) {
    return <tr>
        <td>#</td>
        <td>
            <Link tag="event" id={event.id}>
                {event.name}
            </Link>
        </td>
        <td>{event.startdate}</td>
        <td>{event.enddate}</td>
        <td></td>
    </tr>
}

export const EventSubEventsEditableTable = ({event, children}) => {
    const subevents = event?.subEvents || []
    return (
        <Table bordered striped size="sm" >
            <thead>
                <tr>
                    <th>#</th>
                    <th>Název</th>
                    <th>Počátek</th>
                    <th>Konec</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                {subevents.map(e => 
                    <EventSubEventTableRow key={e.id} event={e} />
                )
                }
            </tbody>
            <tfoot>
                <tr>
                    <th colSpan={5}>
                        {children}
                    </th>
                </tr>
                
            </tfoot>
        </Table>
    )
}

