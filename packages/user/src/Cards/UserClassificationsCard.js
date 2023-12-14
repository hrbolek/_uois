import { Calendar3Fill } from "react-bootstrap-icons"
import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"
import { UserAddEventButton, UserEvents } from "../Components"

export const UserClassificationsCard = ({user}) => {
    return (
        <Card>
            <Card.Header>
               <Calendar3Fill /> Role {user.email}
            </Card.Header>
            <Card.Body>
                Role                
            </Card.Body>
        </Card>
    )
}