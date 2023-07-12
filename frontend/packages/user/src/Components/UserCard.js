import Card from "react-bootstrap/Card"
import Form from "react-bootstrap/Form"
import InputGroup from "react-bootstrap/InputGroup"

import { EnvelopeAtFill, EnvelopeFill, PencilFill, PencilSquare, PersonFill, PlusLg } from "react-bootstrap-icons"
import { UserRoles } from "./UserRoles"
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import { UserGroups } from "./UserGroups"
import { Link } from "@uoisfrontend/shared"
import { UserEvent, UserEvents } from "./UserEvents"
import { UserClassification, UserClassificationEditable, UserClassificationsTable, UserClassificationsTableEditable } from "./UserClassification"
import { UserAddEventButton } from "./UserAddEventDialog"

const UserEmail = ({user, subject="Info", body="Dobr%C3%BD%20den%2C "}) => {
    const hrefValue = `mailto:${user.email}?subject=${subject}&body=${body}`
    // mailto:some@where.com?subject=Info&body=Dobr%C3%BD%20den%2C 
    return (
        <a href={hrefValue}><EnvelopeFill /></a>
    )
}

/**
 * Basic Element for user visualization
 * 
 * @function
 * 
 * @param {Object} props.user represents an entity to show
 * 
 * @returns JSX.Element
 */
export const UserCard = ({user}) => {
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
                            <Link id={user.id} tag="useredit"><PencilSquare /> </Link>
                        </div>
                    </Col>
                </Row>
            </Card.Header>
            <Card.Body>
                {/* <UserClassification user={user} />
                <UserClassificationEditable user={user} /> */}
                <span className="btn btn-outline-success"><Link tag="surveyuser" id={user.id}>Ankety</Link></span> <br />
                <span className="btn btn-outline-success"><Link tag="classificationuser" id={user.id}>Klasifikace</Link></span> <br />
            </Card.Body>
            <Card.Body>
                <hr />
                Kalendar
                <UserEvents user={user} />
                <br />
                <UserAddEventButton user={user} />
                <hr />
                {/* Ukoly
                <UserEvents user={user} />
                <br />
                <UserAddEventButton user={user} /> */}
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