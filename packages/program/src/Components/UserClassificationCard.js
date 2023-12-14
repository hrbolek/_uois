import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { PersonFill, Receipt } from "react-bootstrap-icons"
import { Demo, Link } from "@uoisfrontend/shared"
import { ProgramSubjectsTable } from "./ProgramSubjectsTable"
import { Table } from "react-bootstrap"

const SemesterClassifications = ({semesterid, classifications}) => {
    if (classifications.length === 0) {
        return null
    }
    const classification0 = classifications[0]
    const semester = classification0?.semester || {}
    const subject = semester?.subject || {}
    const program = subject?.program || {}
    return (
        <tr>
            <td>
                <Link tag="program" id={program?.id}>{program?.name}</Link>
            </td>
            <td>
                <Link tag="subject" id={subject?.id}>{subject?.name}</Link>
            </td>
            <td>
                <Link tag="semester" id={semester?.id}>{semester?.order}</Link>
            </td>
            {classifications.map(
                classification => <td key={classification.id}>{classification?.level?.name}</td>
            )}
            <td>
                
            </td>
            <td>
                {/* {JSON.stringify(classifications)} */}
            </td>
        </tr>
        
    )
}
const SubjectClassifications = ({subjectid, classifications}) => {
    const semesters = classifications
        .map(classification => [classification?.semester, classification])
        .reduce(
            (accumulator, [semester, classification]) => {
                const value = accumulator[semester.id] || []
                value.push(classification)
                accumulator[semester.id] = value
                return accumulator
            }, {}
        )
    return (
        <>
            {Object.entries(semesters).map(
                    ([semesterid, classifications]) => <SemesterClassifications key={semesterid} semesterid={semesterid} classifications={classifications} />
            )}
        </>
    )
}

const ProgramClassifications = ({programid, classifications}) => {
    const subjects = classifications
        .map(classification => [classification?.semester?.subject, classification])
        .reduce(
            (accumulator, [subject, classification]) => {
                const value = accumulator[subject.id] || []
                value.push(classification)
                accumulator[subject.id] = value
                return accumulator
            }, {}
        )

    return (
        <>
            {Object.entries(subjects).map(
                    ([subjectid, classifications]) => <SubjectClassifications key={subjectid} subjectid={subjectid} classifications={classifications} />
            )}
        </>
    )
}

const UserClassificationsTableBody = ({programs}) => {
    return (
        <tbody>
            {Object.entries(programs).map(
                ([programid, classifications]) => 
                    <ProgramClassifications key={programid} programid={programid} classifications={classifications} />
            )}
        </tbody>
        // <tbody>
        //     <tr>
        //         <td>
        //             {JSON.stringify(programs)}
        //         </td>
        //     </tr>
        // </tbody>
    )
}

export const UserClassificationCard = ({user}) => {
    const classifications = user?.classifications || []
    const programs = classifications
        .map(classification => [classification?.semester?.subject?.program, classification])
        .reduce(
            (accumulator, [program, classification]) => {
                const value = accumulator[program.id] || []
                value.push(classification)
                accumulator[program.id] = value
                return accumulator
            }, {}
        )
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <Receipt /> 
                    </Col>
                    <Col>
                        <Link id={user.id} tag="user">{user.name} {user.surname}</Link>
                    </Col>
                    <Col>
                        
                    </Col>
                    <Col>
                        <div className="d-flex justify-content-end">
                            <Link id={user.id} tag="user"><PersonFill /> </Link>
                        </div>
                    </Col>
                </Row>

            </Card.Header>
            <Card.Body>
                <Table striped size="sm" bordered>
                    <thead>
                        <tr>
                            <th>Program</th>
                            <th>Předmět</th>
                            <th>Semestr</th>
                            <th>1.</th>
                            <th>2.</th>
                            <th>3.</th>
                            <th>M</th>
                            <th></th>
                        </tr>
                    </thead>
                    <UserClassificationsTableBody programs={programs} />
                </Table>
                
                
            </Card.Body>
            <Card.Body>
                {JSON.stringify(classifications)} <br />
                {JSON.stringify(user)}
            </Card.Body>
        </Card>
    )

    
}