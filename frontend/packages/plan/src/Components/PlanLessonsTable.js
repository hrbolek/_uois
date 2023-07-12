import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"
import Table from "react-bootstrap/Table"

import { CheckSquare, CheckSquareFill, PencilSquare, Plus, PlusSquareFill, Receipt, Square, TrashFill } from "react-bootstrap-icons"
import { CheckGQLError, DeleteButton, Demo, Link, TextInput } from "@uoisfrontend/shared"
import { useDispatch } from "react-redux"
import { LessonRemoveFacilityAsyncAction } from "../Actions/LessonRemoveFacilityAsyncAction"
import { LessonAddTeacherAsyncAction } from "../Actions/LessonAddTeacherAsyncAction"
import { LessonRemoveGroupAsyncAction } from "../Actions/LessonRemoveGroupAsyncAction"
import { LessonAddGroupAsyncAction } from "../Actions/LessonAddGroupAsyncAction"
import { LessonRemoveTeacherAsyncAction } from "../Actions/LessonRemoveTeacherAsyncAction"
import { useState } from "react"
import { Form, InputGroup } from "react-bootstrap"
import { UserSearch } from "@uoisfrontend/user"
import { GroupSearch } from "@uoisfrontend/group"
import { FacilitySearch } from "@uoisfrontend/facility"
import { MsgAddAsyncAction, MsgFlashAsyncAction } from "reducers/msgsreducers"


export const LessonItemButton = ({id, name, linktag, children}) => (
    <span>
        <span key={id} className="btn btn-sm btn-outline-success">
            <Link id={id} tag={linktag}>{name}</Link>
        </span>
        {children}
    </span>
)

export const LessonItemDeleteButton = ({onClick}) => (
    <DeleteButton onClick={onClick}><TrashFill /></DeleteButton>
)

export const LessonItemPlusButton = ({onClick}) => (
    <DeleteButton onClick={onClick}><PlusSquareFill /></DeleteButton>
)

export const LessonFacilityButton = ({facility, children}) => (
    <LessonItemButton linktag="facility" id={facility.id} name={facility.name}>
        {children}
    </LessonItemButton>
)

export const LessonFacilityDeleteButton = ({lesson, facility}) => {
    const dispatch = useDispatch()    
    const onFacilityDelete = () =>
        dispatch(LessonRemoveFacilityAsyncAction({facility_id: facility.id, lesson_id: lesson.id}))
    return (
        <LessonFacilityButton facility={facility}>
            <LessonItemDeleteButton onClick={onFacilityDelete} />
        </LessonFacilityButton>
)}

export const LessonGroupButton = ({group, children}) => (
    <LessonItemButton linktag="group" id={group.id} name={group.name}>
        {children}
    </LessonItemButton>
)

export const LessonGroupDeleteButton = ({lesson, group}) => {
    const dispatch = useDispatch()    
    const onGroupDelete = () =>
        dispatch(LessonRemoveGroupAsyncAction({group_id: group.id, lesson_id: lesson.id}))
    return (
        <LessonGroupButton group={group}>
            <LessonItemDeleteButton onClick={onGroupDelete} />
        </LessonGroupButton>
)}

export const LessonTeacherButton = ({user, children}) => (
    <LessonItemButton linktag="user" id={user.id} name={user.name + " " + user.surname}>
        {children}
    </LessonItemButton>
)

export const LessonTeacherDeleteButton = ({lesson, user}) => {
    const dispatch = useDispatch()    
    const onUserDelete = () =>
        dispatch(LessonRemoveTeacherAsyncAction({user_id: user.id, lesson_id: lesson.id}))
        .then(
            CheckGQLError({
                "ok": () => dispatch(MsgFlashAsyncAction({title: "Odebrání vyučujícího proběhlo úspěšně"})),
                "fail": (json) => dispatch(MsgFlashAsyncAction({title: "Odebrání vyučujícího se nepovedlo" + JSON.stringify(json)})),
            })
        )
    return (
        <LessonTeacherButton user={user}>
            <LessonItemDeleteButton onClick={onUserDelete} />
        </LessonTeacherButton>
)}

export const LessonTeacherList = ({plan, lesson}) => {
    const users = lesson?.users || []
    return (
        <>
            {users.map(
                (user, index) => <LessonTeacherButton key={user.id} user={user} />
            )}
        </>
    )
}

export const LessonTeacherListDeletable = ({plan, lesson}) => {
    const users = lesson?.users || []
    return (
        <>
            {users.map(
                (user, index) => <LessonTeacherDeleteButton key={user.id} lesson={lesson} user={user} />
            )}
        </>
    )
}

