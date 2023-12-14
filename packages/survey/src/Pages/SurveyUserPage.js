import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { CheckGQLError, MsgAddAction, MsgFlashAction, useFreshItem } from "@uoisfrontend/shared"
import { SurveyUserFetchAsyncAction } from "../Actions/SurveyUserFetchAsyncAction"
import { SurveyUserCard } from "../Components/SurveyUserCard"

export const SurveyUserPage = () => {
    const dispatch = useDispatch()

    const {id} = useParams()
    const [user, question] = useFreshItem({id}, SurveyUserFetchAsyncAction)
    question
    .then(
        CheckGQLError({
            ok: () => dispatch(MsgFlashAction({title: "Vse ok"})),
            fail: (json) => dispatch(MsgAddAction({title: "Neco se nepovedlo"}))
        })
    )

    if (user){        
        return (
            <SurveyUserCard user={user} />
        )
    } else {
        return <>Loading facility...</>
    }
}