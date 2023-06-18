import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { SurveyCard } from "../Components/SurveyCard"
import { SurveyFetchAsyncAction } from "../Actions/SurveyFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction } from "@uoisfrontend/shared"

export const SurveyPage = () => {
    const dispatch = useDispatch()

    const id = useParams().id
    const items = useSelector(state => state.items)
    const survey = items[id]

    useEffect(
        () => {
            dispatch(SurveyFetchAsyncAction(id))
            .then(
                CheckGQLError({
                    "ok": (json) => dispatch(MsgFlashAction({title: "Nahrání ankety úspěšné"})),
                    "fail": (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
                })
            )
        }
        ,[id, dispatch]
    )

    if (survey){        
        return (
            <SurveyCard survey={survey} />
        )
    } else {
        return <>Loading facility...</>
    }
}