import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { PencilSquare, Receipt } from "react-bootstrap-icons"
import { Demo, Link } from "@uoisfrontend/shared"
import { ProgramSubjectsTable } from "./ProgramSubjectsTable"

export const ProgramCard = ({program}) => {
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <Receipt /> {program.name}
                    </Col>
                    <Col>
                        {
                        program?.type?.id ? <>
                            <span className="btn btn-outline-success">{program?.type?.level?.name} </span>
                            <span className="btn btn-outline-success">{program?.type?.title?.name} </span>
                            <span className="btn btn-outline-success">{program?.type?.form?.name} </span>
                            <span className="btn btn-outline-success">{program?.type?.language?.name} </span>
                            </> : ""
                        }
                    </Col>
                    <Col>
                        
                    </Col>
                    <Col>
                        <div className="d-flex justify-content-end">
                            <Link id={program.id} tag="programedit"><PencilSquare /> </Link>
                        </div>
                    </Col>
                </Row>

            </Card.Header>
            <Card.Body>
                <Row>
                    <Col>
                        <ProgramSubjectsTable program={program} />
                    </Col>
                </Row>
    
                {JSON.stringify(program)}
            </Card.Body>
        </Card>
    )
}