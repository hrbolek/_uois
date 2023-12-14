import { CheckGQLError, MsgFlashAction, MsgAddAction, TextInput } from "@uoisfrontend/shared"
import { PlanLessonUpdateAsyncAction } from "../Actions/PlanLessonUpdateAsyncAction"
import { useDispatch } from "react-redux"

export const LessonNameInputbox = ({plan, lesson}) => {
    const dispatch = useDispatch()
    const onChange = (value) => {
        dispatch(PlanLessonUpdateAsyncAction({plan, lesson: {...lesson, name: value}}))
        .then(
            CheckGQLError({
                "ok": () => dispatch(MsgFlashAction({title: "Změna názvu proběhla v pořádku"})),
                "fail": (json) => dispatch(MsgAddAction({title: "Změna názvu se nepovedla\n" + JSON.stringify(json)})),
            })
        )
    }
    return (
        <TextInput value={lesson.name} id ={lesson.id} placeholder="Zadejte název lekce" onChange={onChange}/>
    )
}