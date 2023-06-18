import Card from "react-bootstrap/Card"
import Form from "react-bootstrap/Form"
import InputGroup from "react-bootstrap/InputGroup"

import { EnvelopeAtFill, EnvelopeFill, EyeFill, PencilFill, PencilSquare, PersonFill, PlusLg } from "react-bootstrap-icons"
import { UserRoles } from "./UserRoles"
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import { UserGroups } from "./UserGroups"
import { Link } from "@uoisfrontend/shared"
import { UserEvent, UserEvents } from "./UserEvents"
import { UserClassification, UserClassificationEditable, UserClassificationsTable, UserClassificationsTableEditable } from "./UserClassification"
import { UserAttributesEditable } from "./UserAttributesEditable"

const UserEmail = ({user, subject="Info", body="Dobr%C3%BD%20den%2C "}) => {
    const hrefValue = `mailto:${user.email}?subject=${subject}&body=${body}`
    // mailto:some@where.com?subject=Info&body=Dobr%C3%BD%20den%2C 
    return (
        <a href={hrefValue}><EnvelopeFill /></a>
    )
}

export const UserCardEditable = ({user}) => {
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <PersonFill /> {user.name} {user.surname}  <UserEmail user={user} />
                    </Col>
                    <Col>
                        <UserRoles user={user} />
                    </Col>
                    <Col>
                        <UserGroups user={user} />
                    </Col>
                    <Col>
                        <div className="d-flex justify-content-end">
                            <Link id={user.id} tag="user"><EyeFill /> </Link>
                        </div>
                    </Col>
                </Row>
            </Card.Header>
            <Card.Body>
                <h3>Atributy</h3>
                <UserAttributesEditable user={user} />
                <hr />
                <UserClassification user={user} />
                <UserClassificationEditable user={user} />
            </Card.Body>
            <Card.Body>
                <UserEvents user={user} />
                {/* <Row>
                    <Col md={1}>
                        <Form.Label column={"lg"} htmlFor="basic-url">Role</Form.Label>
                    </Col>
                    <Col md={1}>
                        <UserRoles user={user} />
                    </Col>
                    <Col md={1}>
                        <InputGroup className="mb-3">
                            <InputGroup.Text id="basic-addon3">
                            <PlusLg /> Nová role
                            </InputGroup.Text>
                        </InputGroup>
                    </Col>
                </Row> */}
            </Card.Body>
            <Card.Body>
                {/* {JSON.stringify(user)} */}
            </Card.Body>
        </Card>
    )

}