import { FacilitySearch } from "@uoisfrontend/facility"
import { GroupSearch } from "@uoisfrontend/group"
import { UserSearch } from "@uoisfrontend/user"
import { useState } from "react"
import { ArrowDown, ArrowUp, CheckLg, PlusLg, TrashFill, ArrowsExpand } from "react-bootstrap-icons"
import Table from "react-bootstrap/Table"
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import { LessonAddTeacherAsyncAction } from "../Actions/LessonAddTeacherAsyncAction"
import { useDispatch } from "react-redux"
import { CheckGQLError, DeleteButton, Link, TextInput } from "@uoisfrontend/shared"
import { LessonRemoveTeacherAsyncAction } from "../Actions/LessonRemoveTeacherAsyncAction"
import { MsgAddAsyncAction, MsgFlashAsyncAction } from "reducers/msgsreducers"
import { PlanLessonInsertAsyncAction } from "../Actions/PlanLessonInsertAsyncAction"
import { PlanLessonDeleteAsyncAction } from "../Actions/PlanLessonDeleteAsyncAction"
import { PlanAddLessonButton } from "./PlanAddLessonButton"
import { AddRemoveButton } from "./AddRemoveButton"
import { LessonAddRemoveTeacherButton } from "./LessonAddRemoveTeacherButton"
import { LessonNameInputbox } from "./LessonNameInputbox"
import { LessonTypeSelect } from "./LessonTypeSelect"

export const LessonItemButton = ({id, name, linktag, children}) => (
    <span>
        <span key={id} className="btn btn-sm btn-outline-success">
            <Link id={id} tag={linktag}>{name}</Link>
        </span>
        {children}
    </span>
)

export const UserButton = ({user}) => 
    <LessonItemButton id={user.id} linktag={"user"} name={user.name + " " + user.surname} />

export const GroupButton = ({group}) => 
    <LessonItemButton id={group.id} linktag={"group"} name={group.name} />

export const FacilityButton = ({facility}) => 
    <LessonItemButton id={facility.id} linktag={"facility"} name={facility.name} />

