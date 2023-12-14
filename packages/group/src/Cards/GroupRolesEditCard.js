import { PeopleFill } from "react-bootstrap-icons"
import Card from "react-bootstrap/Card"
import { GroupMembersEdit, GroupRolesEdit } from "../Components"
import { Col, Row } from "react-bootstrap"

const UserLink = ({user}) => {
    return (
        <>
        {user.email}<br />
        </>
    )
}

export const GroupRolesEditCard = ({group}) => {
    return (
        <Card>
            <Card.Header><PeopleFill /> Členové</Card.Header>
            <Card.Body>
                <Row>
                    <Col md={6}>
                        <GroupRolesEdit group={group} onlyValid={true}/>
                    </Col>
                    <Col md={6}>
                        <GroupRolesEdit group={group} onlyInvalid={true}/>
                    </Col>
                </Row>
                
            </Card.Body>
        </Card>
    )
}