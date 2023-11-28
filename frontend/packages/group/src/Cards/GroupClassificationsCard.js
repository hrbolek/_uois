import { PeopleFill } from "react-bootstrap-icons"
import Card from "react-bootstrap/Card"
import { GroupClassifications, GroupMembers } from "../Components"

const UserLink = ({user}) => {
    return (
        <>
        {user.email}<br />
        </>
    )
}

export const GroupClassificationsCard = ({group}) => {
    return (
        <Card>
            <Card.Header><PeopleFill /> Klasifikace</Card.Header>
            <Card.Body>
                <GroupClassifications group={group} />
            </Card.Body>
        </Card>
    )
}