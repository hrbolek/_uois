import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { BuildingFill, PencilSquare } from "react-bootstrap-icons"
import { Link } from "@uoisfrontend/shared"
import { FormCardBody } from "./FormCardBody"

export const FormEditCard = ({ form }) => {
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
                            <Link id={form.id} tag="facility"><PencilSquare /> </Link>
                        </div>
                    </Col>
                </Row>

            </Card.Header>
            <Card.Body>               
                <FormCardBody form={form} mode="edit"/>
            </Card.Body>
        </Card>
    )
}