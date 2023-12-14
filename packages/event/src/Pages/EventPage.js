import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { EventCard } from "../Components/EventCard"
import { EventFetchAsyncAction } from "../Actions/EventFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction } from "@uoisfrontend/shared"

export const EventPage = () => {
    const dispatch = useDispatch()

    const id = useParams().id
    const items = useSelector(state => state.items)
    const event = items[id]

    useEffect(
        () => {
            dispatch(EventFetchAsyncAction(id))
            .then(
                CheckGQLError({
                    "ok": (json) => dispatch(MsgFlashAction({title: "Nahrání události úspěšné"})),
                    "fail": (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
                })
            )
        }
        ,[]
    )

    if (event){        
        return (
            <EventCard event={event} />
        )
    } else {
        return <>Loading event...</>
    }
}