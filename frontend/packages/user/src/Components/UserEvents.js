import { useDispatch } from "react-redux"
import { UserEventsFetchAsyncAction } from "../Actions/UserEventsFetchAsyncAction"
import { useEffect } from "react"
import { CheckGQLError, Link, MsgAddAction, MsgFlashAction } from "@uoisfrontend/shared"

export const UserEvent = ({user, event}) => {
    return (
        <>
            <Link tag="event" id={event.id}>
                {event?.startdate} - {event?.enddate} / {event?.name}
             </Link>
        </>
    )
    // return <>Event{JSON.stringify(event)} :)</>
}

export const UserEvents = ({user}) => {
    const events = user?.events
    const dispatch = useDispatch()
    useEffect(
        () => {
            if (events) {

            } else {
                console.log("UserEvents useEffect")
                dispatch(UserEventsFetchAsyncAction(user.id))
                .then(
                    CheckGQLError({
                        errors: (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
                        ok: (json) => dispatch(MsgFlashAction({title: "Načtení událostí v pořádku "})),
                    })
                )
            }
        }
        , []
    )
    if (events) {
        // return <>{JSON.stringify(user)}</>
        return (
            <>
            {events.map(
                (event, index) => <UserEvent key={event.id} event={event} user={user} />
            )}
            </>
        )
    } else {
        return <>{JSON.stringify(user)}</>
    }
}