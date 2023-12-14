import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { FormFetchAsyncAction } from "../Actions/FormFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction, useFreshItem } from "@uoisfrontend/shared"
import { FormEditCard } from "../Components/FormEditCard"
import { FormComponent } from "../Components/FormTypes"

export const FormEditPage = () => {
    const dispatch = useDispatch()

    const {id} = useParams()
    const [item] = useFreshItem({id}, FormFetchAsyncAction)
    // const items = useSelector(state => state.items)
    // const form = items[id]

    // useEffect(
    //     () => {
    //         dispatch(FormFetchAsyncAction(id))
    //         .then(
    //             CheckGQLError({
    //                 "ok": (json) => dispatch(MsgFlashAction({title: "Nahrání objektu úspěšné"})),
    //                 "fail": (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
    //             })
    //         )
    //     }
    //     ,[id, dispatch]
    // )

    if (item) {        
        return (
            <FormEditCard form={item} mode="edit"/>
        )
    } else {
        return <>Loading form...</>
    }
}