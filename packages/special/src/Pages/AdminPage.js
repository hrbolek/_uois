import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { AdminCard } from "../Components/AdminCard"
import { SurveyFetchAsyncAction } from "../Actions/SurveyFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction } from "@uoisfrontend/shared"

export const AdminPage = () => {
    // const dispatch = useDispatch()

    // const id = useParams().id
    // const items = useSelector(state => state.items)
    // const survey = items[id]

    // useEffect(
    //     () => {
    //         dispatch(SurveyFetchAsyncAction(id))
    //         .then(
    //             CheckGQLError({
    //                 "ok": (json) => dispatch(MsgFlashAction({title: "Nahrání ankety úspěšné"})),
    //                 "fail": (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
    //             })
    //         )
    //     }
    //     ,[id, dispatch]
    // )

    return (
        <AdminCard  />
    )
}