import { CheckGQLError } from "@uoisfrontend/shared"
import { useDispatch } from "react-redux"
import { LessonAddTeacherAsyncAction } from "../Actions/LessonAddTeacherAsyncAction"
import { LessonRemoveTeacherAsyncAction } from "../Actions/LessonRemoveTeacherAsyncAction"
import { MsgAddAsyncAction, MsgFlashAsyncAction } from "reducers/msgsreducers"
import { AddRemoveButton } from "./AddRemoveButton"

export const LessonAddRemoveTeacherButton = ({plan, lesson, user}) => {
    const present = lesson.users.find(u => u.id === user.id)? true: false
    const dispatch = useDispatch()
    const onChangeValue = (value) => {
        if (value) {
            dispatch(LessonAddTeacherAsyncAction({plan_id: plan.id, lesson_id: lesson.id, user_id: user.id}))
            .then(
                CheckGQLError({
                    "ok": () => dispatch(MsgFlashAsyncAction({title: "Přiřazení vyučujícícho proběhlo úspěšně"})),
                    "fail": (json) => dispatch(MsgAddAsyncAction({title: "Přiřazení vyučujícícho se nepovedlo\n" + JSON.stringify(json)})),
                })
            )
        } 
        else {
            dispatch(LessonRemoveTeacherAsyncAction({plan_id: plan.id, lesson_id: lesson.id, user_id: user.id}))
            .then(
                CheckGQLError({
                    "ok": () => dispatch(MsgFlashAsyncAction({title: "Odebrání vyučujícícho proběhlo úspěšně"})),
                    "fail": (json) => dispatch(MsgAddAsyncAction({title: "Odebrání vyučujícícho se nepovedlo\n" + JSON.stringify(json)})),
                })
            )

        }
    }
    return <AddRemoveButton state={present} onChangeValue={onChangeValue}/>
}