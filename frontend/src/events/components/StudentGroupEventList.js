import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { useState, useEffect } from 'react'

import { StudentGroupEvents } from "events/queries/StudentGroupEvents"
import { GroupSmall } from "groups/components/links"; 
import { UserSmall } from "users/components/links";

//const startDate = new Date("2022-11-01")
//const endDate = new Date("2022-12-31")

function addDays(date, delta) {
    const result = new Date(date)
    result.setDate(result.getDate() + delta);
    return result;
  }

function beginOfWeek(date) {
    const delta = date.getDay()
    const result = new Date(date)
    result.setDate(result.getDate() - 6 - delta);
    return result;
}
function endOfWeek(date) {
    const result = new Date(date)
    const delta = result.getDay()
    result.setDate(result.getDate() + 1 - delta);
    return result;
}

export const SingleEvent = ({event}) => {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    //console.log(event.startdate.toLocaleString(undefined, options))
    return (
        <tr>
            <td>{event.name}</td>
            <td>{event.startdate.toLocaleString(undefined, options)}</td>
            <td>{event.enddate.toLocaleString(undefined, options)}</td>
            <td>{event.groups.map(g => <span key={g.id}><GroupSmall group={g} /><br/></span>)}</td>
            <td>{event.organizers.map(u => <span key={u.id}><UserSmall user={u} /><br/></span>)}</td>
        </tr>
    )
}

export const EventTable = ({events}) => {
    return (
        <table className="table table-striped">
            <thead>
                <tr>
                    <th>Název</th>
                    <th>Počátek</th>
                    <th>Konec</th>
                    <th>Skupiny</th>
                </tr>
            </thead>
            <tbody>
                {events.map( e => <SingleEvent key={e.id} event={e} />)}
            </tbody>
        </table>
    )
}

const today = new Date()
export const StudentGroupEventList = (props) => {
    const {group} = props
    const [{startDate, endDate}, setDateInterval]  = useState({startDate: beginOfWeek(today), endDate: endOfWeek(today)})
    const [events, setEvents] = useState([])
    useEffect(()=>{
        StudentGroupEvents(group.id, startDate, endDate)
        .then(response => response.json())
        .then(json => json.data.events)
        .then(events => setEvents(events))
    }, [props.id])
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Udalosti
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <EventTable group={group} events={events}/>
            </Card.Body>
        </Card>
    )
}