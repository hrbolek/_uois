//const d = new Date()
import FullCalendar from "@fullcalendar/react"
import dayGridPlugin from '@fullcalendar/daygrid'

import { useEffect, useMemo } from "react"
import { Col, Row } from "react-bootstrap"

export const UserEventsCalendar = ({events, actions}) => {
    const transformedEvents = useMemo(
        () => {
            return events?.map(
                event => ({id: event.id, title: event.name, start: event.startdate, end: event.enddate})
            )
        }
    )
    return (
        <FullCalendar
            plugins={[dayGridPlugin]}//, timeGridPlugin, interactionPlugin]}
            headerToolbar={{
              left: 'prev,next today',
              center: 'title',
              right: 'dayGridMonth,timeGridWeek,timeGridDay'
            }}
            initialView='dayGridMonth'
            editable={true}
            selectable={true}
            selectMirror={true}
            dayMaxEvents={true}
            // weekends={this.state.weekendsVisible}
            initialEvents={transformedEvents} // alternatively, use the `events` setting to fetch from a feed
            // select={this.handleDateSelect}
            // eventContent={renderEventContent} // custom render function
            // eventClick={this.handleEventClick}
            // eventsSet={this.handleEvents} // called after events are initialized/added/changed/removed
            /* you can update a remote database when these fire:
            eventAdd={function(){}}
            eventChange={function(){}}
            eventRemove={function(){}}
            */
            />
    )
}
/*


*/
export const UserEventsTableHeader = ({user, events, actions}) => {
    return (
        <thead>
            <tr>
                <th>#</th>
                <th>Název</th>
                <th>Počátek</th>
                <th>Konec</th>
            </tr>
        </thead>
    )
}

export const UserEventsTableRow = ({index, user, event, actions}) => {
    return (
        <tr>
            <td>{index}</td>
            <td>{event.name}</td>
            <td>{event.startdate}</td>
            <td>{event.enddate}</td>
        </tr>
    )
}

export const UserEventsTableBody = ({user, events, actions}) => {
    return (
        <tbody>
            {events?.map(
                (event, index) => <UserEventsTableRow key={event.id} index={index+1} user={user} event={event} actions={actions} />
            )}
        </tbody>
    )
}


export const UserEventsTable = ({user, events, actions}) => {
    return (
        <table className="table table-stripped">
            <UserEventsTableHeader user={user} events={events} actions={actions} />
            <UserEventsTableBody user={user} events={events} actions={actions} />

        </table>
    )
}

export const UserEvents = ({user, actions}) => {
    const events = user?.events
    
    useEffect(
        () => {
            if (events) {
                
            } else {
                actions.onUserEventsFetchAsync(user.id, "2023-01-01", "2023-12-31")
            }
        }
        ,[user]
    )
    // return (<UserEventsTable user={user} events={events} actions={actions} />)
    return (
        <Row>
            <Col></Col>
            <Col>
                <UserEventsCalendar events={events} actions={actions} />
            </Col>
        </Row>
    )
}