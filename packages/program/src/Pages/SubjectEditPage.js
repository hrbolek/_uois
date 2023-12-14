import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { SubjectFetchAsyncAction } from "../Actions/SubjectFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction } from "@uoisfrontend/shared"
import { SubjectEditCard } from "../Components/SubjectEditCard"

export const SubjectEditPage = () => {
    const dispatch = useDispatch()

    const id = useParams().id
    const items = useSelector(state => state.items)
    const subject = items[id]

    useEffect(
        () => {
            dispatch(SubjectFetchAsyncAction(id))
            .then(
                CheckGQLError({
                    "ok": (json) => dispatch(MsgFlashAction({title: "Nahrání objektu úspěšné"})),
                    "fail": (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
                })
            )
        }
        ,[]
    )

    if (subject){        
        return (
            <SubjectEditCard subject={subject} />
        )
    } else {
        return <>Loading subject...</>
    }
}