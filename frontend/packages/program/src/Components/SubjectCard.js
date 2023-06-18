import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { PencilSquare, Receipt } from "react-bootstrap-icons"
import { Demo, Link } from "@uoisfrontend/shared"

export const SubjectCard = ({subject}) => {
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
                            <Link id={subject.id} tag="subjectedit"><PencilSquare /> </Link>
                        </div>
                    </Col>
                </Row>

            </Card.Header>
            <Card.Body>
                <Row>
                    <Col>
                        <Demo />   
                    </Col>
                    <Col>
                    </Col>
                    <Col>
                    </Col>
                </Row>
    
                {JSON.stringify(subject)}
            </Card.Body>
        </Card>
    )
}