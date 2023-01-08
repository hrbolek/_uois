import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { TeacherSmall } from 'usersgroups/components/links';


export const TeacherSupervisorPhDActive = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Školitel - aktuální práce 
                </Card.Title>
            </Card.Header>
            <Card.Body>

            </Card.Body>
        </Card>

    )
}

export const TeacherSupervisorPhDFinished = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Školitel - ukončené práce 
                </Card.Title>
            </Card.Header>
            <Card.Body>

            </Card.Body>
        </Card>
    )
}

export const TeacherSupervisorMscActive = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Vedoucí - aktuální práce
                </Card.Title>
            </Card.Header>
            <Card.Body>

            </Card.Body>
        </Card>
    )
}

export const TeacherSupervisorMscFinished = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Vedoucí - ukončené práce
                </Card.Title>
            </Card.Header>
            <Card.Body>

            </Card.Body>
        </Card>
    )
}


export const TeacherSupervisor = (props) => {
    const { user } = props
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Školitel / Vedoucí <TeacherSmall user={user} />
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={6}>
                        <TeacherSupervisorMscActive user={user} />
                    </Col>
                    <Col md={6}>
                        <TeacherSupervisorPhDActive user={user} />
                    </Col>
                </Row>
                <Row>
                    <Col md={6}>
                        <TeacherSupervisorMscFinished user={user} />
                    </Col>
                    <Col md={6}>
                        <TeacherSupervisorPhDFinished user={user} />
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}