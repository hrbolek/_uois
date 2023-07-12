import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"
import Table from "react-bootstrap/Table"

import { PencilSquare, Receipt } from "react-bootstrap-icons"
import { Demo, Link } from "@uoisfrontend/shared"

const TopicTableRow = ({topic}) => {
    return (
        <tr>
            <td>{topic.order}</td>
            <td>{topic.name}</td>
            <td></td>
        </tr>
    )
}

const SemesterTopicsTable = ({semester}) => {
    const topics = semester?.topics || []
    return (
        <Table size="sm" striped bordered>
            <thead>
                <tr>
                    <th className="table-success border border-success" colSpan={3}>Témata</th>
                </tr>
                <tr>
                    <th>#</th>
                    <th>Název</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                {topics.map(
                    topic => <TopicTableRow key={topic.id} topic={topic} />
                )}
            </tbody>
        </Table>
    )
}

export const SemesterCard = ({semester}) => {
    const plans = semester?.plans || []
    const topics = semester?.topics || []
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <Receipt /> <Link tag="subject" id={semester?.subject?.id}>{semester?.subject?.name}</Link><Link tag="semester" id={semester.id}> [{semester.order}]</Link>
                    </Col>
                    <Col>
                        Klasifikace: {semester?.classificationType?.name}
                    </Col>
                    <Col>
                        Počet kreditů: {semester?.credits}
                    </Col>
                    <Col>
                        <div className="d-flex justify-content-end">
                            <Link id={semester.id} tag="semesteredit"><PencilSquare /> </Link>
                        </div>
                    </Col>
                </Row>

            </Card.Header>
            <Card.Body>
                <Row>
                    <Col>
                        
                    </Col>
                    <Col>
                    </Col>
                    <Col>
                    </Col>
                </Row>
                {plans.map(
                    (plan, index) => <Link tag="plan" id={plan.id}><span className="btn btn-outline-success">PSP ({index + 1})</span></Link>
                )}
                
                
                <SemesterTopicsTable semester={semester} />

                {JSON.stringify(semester)}
            </Card.Body>
        </Card>
    )
}