import Card from "react-bootstrap/Card"
import { EyeFill, Plus, PlusSquare} from "react-bootstrap-icons"
import { TextInput } from "components/Form/TextInput"
import { UserRolesEditTable } from "./UserRolesEditTable"
import { UGSearchSmall } from "./UGSearch"
import { useMemo } from "react"
import { Col, Row } from "react-bootstrap"
import { UserGroupsTable } from "./UserGroupsTable"
import { UserGroupsEditableTable } from "./UserGroupsEditableTable"
import Form from "components/Form"



export const UserAddGroup = ({user, actions}) => {
    const onAddGroup = (group) => {
        actions.onUserMembershipAdd(user, group)
        .then(json => {
            const msg = json?.data?.result?.msg
            if (msg === "ok") {
                actions.onMsgFlashAsync({title: "Úspěch", variant: "success"})
            } else {
                actions.onMsgAdd({title: "Neúspěch", variant: "danger"})
            }
        })
    }
    const GroupHintComponent = useMemo( 
        () =>({group}) => {
            return (
                <> <span className="btn btn-sm btn-outline-primary" onClick={()=>onAddGroup(group)}><Plus />{group.name}</span></>
            )
    })

    return (
        <UGSearchSmall groups={true} GroupComponent={GroupHintComponent} />
    )
}

export const UserEditCard = ({user, actions}) => {
    const onChangeName = (value) => {
        actions.onUserUpdateAsync({...user, name: value})
        .then(json => {
            const msg = json?.data?.result?.msg
            if (msg === "ok") {
                actions.onMsgFlashAsync({title: "Jméno změněno úspěšně", variant: "success"})
            } else {
                actions.onMsgAddAsync({title: "Chyba " + JSON.stringify(json), variant: "danger"})
            }
        })
    }
    const onChangeSurname = (value) => {
        actions.onUserUpdateAsync({...user, surname: value})
        .then(json => {
            const msg = json?.data?.result?.msg
            if (msg === "ok") {
                actions.onMsgFlashAsync({title: "Příjmení změněno úspěšně", variant: "success"})
            } else {
                actions.onMsgAddAsync({title: "Chyba " + JSON.stringify(json), variant: "danger"})
            }
        })
    }
    const onChangeEmail = (value) => {
        actions.onUserUpdateAsync({...user, email: value})
        .then(json => {
            const msg = json?.data?.result?.msg
            if (msg === "ok") {
                actions.onMsgFlashAsync({title: "Email změněn úspěšně", variant: "success"})
            } else {
                actions.onMsgAddAsync({title: "Chyba " + JSON.stringify(json), variant: "danger"})
            }
        })
    }
    return (
        <Card>
            <Card.Header>
                {user.name} {user.surname} ({user.email}) <Form.Link tag={"user"} id={user.id}><EyeFill /></Form.Link>
            </Card.Header>
            <Card.Body>
                {/* <EditableText value={user.name} /> <br />
                <EditableText value={user.surname} /><br />
                <EditableText value={user.email} /><br /> */}
                <h3>Základní údaje</h3>
                Name: <TextInput value={user.name} onChange={onChangeName}/> <br />
                Surname: <TextInput value={user.surname}  onChange={onChangeSurname}/> <br />
                Email: <TextInput value={user.email}  onChange={onChangeEmail}/> <br />
            </Card.Body>
            <Card.Body>
                <h3>Členství</h3>
                <hr/>
                <UserGroupsEditableTable user={user} actions={actions} valid={true}/>
                
                <h3>Role</h3>
                <hr/>
                <UserRolesEditTable user={user} actions={actions} />
            </Card.Body>
        </Card>
    )
}