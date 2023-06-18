import { CheckGQLError, MsgFlashAction, MsgAddAction, TextInput } from "@uoisfrontend/shared"
import { PlanLessonUpdateAsyncAction } from "../Actions/PlanLessonUpdateAsyncAction"
import { useDispatch } from "react-redux"

export const LessonNameInputbox = ({plan, lesson}) => {
    const dispatch = useDispatch()
    const onChange = (value) => {
        dispatch(PlanLessonUpdateAsyncAction({plan, lesson}))
        .then(
            CheckGQLError({
                "ok": () => dispatch(MsgAddAction({title: "Změna názvu proběhla v pořádku"})),
                "fail": (json) => dispatch(MsgFlashAction({title: "Změna názvu se nepovedla\n" + JSON.stringify(json)})),
            })
        )
    }
    return (
        <TextInput value={lesson.name} id ={lesson.id} placeholder="Zadejte název lekce" onChange={onChange}/>
    )
}