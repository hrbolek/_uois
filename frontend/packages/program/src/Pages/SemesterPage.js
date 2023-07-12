import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { SubjectCard } from "../Components/SubjectCard"
import { SubjectFetchAsyncAction } from "../Actions/SubjectFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction, useFreshItem } from "@uoisfrontend/shared"
import { SemesterFetchAsyncAction } from "../Actions/SemesterFetchAsyncAction"
import { SemesterCard } from "../Components/SemesterCard"

export const SemesterPage = () => {
    const dispatch = useDispatch()

    const {id} = useParams()
    const [semester, query] = useFreshItem({id}, SemesterFetchAsyncAction)
    query.then(
        CheckGQLError({
            "ok": (json) => dispatch(MsgFlashAction({title: "Nahrání objektu úspěšné"})),
            "fail": (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
        })
    )
    

    if (semester){        
        return (
            <SemesterCard semester={semester} />
        )
    } else {
        return <>Loading facility...</>
    }
}