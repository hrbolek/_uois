import { useDispatch } from "react-redux"
import { CheckGQLError, MsgAddAction, MsgFlashAction } from "@uoisfrontend/shared";
import { DateTimePicker }   from "./DateTimePicker"
import { EventUpdateAsyncAction } from "../Actions/EventUpdateAsyncAction";

export const EventStartPicker = ({event}) => {
    const dispatch = useDispatch()
    const onDateChange = (value) => {
        const updatedEvent = {...event, startdate: value}
        dispatch(EventUpdateAsyncAction(updatedEvent))
        .then(
            CheckGQLError({
                "ok": () => dispatch(MsgFlashAction({title: "Změna ok"})),
                "fail": (json) => dispatch(MsgAddAction({title: "Změna se nepovedla\n " + JSON.stringify(json)}))
            })
        )
    }
    // const cdate = membership.enddate ? new Date(membership.enddate + 'Z'): null
    return (
        <DateTimePicker selected={event.startdate} onChange={onDateChange}
            startDate={event.startdate} endDate={event.endDate}
         />
    )
}