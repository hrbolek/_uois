import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import Card from "react-bootstrap/Card"
import { RequestHistories } from "./RequestHistories"
import { CardText, EyeFill } from "react-bootstrap-icons"
import { useState } from "react"
import { FormCardBody } from "./FormCardBody"
import { useFreshItem } from "@uoisfrontend/shared"
import { FormFetchAsyncAction } from "../Actions/FormFetchAsyncAction"

export const RequestEditCard = ({request}) => {
    const histories = request?.histories || []
    const [formToShow, setFormToShow] = useState(histories.slice(-1))
    console.log("RequestEditCard.histories", histories)
    console.log("RequestEditCard.formToShow", formToShow)
    const [form] = useFreshItem({...formToShow}, FormFetchAsyncAction)
    console.log("RequestEditCard.form", form)
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <CardText /> {request.name} ({request.id})
                    </Col>
                    <Col></Col>
                    <Col></Col>
                    <Col>
                        <div className="d-flex justify-content-end">
                            <EyeFill />
                        </div>
                    </Col>
                </Row>
                
            </Card.Header>
            <Card.Body>
                
                <Row>
                    <Col md={8}>
                        <FormCardBody form={formToShow} />
                    </Col>
                    <Col md={4}>
                        <RequestHistories request={request} />
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}