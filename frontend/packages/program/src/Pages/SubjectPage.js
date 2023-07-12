import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { SubjectCard } from "../Components/SubjectCard"
import { SubjectFetchAsyncAction } from "../Actions/SubjectFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction, useFreshItem } from "@uoisfrontend/shared"

export const SubjectPage = () => {
    const dispatch = useDispatch()

    const {id} = useParams()
    const [subject, query] = useFreshItem({id}, SubjectFetchAsyncAction)
    query
    .then(
        CheckGQLError({
            "ok": (json) => dispatch(MsgFlashAction({title: "Nahrání předmětu úspěšné"})),
            "fail": (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
        })
    ).then(
        json => console.log(json)
    )

    if (subject){        
        return (
            <SubjectCard subject={subject} />
        )
    } else {
        return <>Loading subject...{JSON.stringify(subject)}</>
    }
}