export const LessonGroupList = ({plan, lesson}) => {
    const groups = lesson?.groups || []
    return (
        <>
            {groups.map(
                (group, index) => <LessonGroupButton key={group.id} group={group} />
            )}
        </>
    )
}
export const LessonGroupListDeletable = ({plan, lesson}) => {
    const groups = lesson?.groups || []
    return (
        <>
            {groups.map(
                (group, index) => <LessonGroupDeleteButton key={group.id} lesson={lesson} group={group} />
            )}
        </>
    )
}

export const LessonFacilityList = ({plan, lesson}) => {
    const facilities = lesson?.facilities || []
    return (
        <>
            {facilities.map(
                (facility, index) => <LessonFacilityButton key={facility.id} facility={facility} />
            )}
        </>
    )
}


export const LessonFacilityListDeletable = ({plan, lesson}) => {
    const facilities = lesson?.facilities || []
    return (
        <>
            {facilities.map(
                (facility, index) => <LessonFacilityDeleteButton key={facility.id} lesson={lesson} facility={facility} />
            )}
        </>
    )
}

export const PlanLessonsTableRow = ({plan, lesson}) => {
    return (
        <tr>
            <td>{lesson?.order}</td>
            <td>{lesson?.name}</td>
            <td>{lesson?.type?.name}</td>
            <td>{lesson?.length||0}</td>
            <td>
                <LessonTeacherList plan={plan} lesson={lesson} />
            </td>
            <td>
                <LessonGroupList plan={plan} lesson={lesson} />
            </td>
            <td>
                <LessonFacilityList plan={plan} lesson={lesson} />
            </td>
            <td>
                <span className="btn btn-sm btn-outline-success">
                <Link id={"45b2df80-ae0f-11ed-9bd8-0242ac110002"} tag="event">24. 5. 8:00</Link>
                </span>
            </td>
        </tr>
    )
}

export const ThreeCheckBox = ({checked, onChange}) => {
    const [state, setState] = useState(checked)
    const setFalse = () => {
        setState(false)
        if (onChange) {
            onChange(false)
        }
    }
    const setTrue = () => {
        setState(true)
        if (onChange) {
            onChange(true)
        }
    }
    if (state === true) {
        return <span onClick={setFalse}><CheckSquare /></span>
    }
    if (state === false) {
        return <span onClick={setTrue} ><Square /></span>
    }
    return <span onClick={setFalse}><CheckSquareFill /></span>
}

export const PlanLessonsEditableTableRow = ({plan, lesson, onChange, checked}) => {
    const _onChange = (value) => {
        if (onChange) {
            onChange(lesson, value)
        }
    }
    const style = checked ? "table-active" : ""
    return (
        <tr className={style}>
            <td>
                <ThreeCheckBox checked={checked} onChange={_onChange}/>{" "}
                {lesson.id}
            </td>
            <td>{lesson.name}</td>
            <td>Přednáška</td>
            <td>4</td>

            <td>
                <LessonTeacherListDeletable plan={plan} lesson={lesson} />
            </td>
            <td>
                <LessonGroupListDeletable plan={plan} lesson={lesson} />
            </td>
            <td>
                <LessonFacilityListDeletable plan={plan} lesson={lesson} />
            </td>
            <td></td>
        </tr>
    )
}

export const PlanLessonsTableHeader = ({plan, children}) => {
    // console.log("PlanLessonsTable", plan)
    return (
        <thead>
            <tr>
                <th>Pořadí</th>
                <th>Název</th>
                <th>Typ</th>
                <th>Délka</th>
                <th>Vyučující</th>
                <th>Skupiny</th>
                <th>Prostory</th>
                <th>Termín</th>
            </tr>
        </thead>
    )
}

export const PlanLessonsTableTempate = ({plan, children}) => {
    // console.log("PlanLessonsTable", plan)
    return (
        <Table striped bordered>
            <thead>
                <tr>
                    <th>Pořadí</th>
                    <th>Název</th>
                    <th>Typ</th>
                    <th>Délka</th>
                    <th>Vyučující</th>
                    <th>Skupiny</th>
                    <th>Prostory</th>
                    <th>Termín</th>
                </tr>
            </thead>
            <tbody>
                {children}
            </tbody>
        </Table>
    )
}

export const PlanLessonsTable = ({plan, children}) => {
    let lessons = plan?.lessons || []
    lessons = [...lessons]
    lessons.sort((a, b) => (a?.order|| 0) - (b?.order||0))
    // console.log("lessons", lessons)
    // console.log("PlanLessonsTable", plan)
    return (
        <PlanLessonsTableTempate>
            {lessons.map(
                lesson => <PlanLessonsTableRow key={lesson.id} plan={plan} lesson={lesson} />
            )}
        </PlanLessonsTableTempate>
    )
}

