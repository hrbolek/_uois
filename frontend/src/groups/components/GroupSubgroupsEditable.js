import { useCallback } from 'react'

import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { UserSmall } from "users/components/links"
import { GroupSmall } from "groups/components/links"
import { GroupMedium } from "groups/components/GroupMedium"

const Subgroup = (props) => {
    return (
        <Col><GroupMedium group={props.group}/></Col>
    )
}

const SubgroupTableRow = (props) => {
    const { group, actions } = props
    
    const setInvalid = useCallback( () => actions.updateGroupInTreeAsync({...group, valid: false}), [group])
    const setValid = useCallback( () => actions.updateGroupInTreeAsync({...group, valid: true}), [group])

    const changeButton = (group.valid === 'true' | group.valid) ? (
            <button className="btn btn-sm btn-success" onClick={setInvalid}><i className="bi bi-hand-thumbs-up-fill"></i></button>
        ) : (
            <button className="btn btn-sm btn-danger" onClick={setValid}><i className="bi bi-hand-thumbs-down-fill"></i></button>
        )
    return (
        <tr>
            <td>{props.No}</td>
            <td><GroupSmall group={group} /></td>
            <td>{group.grouptype.name}</td>
            <td>{(group.valid === 'true' | group.valid) ? "Ano" : "Ne"}</td>
            <td>
                {changeButton}
            </td>
        </tr>
    )

}

export const GroupSubgroupsEditable = (props) => {
    const { group, grouptype, valid, title, actions } = props
    let subgroups = group.subgroups
    
    //console.log('GroupSubgroupsEditable', props.group)
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <GroupSmall group={group} /> {title||""} (součásti)
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <table className="table table-striped table-sm">
                    <thead>
                        <tr>
                            <th>#</th><th>Název</th><th>Typ</th><th>Platné</th><th>Nástroje</th>
                        </tr>
                    </thead>
                    <tbody>
                        {subgroups.map((sg, index) => <SubgroupTableRow key={sg.id} No={index+1} group={sg} actions={actions} />)}
                    </tbody>
                </table>
            </Card.Body>
        </Card>
    )
}