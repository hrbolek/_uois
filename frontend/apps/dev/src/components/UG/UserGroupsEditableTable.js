import Form from "components/Form";
import { Plus, TrashFill } from "react-bootstrap-icons";
import Table from "react-bootstrap/Table";
import { UGSearchSmall } from "./UGSearch";
import { useMemo } from "react";


export const UserGroupsEditableTableRow = ({index, user, membership, actions}) => {
    const onInvalidateMembership = () => {
        const updatedMembership = {...membership, valid: false}
        // console.log("UserGroupsEditableTableRow", user)
        // console.log("UserGroupsEditableTableRow", updatedMembership)
        actions.onUserMembershipUpdateAsyncAction(user, updatedMembership)
        .then(json => {
            const msg = json?.data?.result.msg
            if (msg === "ok") {
                actions.onMsgFlashAsync({title: "Zneplatnění členství proběhlo úspěšně", variant: "success"})
            } else {
                actions.onMsgAddAsync({title: "Chyba " + JSON.stringify(json), variant: "danger"})
            }
        })
    }
    return (
        <tr>
            <td>{index}</td>
            <td>{membership?.group?.name}</td>
            <td>{membership?.startdate}</td>
            <td>{membership?.endtdate}</td>
            <td><Form.DeleteButton onClick={onInvalidateMembership}><TrashFill /></Form.DeleteButton> </td>
        </tr>
    )
}

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

export const UserGroupsEditableTableBody = ({user, actions, valid}) => {
    let membership = user?.membership || []
    membership = membership.filter(m => m.valid === valid)
    // console.log("UserGroupsEditableTableBody", valid)
    // console.log("UserGroupsEditableTableBody", membership)
    return (
        <tbody>
            {membership?.map(
                (m, index) => <UserGroupsEditableTableRow key={m.id} index={index+1} user={user} membership={m} actions={actions} />
            )}
            <tr>
                <th>Přidat do skupiny</th>
                <td><UserAddGroup user={user} actions={actions} /></td>
                <td></td>
                <td></td>
                <td></td>
            </tr>
        </tbody>
    )
}

export const UserGroupsEditableTableHeader = ({user, actions}) => {
    return (
        <thead>
            <tr>
                <th className="w-25">#</th>
                <th className="w-25">N</th>
                <th className="w-25">počátek</th>
                <th className="w-25">konec</th>
                <th className="w-25"></th>
            </tr>
        </thead>
    )
}

export const UserGroupsEditableTable = ({user, actions, valid}) => {
    return (
        <Table>
            <UserGroupsEditableTableHeader user={user} actions={actions}/>
            <UserGroupsEditableTableBody user={user} actions={actions} valid={valid}/>
        </Table>
    )
}