export const LessonPredefinedTeacherButton = ({user, onClick}) => {
    const _onClick = () => {
        if (onClick) {
            onClick(user)
        }
    }
    return (
        <LessonTeacherButton user={user}>
            <LessonItemPlusButton onClick={_onClick} />{" "}
        </LessonTeacherButton>
    )
}

export const LessonPredefinedFacilityButton = ({facility, onClick}) => {
    const _onClick = () => {
        if (onClick) {
            onClick(facility)
        }
    }
    return (
        <LessonFacilityButton facility={facility}>
            <LessonItemPlusButton onClick={_onClick} />
        </LessonFacilityButton>
    )
}

export const LessonPredefinedGroupButton = ({group, onClick}) => {
    const _onClick = () => {
        if (onClick) {
            onClick(group)
        }
    }
    return (
        <LessonGroupButton group={group}>
            <LessonItemPlusButton onClick={_onClick} />
        </LessonGroupButton>
    )
}

/**
 * 
 * @param {Array} a array which going trought
 * @param {Function} f returns [key, value] for a particular array item
 * @returns dictionary of values
 */
const keyedmap = (a, f) => {
    let result = {}
    a.forEach(
        i => {
            let [key, value] = f(i)
            result[key] = value
        }
    )
    return result
}

/**
 * 
 * @param {Array} a array which going trought 
 * @param {Function} f returns [key, value] for a particular array item
 * @returns dictionary of arrays which represent subarrays of parameter a splitted by keys
 */
const pivotmap = (a, f) => {
    let result = {}
    a.forEach(
        i => {
            let [key, value] = f(i)
            if (key in result) {
                result[key].push(value)
            } else {
                result[key] = [value]
            }            
        }
    )
    return result
}
export const TeacherSelector = ({onTeacherSelect}) => {
    return (
        <InputGroup>
            <TextInput />
            <span className="btn btn-sm btn-outline-success"><Plus /></span>
        </InputGroup>
    )
}

export const UsersPicker = ({users, onClick}) => {
    return (
        <>             
            {users.map(
                user => <LessonPredefinedTeacherButton key={user.id} onClick={onClick} user={user} />
            )}
        </> 
    )
}

export const FacilitiesPicker = ({facilities, onClick}) => {
    return (
        <>             
            {facilities.map(
                facility => <LessonPredefinedFacilityButton key={facility.id} onClick={onClick} facility={facility} />
            )}
        </> 
    )
}

export const GroupsPicker = ({groups, onClick}) => {
    return (
        <>             
            {groups.map(
                group => <LessonPredefinedGroupButton key={group.id} onClick={onClick} group={group} />
            )}
        </> 
    )

}

export const LessonTeacherPredefinedButtons = ({plan, onTeacherAdd}) => {
    const lessons = plan?.lessons || []
    const users = lessons.flatMap(lesson => lesson.users)
    const [index, setIndex] = useState(keyedmap(users, user => [user.id, user]))
    // console.log(users)
    // console.log(Object.values(users))
    const onSelect = (item) => {
        setIndex(
            oldIndex => {
                const result = {...oldIndex}
                result[item.id] = item
                return result
            }
        )
    }
    return (
        <>
            <UsersPicker users={Object.values(index)} onClick={onTeacherAdd} />
            <hr />
            <UserSearch onSelect={onSelect}/>
        </>
        
    )
}

export const LessonGroupsPredefinedButtons = ({plan, onGroupAdd}) => {
    const lessons = plan?.lessons || []
    const groups = lessons.flatMap(lesson => lesson.groups)
    const [index, setIndex] = useState(keyedmap(groups, group => [group.id, group]))
    // console.log(users)
    // console.log(Object.values(users))
    const onSelect = (item) => {
        setIndex(
            oldIndex => {
                const result = {...oldIndex}
                result[item.id] = item
                return result
            }
        )
    }
    return (
        <>
            <GroupsPicker groups={Object.values(index)} onClick={onGroupAdd} />
            <hr />
            <GroupSearch onSelect={onSelect}/>
        </>
    )
}

export const LessonFacilitiesPredefinedButtons = ({plan, onFacilityAdd}) => {
    const lessons = plan?.lessons || []
    const facilities = lessons.flatMap(lesson => lesson.facilities)
    const [index, setIndex] = useState(keyedmap(facilities, facility => [facility.id, facility]))
    // console.log(users)
    // console.log(Object.values(users))
    const onSelect = (item) => {
        setIndex(
            oldIndex => {
                const result = {...oldIndex}
                result[item.id] = item
                return result
            }
        )
    }
    return (
        <>
            <FacilitiesPicker facilities={Object.values(index)} onClick={onFacilityAdd   } />
            <hr />
            <FacilitySearch onSelect={onSelect}/>
        </>
    )
}

