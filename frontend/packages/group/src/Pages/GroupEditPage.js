import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { GroupCard } from "../Components/GroupCard"
import { GroupFetchAsyncAction } from "../Actions/GroupFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction, useFreshItem } from "@uoisfrontend/shared"
import { GroupMembersFetchAsyncAction } from "../Actions/GroupMembersFetchAsyncAction"
import { GroupEditCard } from "../Components/GroupEditCard"

export const GroupEditPage = () => {
    const dispatch = useDispatch()

    const id = useParams().id
    const items = useSelector(state => state.items)
    const group = items[id]
    
    useEffect(
        () => {
                dispatch(GroupMembersFetchAsyncAction({id}))
                .then(
                    CheckGQLError({
                        "ok": (json) => dispatch(MsgFlashAction({title: "Nahrání členů skupiny úspěšné"})),
                        "fail": (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
                    })    
                )            
        }
        ,[id]
    )

    if (group){        
        return (
            <GroupEditCard group={group} />
        )
    } else {
        return <>Loading group</>
    }
}