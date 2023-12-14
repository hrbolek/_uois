import { Link } from "@uoisfrontend/shared"

export const EventInvitation = ({event, presence, children}) => {
    const user = presence?.user
    const invitation = presence?.invitationType?.name
    // console.log("EventInvitation", user)
    // console.log("EventInvitation", invitation)
    if (user && invitation ) {
        return (
            <>
                <span className="btn btn-outline-success">
                <Link id={user.id} tag="user">{user.name} {user.surname}</Link> - 
                {invitation}  
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

export const EventInvitations = ({event, children}) => {
    const presences = event?.presences || []
    return (
        <>
            {presences.map(
                (presence, index) => <EventInvitation key={presence.id} event={event} presence={presence}> </EventInvitation>
            )}
        </>
    )
}