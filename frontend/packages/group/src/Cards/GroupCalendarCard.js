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

export const GroupCalendarCard = ({group}) => {
    return (
        <Card>
            <Card.Header><PeopleFill /> Kalendář</Card.Header>
            <Card.Body>
                
            </Card.Body>
        </Card>
    )
}