export const PlanPivotEditableTableHead = ({plan, users, groups, facilities, onSelectUser, onSelectGroup, onSelectFacility}) => {
    return (
        <thead>
            <tr>
                <th colSpan={4} className="table-success">
                    <h3>Programování 1. semester</h3>
                </th>
                <th></th>
                <th className="table-warning"></th>
                <th colSpan={users.length}><UserSearch onSelect={onSelectUser}/></th>
                <th className="table-warning"></th>
                <th colSpan={groups.length}><GroupSearch onSelect={onSelectGroup}/></th>
                <th className="table-warning"></th>
                <th colSpan={facilities.length}><FacilitySearch onSelect={onSelectFacility}/></th>
                <th></th>
            </tr>

            <tr>
                <th>#</th>
                <th>Téma</th>
                <th>Typ</th>
                <th>Délka</th>
                <th></th>
                <th className="table-warning"></th>
                {users.map(
                    user => <th key={user.id} style={{"writingMode": "vertical-rl", "textOrientation": "mixed"}}>
                        <UserButton user={user} />
                    </th>
                )}
                <th className="table-warning"></th>
                {groups.map(
                    group => <th key={group.id} style={{"writingMode": "vertical-rl", "textOrientation": "mixed"}}>
                        <GroupButton group={group} />
                    </th>
                )}
                <th className="table-warning"></th>
                {facilities.map(
                    facility => <th key={facility.id} style={{"writingMode": "vertical-rl", "textOrientation": "mixed"}}>
                        <FacilityButton facility={facility} />
                    </th>
                )}
                <th>Termín</th>
            </tr>
        </thead>
    )
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

// export const LessonAddRemoveTeacherButton = ({plan, lesson, user}) => {
//     const present = lesson.users.find(u => u.id === user.id)? true: false
//     const dispatch = useDispatch()
//     const onChangeValue = (value) => {
//         if (value) {
//             dispatch(LessonAddTeacherAsyncAction({plan_id: plan.id, lesson_id: lesson.id, user_id: user.id}))
//             .then(
//                 CheckGQLError({
//                     "ok": () => dispatch(MsgFlashAsyncAction({title: "Přiřazení vyučujícícho proběhlo úspěšně"})),
//                     "fail": (json) => dispatch(MsgAddAsyncAction({title: "Přiřazení vyučujícícho se nepovedlo\n" + JSON.stringify(json)})),
//                 })
//             )
//         } else {
//             dispatch(LessonRemoveTeacherAsyncAction({plan_id: plan.id, lesson_id: lesson.id, user_id: user.id}))
//             .then(
//                 CheckGQLError({
//                     "ok": () => dispatch(MsgFlashAsyncAction({title: "Odebrání vyučujícícho proběhlo úspěšně"})),
//                     "fail": (json) => dispatch(MsgAddAsyncAction({title: "Odebrání vyučujícícho se nepovedlo\n" + JSON.stringify(json)})),
//                 })
//             )

//         }
//     }
//     return <AddRemoveButton state={present} onChangeValue={onChangeValue}/>
// }

export const UsersSegment = ({plan, lesson, users}) => {
    return (
        <>
            {users.map(
                user => <td key={user.id}>
                    <LessonAddRemoveTeacherButton plan={plan} lesson={lesson} user={user} />
                </td>
            )}
        </>
    )
}

export const LessonAddRemoveGroupButton = ({plan, lesson, group}) => {
    const present = lesson.groups.find(g => g.id === group.id)? true: false
    return <AddRemoveButton state={present} />
}

export const GroupsSegment = ({plan, lesson, groups}) => {
    return (
        <>
            {groups.map(
                    group => <td key={group.id}>
                        {/* {groupIndex[group.id]?"t":"f"} */}                       
                        <LessonAddRemoveGroupButton plan={plan} lesson={lesson} group={group} />
                    </td>
                )}
        </>
    )
}
// export const AddRemoveButton = ({state, onChangeValue}) => {
//     const [_state, setState] = useState(state)
//     const set0 = () => setState(0)
//     const settrueCall = () => {
//         setState(true)
//         if (onChangeValue) {
//             onChangeValue(true)
//         }
//     }
//     const setfalse = () => setState(false)
//     const setfalseCall = () => {
//         setState(false)
//         if (onChangeValue) {
//             onChangeValue(false)
//         }
//     }
//     switch(_state) {
//         case true:
//             return (
//                 <span className="btn btn-sm btn-outline-success" onClick={setfalseCall}><CheckLg /></span>
//             )  
//         case false:
//             return (
//                 <span className="btn btn-sm btn-outline-light" onClick={set0}><PlusLg /></span>
//             )
//         default:
//             return (
//                 <>
//                 <span className="btn btn-sm btn-outline-light" onClick={setfalse}><PlusLg /></span>
//                 <span className="btn btn-sm btn-outline-danger" onClick={settrueCall}><PlusLg /></span>
//                 </>
//             )            
//       } 
// }

export const LessonAddRemoveFacilityButton = ({plan, lesson, facility}) => {
    const present = lesson.facilities.find(f => f.id === facility.id)? true: false
    return <AddRemoveButton state={present} />
}

export const FacilitiesSegment = ({plan, lesson, facilitites}) => {
    return (
        <>
            {facilitites.map(
                    facility => <td key={facility.id}>
                        <LessonAddRemoveFacilityButton plan={plan} lesson={lesson} facility={facility} />
                    </td>
                )}
        </>
    )
}

export const PlanPivotEditableTableRow = ({plan, lesson, users, groups, facilities}) => {
    
    return (
        <tr>
            <td>
                <LessonDeleteButton lesson={lesson} plan={plan}/>
                <span className="btn btn-sm btn-outline-success"><ArrowUp /></span>
                <span className="btn btn-sm btn-outline-success"><ArrowDown /></span>
                <span className="btn btn-sm btn-outline-success"><ArrowsExpand /></span>
            </td>
            <td>
                <LessonNameInputbox lesson={lesson} plan={plan}/>
            </td>
            <td>
                <LessonTypeSelect lesson={lesson} plan={plan}/> 
            </td>
            <td>4</td>
            <td></td>
            <td className="table-warning"></td>
            <UsersSegment plan={plan} lesson={lesson} users={users} />
            <td className="table-warning"></td>
            <GroupsSegment plan={plan} lesson={lesson} groups={groups} />
            <td className="table-warning"></td>
            <FacilitiesSegment plan={plan} lesson={lesson} facilitites={facilities} />
            <td></td>
        </tr>
    )
}

// export const PlanAddLessonButton = ({plan, name="Nová lekce", lessontype_id="e2b7cbf6-95e1-11ed-a1eb-0242ac120002"}) => {
//     const dispatch = useDispatch()
//     const onClick = () => {
//         dispatch(PlanLessonInsertAsyncAction({name, lessontype_id, plan_id: plan.id}))
//         .then(
//             CheckGQLError({
//                 "ok": () => dispatch(MsgFlashAsyncAction({title: "Přidání lekce úspěšné"})),
//                 "fail": (json) => dispatch(MsgAddAsyncAction({title: "Přidání lekce se nepovedlo\n" + JSON.stringify(json)})),
//             })
//         )
//     }
//     return (
//         <button className="btn form-control btn-outline-success" onClick={onClick}><PlusLg /> Přidat lekci</button>
//     )
// }

export const PlanAddLessonsFromAccreditationButton = ({plan}) => {
    const dispatch = useDispatch()
    const onClick = () => {
    //     dispatch(PlanLessonInsertAsyncAction({name, lessontype_id, plan_id: plan.id}))
    //     .then(
    //         CheckGQLError({
    //             "ok": () => dispatch(MsgFlashAsyncAction({title: "Přidání lekce úspěšné"})),
    //             "fail": (json) => dispatch(MsgAddAsyncAction({title: "Přidání lekce se nepovedlo\n" + JSON.stringify(json)})),
    //         })
    //     )
    }
    if (plan?.semester) {
        return (
            <button className="btn form-control btn-outline-success" onClick={onClick}><PlusLg /> Přidat lekce z akreditace</button>
        )
    
    } else {
        return <></>
    }
}

export const LessonDeleteButton = ({lesson, plan}) => {
    const dispatch = useDispatch()
    const onClick = () => {
        console.log("LessonDeleteButton.onClick", plan)
        console.log("LessonDeleteButton.onClick", lesson)
        dispatch(PlanLessonDeleteAsyncAction({plan_id: plan.id, lesson_id: lesson.id, lastchange: lesson.lastchange}))
        .then(
            CheckGQLError({
                "ok": () => dispatch(MsgFlashAsyncAction({title: "Smazání lekce úspěšné"})),
                "error": (json) => dispatch(MsgAddAsyncAction({title: "Smazání lekce se nepovedlo\n" + JSON.stringify(json)})),
            })
        )
    }
    return (
        <DeleteButton onClick={onClick}><TrashFill /></DeleteButton>
    )
}

export const PlanPivotEditableTableSumRow = ({lessons, users, groups, facilities}) => {   
    const userSums = pivotmap(users, user => {
        const results = lessons.map(l => {
            if (l.users.find(_u => _u.id === user.id)) {
                return 4
            } else {
                return 0
            }
        })
        return [user.id, results.reduce((a,b) => a+b)]
    })
    return (
        <tr>
            <td colSpan={2}>
                
            </td>
            <td></td>
            <td></td>
            <td></td>
            
            <td className="table-warning"></td>
            {users.map(
                u => <td key={u.id}>{userSums[u.id]}</td>
            )}
            <td className="table-warning"></td>
            {groups.map(
                g => <td key={g.id}></td>
            )}
            <td className="table-warning"></td>
            {facilities.map(
                f => <td key={f.id}></td>
            )}
            <td></td>
        </tr>
    )

}
export const PlanPivotEditableTableFoot = ({plan, users, groups, facilities}) => {   
    return (
        <tfoot>
        <tr>           
            <td colSpan={5}>
                <PlanAddLessonButton plan={plan} />
                <hr />
                <PlanAddLessonsFromAccreditationButton plan={plan} />
            </td>
            
            <td className="table-warning"></td>
            {users.map(
                u => <td key={u.id}></td>
            )}
            <td className="table-warning"></td>
            {groups.map(
                g => <td key={g.id}></td>
            )}
            <td className="table-warning"></td>
            {facilities.map(
                f => <td key={f.id}></td>
            )}
            <td></td>
        </tr>
        <PlanPivotEditableTableSumRow lessons={plan.lessons} users={users} groups={groups} facilities={facilities} />
        <tr>
            <td colSpan={1}></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td className="table-warning"></td>
            {users.map(
                u => <td key={u.id}></td>
            )}
            <td className="table-warning"></td>
            {groups.map(
                g => <td key={g.id}></td>
            )}
            <td className="table-warning"></td>
            {facilities.map(
                f => <td key={f.id}></td>
            )}
            <td></td>
        </tr>
        </tfoot>
    )
}

const makeUnique = (a) => {
    const result = {}
    a.forEach(i => {
        const id = i.id
        if (!(id in result)) {
            result[id] = i
        }
    })
    return Object.values(result)
}

export const PlanPivotEditableTable = ({plan}) => {
    console.log("PlanPivotEditableTable.plan", plan)
    const lessons = plan?.lessons || []
    const users = makeUnique(lessons.flatMap(
        lesson => lesson?.users || []
    ))
    const groups = makeUnique(lessons.flatMap(
        lesson => lesson?.groups || []
    ))
    const facilities = makeUnique(lessons.flatMap(
        lesson => lesson?.facilities || []
    ))
    const [_users, setUsers] = useState(users)
    const [_groups, setGroups] = useState(groups)
    const [_facilities, setFacilities] = useState(facilities)

    const onSelectUser = (user) => {
        if (_users.find(u => u.id === user.id)) {

        } else {
            setUsers([..._users, user])
        }
    }
    const onSelectGroup = (group) => {
        if (_groups.find(g => g.id === group.id)) {

        } else {
            setGroups([..._groups, group])
        }
    }
    const onSelectFacility = (facility) => {
        if (_facilities.find(f => f.id === facility.id)) {

        } else {
            setFacilities([..._facilities, facility])
        }
    }

    console.log(users)
    return (
        <Table striped hover bordered>
            <PlanPivotEditableTableHead 
                plan={plan} users={_users} groups={_groups} facilities={_facilities} 
                onSelectUser={onSelectUser}
                onSelectGroup={onSelectGroup}
                onSelectFacility={onSelectFacility}
            />
            <tbody>
                {lessons.map(
                    lesson => <PlanPivotEditableTableRow key={lesson.id} plan={plan} lesson={lesson} users={_users} groups={_groups} facilities={_facilities} />
                )}
            </tbody>
            <PlanPivotEditableTableFoot plan={plan} users={_users} groups={_groups} facilities={_facilities} />
        </Table>
    )
}