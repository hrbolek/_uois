import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { PlanFetchAsyncAction } from "../Actions/PlanFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction, useFreshItem } from "@uoisfrontend/shared"
import { PlanEditCard } from "../Components/PlanEditCard"

export const PlanEditPage = () => {
    const dispatch = useDispatch()

    const {id} = useParams()
    const [plan, query] = useFreshItem({id}, PlanFetchAsyncAction)
    query
    .then(
        CheckGQLError({
            "ok": (json) => dispatch(MsgFlashAction({title: "Nahrání objektu úspěšné"})),
            "fail": (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
        })
    )


    if (plan){        
        return (
            <PlanEditCard plan={plan} />
        )
    } else {
        return <>Loading plan...</>
    }
}