import { Calendar3Fill } from "react-bootstrap-icons"
import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"
import { UserAddEventButton, UserEvents } from "../Components"

export const UserGroupsCard = ({user}) => {
    return (
        <Card>
            <Card.Header>
               <Calendar3Fill /> Groups {user.email}
            </Card.Header>
            <Card.Body>
                Groups                
            </Card.Body>
        </Card>
    )
}