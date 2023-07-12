import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { EyeFill, PencilSquare, Receipt } from "react-bootstrap-icons"
import { Link } from "@uoisfrontend/shared"
import { PlanLessonsEditableTable } from "./PlanLessonsTable"
import { PlanPivotEditableTable } from "./PlanPivotEditableTable"

export const PlanEditCard = ({plan}) => {
    return (
        <>
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <span className="btn btn-sm btn-outline-success">
                            <Receipt />{" "}
                            <Link id="ce250a68-b095-11ed-9bd8-0242ac110002" tag="subject">
                                {plan?.semester?.subject?.name}
                                &nbsp;{plan?.semester?.order}{". semestr"}
                            </Link>
                            
                        </span>
                    </Col>
                    <Col>
                        <span className="btn btn-sm btn-outline-success">
                            <Link id="ce250a68-b095-11ed-9bd8-0242ac110002" tag="event">
                                2022/23 LS
                            </Link>
                        </span>

                    </Col>
                    <Col>
                        
                    </Col>
                    <Col>
                        <div className="d-flex justify-content-end">
                            <Link id={plan.id} tag="plan"><EyeFill /> </Link>
                        </div>
                    </Col>
                </Row>

            </Card.Header>
            {/* <Card.Body>             
                               

                
            </Card.Body> */}
        </Card>
        <PlanPivotEditableTable plan={plan} />
        </>
    )
}