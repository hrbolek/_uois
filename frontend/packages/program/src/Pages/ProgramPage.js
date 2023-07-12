import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { ProgramCard } from "../Components/ProgramCard"
import { ProgramFetchAsyncAction } from "../Actions/ProgramFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction, useFreshItem } from "@uoisfrontend/shared"

export const ProgramPage = () => {
    const dispatch = useDispatch()
    const {id} = useParams()   
    const [program, query] = useFreshItem({id}, ProgramFetchAsyncAction)
    query
    .then(
        CheckGQLError({
            "ok": (json) => dispatch(MsgFlashAction({title: "Nahrání objektu úspěšné"})),
            "fail": (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
        })
    )

    if (program){        
        return (
            <ProgramCard program={program} />
        )
    } else {
        return <>Loading facility...</>
    }
}