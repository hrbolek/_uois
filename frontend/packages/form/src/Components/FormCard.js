import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { BuildingFill, PencilSquare } from "react-bootstrap-icons"
import { Demo, Link } from "@uoisfrontend/shared"
import { FormCardBody } from "./FormCardBody"

export const FormCard = ({form}) => {
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <BuildingFill /> {form.name}
                    </Col>
                    <Col>
                        
                    </Col>
                    <Col>
                        
                    </Col>
                    <Col>
                        <div className="d-flex justify-content-end">
                            <Link id={form.id} tag="formedit"><PencilSquare /> </Link>
                        </div>
                    </Col>
                </Row>

            </Card.Header>
            <Card.Body>
                <FormCardBody form={form} />
            </Card.Body>
        </Card>
    )
}