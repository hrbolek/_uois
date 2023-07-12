import { useDispatch } from "react-redux"
import { PlanLessonInsertAsyncAction } from "../Actions/PlanLessonInsertAsyncAction"
import { CheckGQLError } from "@uoisfrontend/shared"
import { MsgAddAsyncAction, MsgFlashAsyncAction } from "reducers/msgsreducers"
import { PlusLg } from "react-bootstrap-icons"

export const PlanAddLessonButton = ({plan, name="Nová lekce", lessontype_id="e2b7cbf6-95e1-11ed-a1eb-0242ac120002"}) => {
    const dispatch = useDispatch()
    const lessons = plan?.lessons || []
    const onClick = () => {
        dispatch(PlanLessonInsertAsyncAction({name, lessontype_id, plan_id: plan.id, order: lessons.length + 1, length: 2}))
        .then(
            CheckGQLError({
                "ok": () => dispatch(MsgFlashAsyncAction({title: "Přidání lekce úspěšné"})),
                "fail": (json) => dispatch(MsgAddAsyncAction({title: "Přidání lekce se nepovedlo\n" + JSON.stringify(json)})),
            })
        )
    }
    return (
        <button className="btn form-control btn-outline-success" onClick={onClick}><PlusLg /> Přidat lekci</button>
    )
}

