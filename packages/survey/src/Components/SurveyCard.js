import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { PencilSquare, Receipt } from "react-bootstrap-icons"
import { Demo, Link } from "@uoisfrontend/shared"

export const SurveyCard = ({survey}) => {
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <Receipt /> {survey.name}
                    </Col>
                    <Col>
                        
                    </Col>
                    <Col>
                        
                    </Col>
                    <Col>
                        <div className="d-flex justify-content-end">
                            <Link id={survey.id} tag="surveyedit"><PencilSquare /> </Link>
                        </div>
                    </Col>
                </Row>

            </Card.Header>
            <Card.Body>
                <Demo />   
                {JSON.stringify(survey)}
            </Card.Body>
        </Card>
    )
}