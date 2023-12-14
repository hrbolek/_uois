import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { EventCard } from "../Components/EventCard"
import { EventFetchYearsAsyncAction } from "../Actions/EventFetchYearsAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction } from "@uoisfrontend/shared"
import { EventPlanEditCard } from "../Components/EventPlanEditCard"

export const EventPlanEditPage = () => {
    const dispatch = useDispatch()

    const id = "a517c2fd-8dc7-4a2e-a107-cbdb88ba2aa5"
    const items = useSelector(state => state.items)
    const plan = items[id]

    useEffect(
        () => {
            dispatch(EventFetchYearsAsyncAction(id))
            .then(
                CheckGQLError({
                    "ok": (json) => dispatch(MsgFlashAction({title: "Nahrání události úspěšné"})),
                    "fail": (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
                })
            )
        }
        ,[]
    )

    if (plan){        
        return (
            <EventPlanEditCard plan={plan}/>
        )
    } else {
        return <>Loading event...</>
    }
}