export const PlanLessonsEditableTable = ({plan, children}) => {
    const dispatch = useDispatch()
    // const [lessons, setLessons] = useState(plan?.lessons || [])
    const lessons = plan?.lessons || []
    const [lessonsChecks, setChecks] = useState(
        keyedmap(lessons, lesson => [lesson.id, false]))
    
    
    const onLessonCheckChange = (lesson, state) => {
        const newChecks = {...lessonsChecks}
        newChecks[lesson.id] = state
        setChecks(newChecks)
        // console.log(newChecks)
    }

    const onTeacherAdd = (user) => {
        const checkedLessons = lessons.filter(lesson => lessonsChecks[lesson.id])
        const lessonsWOUser = checkedLessons.filter(lesson => !(lesson.users.find(u => u.id === user.id)))
        lessonsWOUser.forEach(
            lesson => dispatch(LessonAddTeacherAsyncAction({plan_id: plan.id, user_id: user.id, lesson_id: lesson.id}))
                .then(
                    CheckGQLError({
                        "ok": () => dispatch(MsgFlashAsyncAction({title: "Přiřazení vyučujícícho proběhlo úspěšně"})),
                        "fail": (json) => dispatch(MsgAddAsyncAction({title: "Přiřazení vyučujícícho se nepovedlo\n" + JSON.stringify(json)})),
                    })
                )
        )
    }

    const onGroupAdd = (group) => {
        const checkedLessons = lessons.filter(lesson => lessonsChecks[lesson.id])
        const lessonsWOGroup = checkedLessons.filter(lesson => !(lesson.groups.find(g => g.id === group.id)))
        lessonsWOGroup.forEach(
            lesson => dispatch(LessonAddGroupAsyncAction({plan_id: plan.id, group_id: group.id, lesson_id: lesson.id}))
                .then(
                    CheckGQLError({
                        "ok": () => dispatch(MsgFlashAsyncAction({title: "Přiřazení skupiny proběhlo úspěšně"})),
                        "fail": (json) => dispatch(MsgAddAsyncAction({title: "Přiřazení skupiny se nepovedlo\n" + JSON.stringify(json)})),
                    })
                )
        )
    }

    const onFacilityAdd = (facility) => {
        const checkedLessons = lessons.filter(lesson => lessonsChecks[lesson.id])
        const lessonsWOFacility = checkedLessons.filter(lesson => !(lesson.facilities.find(f => f.id === facility.id)))
        lessonsWOFacility.forEach(
            lesson => dispatch(LessonAddGroupAsyncAction({plan_id: plan.id, facility_id: facility.id, lesson_id: lesson.id}))
                .then(
                    CheckGQLError({
                        "ok": () => dispatch(MsgFlashAsyncAction({title: "Přiřazení prostor proběhlo úspěšně"})),
                        "fail": (json) => dispatch(MsgAddAsyncAction({title: "Přiřazení prostor se nepovedlo\n" + JSON.stringify(json)})),
                    })
                )
        )
    }

    return (
        <Table bordered hover>
            <PlanLessonsTableHeader />
            <tbody>
                {lessons.map(
                    lesson => <PlanLessonsEditableTableRow key={lesson.id} 
                        checked={lessonsChecks[lesson.id]} onChange={onLessonCheckChange}
                        plan={plan} lesson={lesson} />
                )}
                <tr className="table-warning">
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>

                <tr>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <th className="table-success">
                        Předdefinovaní vyučující
                    </th>
                    <th className="table-success">
                        Předdefinované skupiny 
                    </th>
                    <th className="table-success">
                        Předdefinované prostory
                    </th>
                    <td></td>
                </tr>
                <tr className="bg-light">
                    <th colSpan={2}>Předdefinované prvky</th>
                    <td></td>
                    <td></td>
                    <td>
                        <LessonTeacherPredefinedButtons plan={plan} onTeacherAdd={onTeacherAdd}/>
                    </td>
                    <td>
                        <LessonGroupsPredefinedButtons plan={plan} onGroupAdd={onGroupAdd}/>
                    </td>
                    <td>
                        <LessonFacilitiesPredefinedButtons plan={plan} onFacilityAdd={onFacilityAdd}/>
                    </td>
                    <td></td>
                </tr>
            </tbody>
        </Table>
    )
}
