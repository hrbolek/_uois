import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { PencilSquare, Receipt } from "react-bootstrap-icons"
import { Demo, Link } from "@uoisfrontend/shared"
import { UserClassificationsTableConstant, SemesterClassificationsTableConstant } from "./Classifications"
import { PlanLessonsEditableTable, PlanLessonsTable } from "./PlanLessonsTable"

export const PlanCard = ({plan}) => {
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <span className="btn btn-sm btn-outline-success">
                        <Receipt />{" "}
                            <Link id={plan?.semester?.subject?.id} tag="subject">
                                {plan?.semester?.subject?.name}
                            </Link>{" "}[
                            <Link id={plan?.semester?.id} tag="semester">
                                {plan?.semester?.order}
                            </Link>
                            ]
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
                            <Link id={plan.id} tag="planedit"><PencilSquare /> </Link>
                        </div>
                    </Col>
                </Row>

            </Card.Header>
            <Card.Body>
                <PlanLessonsTable plan={plan} />
                {/* <UserClassificationsTableConstant />
                <SemesterClassificationsTableConstant /> */}
            </Card.Body>
            <Card.Body>
                
                {/* {JSON.stringify(plan)} */}
            </Card.Body>
        </Card>
    )
}