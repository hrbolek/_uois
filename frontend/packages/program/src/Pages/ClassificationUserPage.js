import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { ProgramCard } from "../Components/ProgramCard"
import { ProgramFetchAsyncAction } from "../Actions/ProgramFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction, useFreshItem } from "@uoisfrontend/shared"
import { UserClassificationFetchAsyncAction } from "../Actions/UserClassificationFetchAsyncAction"
import { UserClassificationCard } from "../Components/UserClassificationCard"

export const ClassificationUserPage = () => {
    const dispatch = useDispatch()

    const {id} = useParams()
    const [user, query] = useFreshItem({id}, UserClassificationFetchAsyncAction)
    console.log("ClassificationUserPage", id)
    query
    .then(
        CheckGQLError({
            "ok": (json) => dispatch(MsgFlashAction({title: "Nahrání objektu úspěšné"})),
            "fail": (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
        })
    )

    if (user){
        return (
            <UserClassificationCard user={user} />
        )
    } else {
        return <>Loading user...</>
    }
}