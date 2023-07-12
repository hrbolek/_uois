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

    const { id } = useParams()
    
    const [group, updateDone] = useFreshItem({id: id}, 
        GroupMembersFetchAsyncAction)

    updateDone
    .then(
        CheckGQLError({
            "ok": (json) => dispatch(MsgFlashAction({ title: "Nahrání skupiny úspěšné" })),
            "fail": (json) => dispatch(MsgAddAction({ title: "Chyba " + JSON.stringify(json) })),
        })
    )
    

    if (group){        
        return (
            <GroupEditCard group={group} />
        )
    } else {
        return <>Loading group</>
    }
}