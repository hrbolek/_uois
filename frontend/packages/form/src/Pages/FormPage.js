import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { FormCard } from "../Components/FormCard"
import { FormFetchAsyncAction } from "../Actions/FormFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction } from "@uoisfrontend/shared"
import { FormComponent } from "../Components/FormTypes"

export const FormPage = () => {
    const dispatch = useDispatch()

    const id = useParams().id
    const items = useSelector(state => state.items)
    const form = items[id]

    useEffect(
        () => {
            dispatch(FormFetchAsyncAction(id))
            .then(
                CheckGQLError({
                    "ok": (json) => dispatch(MsgFlashAction({title: "Nahrání objektu úspěšné"})),
                    "fail": (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
                })
            )
        }
        ,[id, dispatch]
    )

    if (form) {        
        
        return (
            <FormCard form={form} />
        )
    } else {
        return <>Loading form...</>
    }
}