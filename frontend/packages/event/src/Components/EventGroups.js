import { Link } from "@uoisfrontend/shared"

export const EventGroup = ({event, group, children}) => {
    return (
        <>
            <span className="btn btn-outline-success">
                <Link id={group.id} tag="group">{group?.name}</Link>
            </span>
            {children}
        </>
    )
}
export const EventGroups = ({event, children}) => {
    const groups = event?.groups || []
    return (
        <>
            {groups.map(
                (group, index) => <EventGroup key={group.id} event={event} group={group}> </EventGroup>
            )}
            {children}
        </>
    )
}