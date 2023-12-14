import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { ProgramFetchAsyncAction } from "../Actions/ProgramFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction, useFreshItem } from "@uoisfrontend/shared"
import { ProgramEditCard } from "../Components/ProgramEditCard"

export const ProgramEditPage = () => {
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
            <ProgramEditCard program={program} />
        )
    } else {
        return <>Loading program...</>
    }
}