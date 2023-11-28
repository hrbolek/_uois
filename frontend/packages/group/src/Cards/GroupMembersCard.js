import { PeopleFill } from "react-bootstrap-icons"
import Card from "react-bootstrap/Card"
import { GroupMembers } from "../Components"

const UserLink = ({user}) => {
    return (
        <>
        {user.email}<br />
        </>
    )
}

export const GroupMembersCard = ({group}) => {
    return (
        <Card>
            <Card.Header><PeopleFill /> Členové</Card.Header>
            <Card.Body>
                {group?.memberships?.map(
                    m => <UserLink key={m.id} user={m.user} />
                )}
                <GroupMembers group={group} />
            </Card.Body>
        </Card>
    )
}