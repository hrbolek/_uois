import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { PlanFetchAsyncAction } from "../Actions/PlanFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction } from "@uoisfrontend/shared"
import { PlanEditCard } from "../Components/PlanEditCard"

export const PlanEditPage = () => {
    const dispatch = useDispatch()

    const id = useParams().id
    const items = useSelector(state => state.items)
    const plan = items[id]

    useEffect(
        () => {
            dispatch(PlanFetchAsyncAction(id))
            .then(
                CheckGQLError({
                    "ok": (json) => dispatch(MsgFlashAction({title: "Nahrání objektu úspěšné"})),
                    "fail": (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
                })
            )
        }
        ,[id, dispatch]
    )

    if (plan){        
        return (
            <PlanEditCard plan={plan} />
        )
    } else {
        return <>Loading plan...</>
    }
}