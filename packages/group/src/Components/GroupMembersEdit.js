import { TrashFill } from "react-bootstrap-icons"
import { DeleteButton, Link } from "@uoisfrontend/shared"
import { GroupMember } from "./GroupMembers"
import Table from "react-bootstrap/Table"
import { GroupMembershipSetStartPicker } from "./GroupMembershipStartPicker"
import { GroupMembershipEndPicker } from "./GroupMembershipEndPicker"
import { GroupMemberValidButton } from "./GroupMemberValidButton"

export const GroupEditMembers_ = ({group, children}) => {
    let memberships = group?.memberships || []
    memberships = memberships.filter(
        (m) => m.valid
    )

    return (
        <>
            {memberships.map(
                (m, index) => <GroupMember key={m.id} group={group} membership={m}><DeleteButton><TrashFill /></DeleteButton> </GroupMember>
            )}
            {children}
        </>
    )
}

const UserLink = ({user}) => {
    return (
        <Link id={user.id} tag="user">{user.name} {user.surname}</Link>
    )
}

export const GroupEditMembersTableBody = ({group, members, children}) => {
    const grouped = null
    return (
        <tbody>
            {members.map(
                (m, index) => (<tr key={m.id}>
                    <td>{index+1}</td>
                    <td><UserLink user={m?.user} /></td>
                    <td>
                        <GroupMembershipSetStartPicker group={group} membership={m}/>
                    </td>
                    <td>
                        <GroupMembershipEndPicker group={group} membership={m} />
                    </td>
                    <td>
                        <GroupMemberValidButton group={group} membership={m}/>
                    </td>
                </tr>)
            )}
        </tbody>
    )
}

export const GroupMembersEdit = ({group, children, onlyValid=true, onlyInvalid=false}) => {
    let memberships = group?.memberships || []
    let tableHeader = null
    if (onlyInvalid === true) {       
        memberships = memberships.filter(
            (m) => m.valid === false
        )
        console.log("GroupEditMembers.invalid", memberships)

        tableHeader = "Bývalí členové"
    } else {
        if (onlyValid === true) {
            memberships = memberships.filter(
                (m) => m.valid === true
            )
        }
        console.log("GroupEditMembers.valid", memberships)
        tableHeader = "Aktivní členové"
    }

    return (
        <Table striped bordered size="sm">
            <thead>
                <tr>
                    <th className="table-success" colSpan={5}>{tableHeader}</th>
                </tr>
                <tr>
                    <th>#</th>
                    <th className="w-25">User</th>
                    <th className="w-25">start</th>
                    <th className="w-25">end</th>
                    <th className="w-25"></th>
                </tr>
            </thead>
            <GroupEditMembersTableBody group={group} members={memberships} />
        </Table>
    )
}