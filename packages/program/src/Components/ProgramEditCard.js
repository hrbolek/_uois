import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { Receipt, EyeFill } from "react-bootstrap-icons"
import { Link } from "@uoisfrontend/shared"
import { ProgramSubjectsTable } from "./ProgramSubjectsTable"

export const ProgramEditCard = ({program}) => {
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
                            <Link id={program.id} tag="program"><EyeFill /> </Link>
                        </div>
                    </Col>
                </Row>

            </Card.Header>
            <Card.Body>               
                <ProgramSubjectsTable program={program} />
                {JSON.stringify(program)}
            </Card.Body>
        </Card>
    )
}