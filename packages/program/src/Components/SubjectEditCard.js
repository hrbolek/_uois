import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { PencilSquare, Receipt, EyeFill } from "react-bootstrap-icons"
import { Link } from "@uoisfrontend/shared"

export const SubjectEditCard = ({subject}) => {
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <Receipt /> {subject.name}
                    </Col>
                    <Col>
                        <Link tag="program" id={subject?.program?.id}>{subject?.program?.name}</Link>
                    </Col>
                    <Col>
                        
                    </Col>
                    <Col>
                        <div className="d-flex justify-content-end">
                            <Link id={subject.id} tag="subject"><EyeFill /> </Link>
                        </div>
                    </Col>
                </Row>

            </Card.Header>
            <Card.Body>               
                {JSON.stringify(subject)}
            </Card.Body>
        </Card>
    )
}