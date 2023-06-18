import Table from "react-bootstrap/Table"
import { CheckGQLError, Link, MsgAddAction, MsgFlashAction, useFreshItem } from "@uoisfrontend/shared"
import { UserClassificationFetchAsyncAction, UserClassificationInsertAsyncAction } from "@uoisfrontend/user"
import { ProgramFetchAsyncAction } from "../../../program/src/Actions/ProgramFetchAsyncAction"


import { useState } from "react"
import { PlusLg, CheckLg } from "react-bootstrap-icons"
import { useDispatch } from "react-redux"

// variant="btn-outline-succcess" 
export const AddClassificationType = ({variant="outline-success", classificationType, onClick}) => {
    const onClick_ = () => {
        if (onClick) {
            onClick(classificationType)
        }
    }
    return (
        <button className={"btn btn-sm btn-" + variant} onClick={onClick_}>{classificationType.name}</button>
    )
}
const  classificationTypes_ = [
    {"id": "5fae9dd8-b095-11ed-9bd8-0242ac110002" , "name": "A", "name_en": "A"},
    {"id": "5faea134-b095-11ed-9bd8-0242ac110002" , "name": "B", "name_en": "B"},
    {"id": "5faea21a-b095-11ed-9bd8-0242ac110002" , "name": "C", "name_en": "C"},
    {"id": "5faea2d8-b095-11ed-9bd8-0242ac110002" , "name": "D", "name_en": "D"},
    {"id": "5faea332-b095-11ed-9bd8-0242ac110002" , "name": "E", "name_en": "E"},
    {"id": "5faea396-b095-11ed-9bd8-0242ac110002" , "name": "F", "name_en": "F"}]

export const ChangeButton = ({value, classificationTypes=classificationTypes_, onChangeValue }) => {
    const [_state, setState] = useState(false)
    const settrue = () => setState(true)
    const onClick = (classificationType) => {
        if (onChangeValue) {
            onChangeValue(classificationType)
        }
    }
    const setfalse = () => setState(false)
    const setfalseCall = () => {
        setState(false)
        if (onChangeValue) {
            onChangeValue(false)
        }
    }
    if (_state === false) {
        return (
            <>
            {classificationTypes.map(
                classificationType => ((classificationType.id === value) ?
                    <AddClassificationType key={classificationType.id} variant="danger" classificationType={classificationType} onClick={settrue} />:
                    ""
            ))}
            </>
        )
    } else {
        return (
            <>
            {classificationTypes.map(
                classificationType => ((classificationType.id === value) ?
                    <AddClassificationType key={classificationType.id} variant="danger" classificationType={classificationType} onClick={setfalse} />:
                    <AddClassificationType key={classificationType.id} variant="outline-success" classificationType={classificationType} onClick={onClick} />
            ))}
            {/* {classificationTypes.map(
                classificationType => <AddClassificationType key={classificationType.id} variant="danger" classificationType={classificationType} onClick={onClick} />
            )} */}
            </>
        )
    }
    
}
    

export const AddButton = ({ classificationTypes=classificationTypes_, onChangeValue }) => {
    const [_state, setState] = useState(false)
    const set0 = () => setState(0)
    const onClick = (classificationType) => {
        if (onChangeValue) {
            onChangeValue(classificationType)
        }
    }
    const setfalse = () => setState(false)
    const setfalseCall = () => {
        setState(false)
        if (onChangeValue) {
            onChangeValue(false)
        }
    }
    switch(_state) {
        case true:
            return (
                <span className="btn btn-sm btn-outline-success" onClick={setfalseCall}><CheckLg /></span>
            )  
        case false:
            return (
                <span className="btn btn-sm btn-outline-light" onClick={set0}><PlusLg /></span>
            )
        default:
            return (
                <>
                <span className="btn btn-sm btn-outline-primary" onClick={setfalse}><PlusLg /></span>
                {classificationTypes.map(classificationType => <AddClassificationType key={classificationType.id} classificationType={classificationType} onClick={onClick} />

                    
                )}
                </>
            )            
      } 
}
export const AddClassificationButton = ({semester, user, classificationTypes=classificationTypes_, order}) => {
    const dispatch = useDispatch()
    const onChangeValue = (value) => {
        dispatch(UserClassificationInsertAsyncAction({user_id: user.id, semester_id: semester.id, level_id: value, order: order}))
        .then(
            CheckGQLError({
                "ok": () => dispatch(MsgFlashAction({title: "Známka vložena úspěšně"})),
                "fail": (json) => dispatch(MsgAddAction({title: "Známku se nepodařilo vložit" + JSON.stringify(json)})),
            })
        )
    }
    return (
        <AddButton classificationTypes={classificationTypes} onChangeValue={onChangeValue} />
    )
}

export const ChangeClassificationButton = ({classification}) => {
    const dispatch = useDispatch()
    const onChangeValue = (value) => {
        //dispatch(UserCla)
    }
    return (
        <ChangeButton value={classification.level.id} onChangeValue={onChangeValue}/>
    )
}

export const UserClassifications = ({semesters, user}) => {
    // console.log("UserClassifications", user)
    const [freshUser, promise] = useFreshItem(user, UserClassificationFetchAsyncAction)
    const onChangeValue = (value) => {

    }
    return (
        <tr>
            <td>
                
            </td>
            <td>
                <Link tag="user" id={user.id}>{user.name} {user.surname}</Link>
            </td>
            {semesters.map(semester =>
                <td key={semester[1]}>
                    <AddClassificationButton semester={semester} user={user} order={1}/>
                    <AddButton />
                    <ChangeButton value={"5faea2d8-b095-11ed-9bd8-0242ac110002"}/>
                </td>
            )}

            <td>
            </td>
            <td>
            </td>
        
        
        </tr>
    )
}

export const GroupClassificationsTableHeader = ({semesters}) => {
    return (
        <tr>
            <th></th>
            <th></th>
            {semesters.map(semester =>
                <th key={semester[1]} style={{writingMode: "vertical-rl", "textOrientation": "mixed"}}>{semester[0]}</th>
            )}
            <th></th>
            <th></th>
        </tr>
    )
}

export const GroupClassifications = ({group}) => {
    const members = group?.memberships?.map(
        m => m.user
    ) || []
    const [freshProgram] = useFreshItem({id: "2766fc9a-b095-11ed-9bd8-0242ac110002"}, ProgramFetchAsyncAction)
    const subjects = freshProgram?.subjects || []
    const semesters = subjects.flatMap(subject => 
            subject?.semesters.map(semester =>
                ([subject.name + " " + semester.order, semester.id])
            )
        )
    console.log("GroupClassifications.semesters", semesters)
    return (
        <Table striped size="sm" bordered>
            <thead>
                <GroupClassificationsTableHeader semesters={semesters} />
                {/* <tr>
                    <th>#</th>
                    <th>#</th>
                    <th>#</th>
                    <th>#</th>
                    <th>#</th>
                    
                </tr> */}
            </thead>
            <tbody>
                {members.map(
                    u => <UserClassifications key={u.id} user={u} semesters={semesters}/>
                )}
            </tbody>
        </Table>
    )
}
