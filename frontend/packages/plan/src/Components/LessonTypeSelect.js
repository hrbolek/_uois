import { CheckGQLError, MsgFlashAction, MsgAddAction, SelectFloatingElement, SelectElement } from "@uoisfrontend/shared"
import { PlanLessonUpdateAsyncAction } from "../Actions/PlanLessonUpdateAsyncAction"
import { useDispatch } from "react-redux"

import { createAttributeSelectEditor } from "@uoisfrontend/shared"
import { LessonTypeFetch } from "../Actions/LessonTypeFetch"
import { useEffect, useState } from "react"

// const LessonTypeSelector_ = createAttributeSelectEditor({label: "typ lekce", attributeName: "type_id", asyncAction: PlanLessonUpdateAsyncAction, asyncFetchItemsAction: LessonTypeFetch})
// const LessonTypeSelector__ = ({lesson}) => <LessonTypeSelector item={{...lesson, type_id: lesson?.type?.id}} />

export const LessonTypeSelector = ({lesson, ...props}) => {
    const [options, setOptions] = useState([])
    useEffect(
        () => {
            if (options.length === 0) {
                LessonTypeFetch({})
                .then(json => {
                    // console.log("LessonTypeSelector got", json)
                    const result = json?.data?.result
                    if (result) {
                        setOptions(result)
                    }
                    return json
                })
            }
        }
    )
    const onChange = (newValue) => {
        const newItem = {...lesson, type_id: newValue}
        // newItem[attributeName] = newValue
        // asyncAction(newItem)
        PlanLessonUpdateAsyncAction(newItem)
    }
    return <SelectElement value={lesson?.type?.id} label={"typ lekce"} options={options} onChange={onChange} {...props}/>
    // return (
    //     <>
    //     {JSON.stringify(options)}
    //     </>
    // )
}


export const LessonTypeSelect = ({plan, lesson}) => {
    const dispatch = useDispatch()
    const onChange = (value) => {
        // console.log("LessonTypeSelect.zmena", value)
        dispatch(PlanLessonUpdateAsyncAction({plan, lesson: {...lesson, lessontype_id: value}}))
        .then(
            CheckGQLError({
                "ok": () => dispatch(MsgFlashAction({title: "Změna názvu proběhla v pořádku"})),
                "fail": (json) => dispatch(MsgAddAction({title: "Změna názvu se nepovedla\n" + JSON.stringify(json)})),
            })
        )
    }
    return (
        // <TextInput value={lesson.name} id ={lesson.id} placeholder="Zadejte název lekce" onChange={onChange}/>
        <>
            {/* {lesson?.type?.name} */}
            <LessonTypeSelector lesson={lesson} onChange={onChange}/>
        </>
    )
}