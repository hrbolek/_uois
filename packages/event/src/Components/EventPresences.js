import Table from "react-bootstrap/Table"
import { Link } from "@uoisfrontend/shared"
import { EventPresenceSelect } from "./EventPresenceSelect"
import { EventInvitationSelect } from "./EventInvitationSelect"

export const EventPresence = ({event, presence, children}) => {
    const user = presence?.user
    const presenceTypeName = presence?.presenceType?.name
    // console.log("EventPresence", user)
    // console.log("EventPresence", presence)
    if (user && presenceTypeName ) {
        return (
            <>
                <span className="btn btn-outline-success">
                <Link id={user.id} tag="user">{user.name} {user.surname}</Link> - 
                {presenceTypeName}  
                </span>
                {children}
            </>
        )    
    } else {
        return (
            <>{JSON.stringify(presence)}{children}</>
        )
    }
}

export const EventPresences = ({event, children}) => {
    let presences_ = event?.presences || []
    // presences.sort((a,b)=> {
    //     if (a.user.id < b.user.id) {return -1}
    //     if (a.user.id > b.user.id) {return 1}
    //     return 0
    // })    
    let presences = [...presences_]
    // presences.sort((a,b)=> a.user.email.localeCompare(b.user.email))

    presences.sort((a,b)=> {
        if (a.user.email < b.user.email) {return -1}
        if (a.user.email > b.user.email) {return 1}
        return 0
    })
    // console.log("EventPresences", presences)
    return (
        <>
            {presences.map(
                (presence, index) => <EventPresence key={presence.id} event={event} presence={presence}> </EventPresence>
            )}
        </>
    )
}

export const EventPresenceEditableTable = ({event}) => {
    const presences_ = event?.presences || []
    let presences = [...presences_]
    presences.sort((a,b)=> a.user.email.localeCompare(b.user.email))

    // presences.sort((a,b)=> {
    //     if (a.user.email < b.user.email) {return -1}
    //     if (a.user.email > b.user.email) {return 1}
    //     return 0
    // })
    return (
        <Table size="sm" striped bordered>
            <thead>
                <tr className="table-success">
                    <th>#</th>
                    <th className="w-25">Jméno</th>
                    <th className="w-25">Pozvánka</th>
                    <th className="w-25">Přítomnost</th>
                    <th className="w-25"></th>
                </tr>
            </thead>
            <tbody>
                {presences.map(
                        (presence, index) => <tr key={presence.id}>
                            <td>{index + 1}</td>
                            <td>
                                <span className="">
                                    <Link tag="user" id={presence?.user?.id}>{presence?.user?.name} {presence?.user?.surname}</Link>
                                </span>
                            </td>
                            <td><EventInvitationSelect event={event} presence={presence} /></td>                           
                            <td><EventPresenceSelect presence={presence} /></td>
                            <td></td>
                        </tr>
                )}
            </tbody>
        </Table>
    )
}
