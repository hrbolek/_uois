import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { UserCard } from "../Components/UserCard"
import { UserFetchAsyncAction } from "../Actions/UserFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction } from "@uoisfrontend/shared"

export const UserPage = () => {
    const dispatch = useDispatch()

    const id = useParams().id
    const items = useSelector(state => state.items)
    const user = items[id]

    useEffect(
        () => {
            dispatch(UserFetchAsyncAction({id}))
            .then(
                CheckGQLError({
                    "ok": (json) => dispatch(MsgFlashAction({title: "Nahrání uživatele úspěšné"})),
                    "fail": (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
                })
            )
        }
        ,[id]
    )

    if (user){        
        return (
            <UserCard user={user} />
        )
    } else {
        return <>Loading user...</>
    }
}