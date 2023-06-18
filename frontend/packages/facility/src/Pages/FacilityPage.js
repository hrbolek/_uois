import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { FacilityCard } from "../Components/FacilityCard"
import { FacilityFetchAsyncAction } from "../Actions/FacilityFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction } from "@uoisfrontend/shared"

export const FacilityPage = () => {
    const dispatch = useDispatch()

    const id = useParams().id
    const items = useSelector(state => state.items)
    const facility = items[id]

    useEffect(
        () => {
            dispatch(FacilityFetchAsyncAction(id))
            .then(
                CheckGQLError({
                    "ok": (json) => dispatch(MsgFlashAction({title: "Nahrání objektu úspěšné"})),
                    "fail": (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
                })
            )
        }
        ,[id, dispatch]
    )

    if (facility){        
        return (
            <FacilityCard facility={facility} />
        )
    } else {
        return <>Loading facility...</>
    }
}