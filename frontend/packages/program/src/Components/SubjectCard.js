import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { PencilSquare, Receipt } from "react-bootstrap-icons"
import { Demo, Link } from "@uoisfrontend/shared"
import { SemesterCard } from "./SemesterCard"

export const SubjectCard = ({subject}) => {
    const semesters = subject?.semesters || []
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <Receipt /> Předmět {subject.name}
                    </Col>
                    <Col>
                        Program <Link tag="program" id={subject?.program?.id}>{subject?.program?.name}</Link>
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
                        {semesters.map(
                            semester => <span key={semester.id} className="btn btn-outline-success"><Link tag="semester" id={semester.id}>Semestr {semester.order}</Link></span>
                        )}        
                        {semesters.map(
                            semester => <SemesterCard key={semester.id} semester={{...semester, subject}} />
                        )}        
                    </Col>
                </Row>

                {JSON.stringify(subject)}
            </Card.Body>
        </Card>
    )
}