import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { SurveyFetchAsyncAction } from "../Actions/SurveyFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction } from "@uoisfrontend/shared"
import { SurveyEditCard } from "../Components/HomeCard"

export const HomePage = () => {
    // const dispatch = useDispatch()

    // const id = useParams().id
    // const items = useSelector(state => state.items)
    // const facility = items[id]

    // useEffect(
    //     () => {
    //         dispatch(SurveyFetchAsyncAction(id))
    //         .then(
    //             CheckGQLError({
    //                 "ok": (json) => dispatch(MsgFlashAction({title: "Nahrání objektu úspěšné"})),
    //                 "fail": (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
    //             })
    //         )
    //     }
    //     ,[id, dispatch]
    // )

    return <HomePage />
}