import { PeopleFill } from "react-bootstrap-icons"
import Card from "react-bootstrap/Card"
import { GroupMembersEdit } from "../Components"
import { Col, Row } from "react-bootstrap"

const UserLink = ({user}) => {
    return (
        <>
        {user.email}<br />
        </>
    )
}

export const GroupMembersEditCard = ({group}) => {
    return (
        <Card>
            <Card.Header><PeopleFill /> Členové</Card.Header>
            <Card.Body>
                <Row>
                    <Col md={6}>
                        <GroupMembersEdit group={group} onlyValid={true}/>
                    </Col>
                    <Col md={6}>
                        <GroupMembersEdit group={group} onlyInvalid={true}/>
                    </Col>
                </Row>
                
            </Card.Body>
        </Card>
    )
}